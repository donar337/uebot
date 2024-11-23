import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.bot import DefaultBotProperties

from Spam_clf.spam_classification import ModelReducer

# Укажите токен вашего бота
BOT_TOKEN = "ХУЙ_СОСИТЕ"

# Укажите имя стикерпакета (например, "FunnyStickers")
TARGET_STICKERS_NAMES = {"nefory842", "vagodrochKKX_by_fStikBot"}

FORBIDDEN = {"AgADLFoAAqx_EUo"}

Z_COOL_STICKER = "AgADaU4AAkxqAAFI"

SPAM_MODEL = ModelReducer()


async def start_handler(message: Message):
    """
    Обработчик команды /start.
    """
    await message.answer("Привет! Я бот, который удаляет Саввины блядские стикеры")


async def sticker_handler(message: Message):
    """
        Обработчик стикеров.
        Удаляет сообщения, если это Саввин блядский стикер.
    """
    print(
        f"Стикер {message.sticker.file_unique_id} из {message.sticker.set_name} от {message.from_user.username} в {message.chat.title}",
        end=" ")
    if (
        (message.from_user.username == "s3drmn" and message.sticker.set_name is None) or
        message.sticker.set_name in TARGET_STICKERS_NAMES and
        not message.sticker.file_unique_id == Z_COOL_STICKER
    ):
        try:
            await message.delete()
            print("ликвидирован")
        except Exception as e:
            print(f"Ошибка при удалении сообщения: {e}")
    else:
        print("оставлен")


async def spam_handler(message: Message):
    """
        Обработчик стикеров.
        Удаляет сообщения, если это Саввин блядский стикер.
    """
    try:
        if SPAM_MODEL.spam_or_not(message.text) == 1:
            try:
                await message.delete()
                print(f"{message.from_user.username} насрал: {message.text}")
            except Exception as e:
                print(f"Ошибка при удалении сообщения: {e}")
    except Exception as e:
        print(f"Макс - говножуй, {e}")


async def main():
    # Инициализация бота с использованием DefaultBotProperties
    bot = Bot(
        token=BOT_TOKEN,
        session=AiohttpSession(),
        default=DefaultBotProperties(parse_mode="HTML")
    )
    dp = Dispatcher()

    # Регистрация хэндлеров
    dp.message.register(start_handler, Command("start"))
    dp.message.register(sticker_handler, F.content_type == "sticker")
    dp.message.register(spam_handler, F.content_type == "text")

    # Запуск polling
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
