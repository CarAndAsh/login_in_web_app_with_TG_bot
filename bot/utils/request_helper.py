from aiohttp import ClientSession


class RequestHelper:
    session: ClientSession|None = None

    async def __aenter__(self):
        self.session: ClientSession = ClientSession()
        return self.session


    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()


    async def get(self, url, **kwargs):
        async with self as session:
            return await session.get(url, **kwargs)


    async def post(self, url, **kwargs):
        async with self as session:
            return await session.post(url, **kwargs)


    async def patch(self, url, **kwargs):
        async with self as session:
            return await session.patch(url, **kwargs)


request_helper = RequestHelper()
