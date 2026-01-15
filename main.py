import asyncio

from app.create_app import start_web_app
from bot.bot_core.test_bot import start_bot


async def main():
     async with asyncio.TaskGroup() as group:
         group.create_task(start_web_app())
         group.create_task(start_bot())

if __name__ == '__main__':
    asyncio.run(main())
