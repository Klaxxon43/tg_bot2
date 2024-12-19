import asyncio
from aiogram import Bot, Dispatcher
from app.heandlers import router
from app.database.models import async_main
from aiogram.types import Message

token='7585776111:AAHwz-FOu9kZ96piHD0ZlU8QrUBxqNgS8Bc'

async def main():
    await async_main()
    bot = Bot(token='7585776111:AAHwz-FOu9kZ96piHD0ZlU8QrUBxqNgS8Bc')
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)
    
bot = Bot(token='7585776111:AAHwz-FOu9kZ96piHD0ZlU8QrUBxqNgS8Bc')

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')
