import aiohttp
from asyncio import Semaphore

from app.network.abstractions.session_manager import AbstractSessionManager


class SessionManager(AbstractSessionManager):
    def __init__(self, headers=None, semaphore: Semaphore = Semaphore(10)):
        self.headers = headers or {"User-Agent": "Mozilla/5.0"}
        self.semaphore = semaphore

    def create_session(self):
        return aiohttp.ClientSession(headers=self.headers)
