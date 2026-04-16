import logging
from datetime import datetime, timedelta
from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from .states import Quiz
from .keyboards import kb_start, kb_q1, kb_q2, kb_q3, kb_q4, kb_slots, kb_confirm
from .scheduler import schedule_reminders
from .config import ADMIN_ID

router = Router()
logger = logging.getLogger(__name__)

# Свободные слоты (в реальном проекте — из Google Calendar / базы)
FREE_SLOTS = [
    "📅 Пятница, 18 апреля в 11:00",
    "📅 Пятница, 18 апреля в 15:00",
    "📅 Суббота, 19 апреля в 12:00",
]

Q_LABELS = {
    "q1_anxiety": "😰 Тревога и стресс",
    "q1_relations": "💔 Отношения",
    "q1_burnout": "😮‍💨 Выгорание и усталость",
    "q1_other": "🔹 Другое",
    "q2_weeks": "Несколько недель",
    "q2_months": "Несколько месяцев",
    "q2_year": "Больше года",
    "q3_yes": "Да, был опыт",
    "q3_no": "Нет, впервые",
    "q4_online": "💻 Онлайн (Zoom)",
    "q4_offline": "🏢 Очно, Астана",
}


# ─── /start ────────────────────────────────────────────────────────────────────

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Здравствуйте 🌿\n\n"
        "Я — бот психолога <b>Айгерим Нурлановой</b>.\n"
        "Помогу вам понять, с каким запросом вы пришли, "
        "и подберу удобное время для консультации.\n\n"
        "Это займёт ~2 минуты.\n\n"
        "<b>Готовы начать?</b>",
        reply_markup=kb_start(),
        parse_mode="HTML",
    )


# ─── О психологе ───────────────────────────────────────────────────────────────

@router.callback_query(F.data == "about")
async def about_handler(call: CallbackQuery):
    await call.message.edit_text(
        "🌿 <b>Айгерим Нурланова</b> — психолог, Астана\n\n"
        "Специализация: тревожность, выгорание, отношения\n"
        "Опыт: 6 лет практики\n"
        "Форматы: онлайн (Zoom) и очно\n"
        "Стоимость сессии: <b>25 000 ₸</b> (60 минут)\n\n"
        "Нажмите «Да, поехали» — и я подберу для вас подходящее время 🙌",
        reply_markup=kb_start(),
        parse_mode="HTML",
    )
    await call.answer()


# ─── Старт квиза ───────────────────────────────────────────────────────────────

@router.callback_query(F.data == "start_quiz")
async def start_quiz(call: CallbackQuery, state: FSMContext):
    await state.set_state(Quiz.q1)
    await call.message.edit_text(
        "<b>Вопрос 1 из 4</b>\n\n"
        "Что сейчас беспокоит вас больше всего?",
        reply_markup=kb_q1(),
        parse_mode="HTML",
    )
    await call.answer()


# ─── Q1 ────────────────────────────────────────────────────────────────────────

@router.callback_query(Quiz.q1, F.data.startswith("q1_"))
async def q1_handler(call: CallbackQuery, state: FSMContext):
    await state.update_data(q1=Q_LABELS[call.data])
    await state.set_state(Quiz.q2)
    await call.message.edit_text(
        "<b>Вопрос 2 из 4</b>\n\n"
        "Как давно вы живёте с этим состоянием?",
        reply_markup=kb_q2(),
        parse_mode="HTML",
    )
    await call.answer()


# ─── Q2 ────────────────────────────────────────────────────────────────────────

@router.callback_query(Quiz.q2, F.data.startswith("q2_"))
async def q2_handler(call: CallbackQuery, state: FSMContext):
    await state.update_data(q2=Q_LABELS[call.data])
    await state.set_state(Quiz.q3)
    await call.message.edit_text(
        "<b>Вопрос 3 из 4</b>\n\n"
        "Был ли у вас опыт работы с психологом?",
        reply_markup=kb_q3(),
        parse_mode="HTML",
    )
    await call.answer()


# ─── Q3 ────────────────────────────────────────────────────────────────────────

