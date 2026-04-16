from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


def kb_start() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Да, поехали", callback_data="start_quiz")],
        [InlineKeyboardButton(text="ℹ️ Расскажите об Айгерим", callback_data="about")],
    ])


def kb_q1() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="😰 Тревога и стресс", callback_data="q1_anxiety")],
        [InlineKeyboardButton(text="💔 Отношения", callback_data="q1_relations")],
        [InlineKeyboardButton(text="😮‍💨 Выгорание и усталость", callback_data="q1_burnout")],
        [InlineKeyboardButton(text="🔹 Другое", callback_data="q1_other")],
    ])


def kb_q2() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Несколько недель", callback_data="q2_weeks")],
        [InlineKeyboardButton(text="Несколько месяцев", callback_data="q2_months")],
        [InlineKeyboardButton(text="Больше года", callback_data="q2_year")],
    ])


def kb_q3() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Да, был опыт", callback_data="q3_yes")],
        [InlineKeyboardButton(text="Нет, впервые", callback_data="q3_no")],
    ])


def kb_q4() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💻 Онлайн (Zoom)", callback_data="q4_online")],
        [InlineKeyboardButton(text="🏢 Очно, Астана", callback_data="q4_offline")],
    ])


def kb_slots(slots: list[str]) -> InlineKeyboardMarkup:
    buttons = [[InlineKeyboardButton(text=slot, callback_data=f"slot_{i}")] for i, slot in enumerate(slots)]
    buttons.append([InlineKeyboardButton(text="✉️ Задать вопрос", callback_data="ask_question")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def kb_confirm() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Всё в силе", callback_data="confirm_ok")],
        [InlineKeyboardButton(text="🔄 Перенести", callback_data="reschedule")],
    ])
