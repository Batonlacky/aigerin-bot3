"""
Планировщик напоминаний.
Для Railway (без постоянного хранилища) используем asyncio задачи в памяти.
Напоминания живут пока процесс запущен — этого достаточно для демо и реального использования
если бот не перезапускается между записью и сессией.
"""
import asyncio
import logging
from datetime import datetime, timedelta

from aiogram import Bot
from .keyboards import kb_confirm

logger = logging.getLogger(__name__)

# Пример парсинга слота — слоты захардкожены в handlers.py в формате:
# "📅 Пятница, 18 апреля в 11:00"
# Для реального проекта нужно хранить datetime в базе.
# Здесь делаем демо-напоминания: через 10 секунд (имитация 24ч) и через 20 секунд (имитация 2ч).
# На проде меняем delays на реальные.

DEMO_MODE = True  # True = короткие задержки для демонстрации


async def _send_reminder_24h(bot: Bot, user_id: int, slot: str):
    delay = 10 if DEMO_MODE else 86400  # 10 сек или 24 часа
    await asyncio.sleep(delay)
    try:
        await bot.send_message(
            user_id,
            f"🌿 Напоминаю: <b>завтра</b> у вас сессия с Айгерим!\n\n"
            f"<b>{slot}</b>\n\n"
            "Zoom-ссылка придёт за 30 минут до встречи.\n\n"
            "Всё в силе?",
            reply_markup=kb_confirm(),
            parse_mode="HTML",
        )
        logger.info(f"Напоминание 24ч отправлено → {user_id}")
    except Exception as e:
        logger.error(f"Ошибка напоминания 24ч для {user_id}: {e}")


async def _send_reminder_2h(bot: Bot, user_id: int, slot: str):
    delay = 20 if DEMO_MODE else 79200  # 20 сек или 22 часа (через 2ч после 24ч = за 2ч до сессии)
    await asyncio.sleep(delay)
    try:
        await bot.send_message(
            user_id,
            f"🙌 Через <b>2 часа</b> — ваша сессия с Айгерим!\n\n"
            f"<b>{slot}</b>\n\n"
            "💡 Совет: найдите тихое место, налейте чай, "
            "подумайте что хотите обсудить.\n\n"
            "Если нужно перенести — /reschedule",
            parse_mode="HTML",
        )
        logger.info(f"Напоминание 2ч отправлено → {user_id}")
    except Exception as e:
        logger.error(f"Ошибка напоминания 2ч для {user_id}: {e}")


async def schedule_reminders(bot: Bot, user_id: int, slot: str):
    """Запускает два фоновых задания с напоминаниями."""
    asyncio.create_task(_send_reminder_24h(bot, user_id, slot))
    asyncio.create_task(_send_reminder_2h(bot, user_id, slot))
    logger.info(f"Напоминания запланированы для user_id={user_id}, слот={slot}")