@router.callback_query(Quiz.q3, F.data.startswith("q3_"))
async def q3_handler(call: CallbackQuery, state: FSMContext):
    await state.update_data(q3=Q_LABELS[call.data])
    await state.set_state(Quiz.q4)
    await call.message.edit_text(
        "<b>Вопрос 4 из 4</b>\n\n"
        "Какой формат вам удобнее?",
        reply_markup=kb_q4(),
        parse_mode="HTML",
    )
    await call.answer()


# ─── Q4 → результат + слоты ────────────────────────────────────────────────────

@router.callback_query(Quiz.q4, F.data.startswith("q4_"))
async def q4_handler(call: CallbackQuery, state: FSMContext):
    await state.update_data(q4=Q_LABELS[call.data])
    data = await state.get_data()
    await state.set_state(Quiz.choose_slot)

    slots_text = "\n".join(FREE_SLOTS)
    await call.message.edit_text(
        "Спасибо 🌿\n\n"
        "По вашим ответам Айгерим подготовит персональный подход к первой сессии.\n\n"
        f"<b>Ближайшие свободные окна:</b>\n{slots_text}\n\n"
        "💰 Стоимость первой сессии: <b>25 000 ₸</b> (60 минут)\n\n"
        "Выберите удобное время 👇",
        reply_markup=kb_slots(FREE_SLOTS),
        parse_mode="HTML",
    )
    await call.answer()


# ─── Выбор слота → подтверждение ───────────────────────────────────────────────

@router.callback_query(Quiz.choose_slot, F.data.startswith("slot_"))
async def slot_handler(call: CallbackQuery, state: FSMContext, bot: Bot):
    idx = int(call.data.split("_")[1])
    chosen_slot = FREE_SLOTS[idx]
    data = await state.get_data()
    data["slot"] = chosen_slot
    data["user_id"] = call.from_user.id
    data["username"] = call.from_user.username or call.from_user.full_name
    await state.update_data(slot=chosen_slot, user_id=call.from_user.id)

    # Уведомление администратору
    admin_text = (
        "🔔 <b>Новая запись!</b>\n\n"
        f"👤 Клиент: @{data['username']}\n"
        f"📌 Запрос: {data.get('q1', '—')}\n"
        f"⏳ Длительность: {data.get('q2', '—')}\n"
        f"🧠 Опыт терапии: {data.get('q3', '—')}\n"
        f"💻 Формат: {data.get('q4', '—')}\n"
        f"📅 Слот: {chosen_slot}"
    )
    try:
        await bot.send_message(ADMIN_ID, admin_text, parse_mode="HTML")
    except Exception as e:
        logger.error(f"Не удалось отправить уведомление админу: {e}")

    # Подтверждение клиенту
    format_info = "Zoom-ссылка придёт за 30 минут до сессии" if "Zoom" in data.get("q4", "") else "Адрес: ул. Кенесары 4, офис 12, Астана"
    await call.message.edit_text(
        f"Записаны ✅\n\n"
        f"<b>{chosen_slot}</b>\n"
        f"📍 {format_info}\n\n"
        "Я напомню вам <b>за 24 часа</b> и <b>за 2 часа</b> до сессии.\n"
        "Если нужно перенести — напишите /reschedule",
        parse_mode="HTML",
    )

    # Планируем напоминания
    await schedule_reminders(bot, call.from_user.id, chosen_slot)
    await state.clear()
    await call.answer()


# ─── Вопрос (без слота) ────────────────────────────────────────────────────────

@router.callback_query(F.data == "ask_question")
async def ask_question_handler(call: CallbackQuery):
    await call.message.answer(
        "Напишите ваш вопрос — Айгерим ответит лично в течение нескольких часов 🌿"
    )
    await call.answer()


# ─── /reschedule ───────────────────────────────────────────────────────────────

@router.message(Command("reschedule"))
async def reschedule_handler(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Хорошо, давайте перенесём.\n\n"
        "Напишите @aigerin_psych или нажмите /start чтобы выбрать новый слот.",
    )


# ─── Напоминания — подтверждение ───────────────────────────────────────────────

@router.callback_query(F.data == "confirm_ok")
async def confirm_ok(call: CallbackQuery):
    await call.message.edit_text("Отлично! До встречи 🌿")
    await call.answer()


@router.callback_query(F.data == "reschedule")
async def reschedule_callback(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_text(
        "Хорошо, давайте перенесём.\n\n"
        "Напишите /start чтобы выбрать новый слот.",
    )
    await call.answer()
