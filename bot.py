import asyncio
from aiogram import Bot, Dispatcher
from app.heandlers import router
from app.database.models import async_main
from aiogram.types import Message


async def main():
    await async_main()
    bot = Bot(token='TOKEN')
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)
    
bot = Bot(token='TOKEN')

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')
