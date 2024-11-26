import asyncio
from aiogram.types import Message


async def delayed_delete(message: Message, reply_message: Message, delay: int):
    """
    Удаляет сообщение и связанный ответ с заданной задержкой.
    """
    await asyncio.sleep(delay)
    try:
        await message.delete()
        await reply_message.delete()
        print(f"{message.from_user.username} насрал: {message.text}")
    except Exception as e:
        print(f"Ошибка при удалении сообщения: {e}")
