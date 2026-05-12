# SPDX-License-Identifier: MIT
import aiohttp
import logging

logger = logging.getLogger(__name__)

class RustChainAPI:
    def __init__(self, base_url="https://rustchain.org/api", verify_ssl=True):
        self.base_url = base_url
        self.verify_ssl = verify_ssl

    async def _get(self, endpoint):
        url = f"{self.base_url}{endpoint}"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, ssl=self.verify_ssl) as response:
                    if response.status == 200:
                        return await response.json()
                    return {"error": f"HTTP {response.status}"}
            except Exception as e:
                return {"error": str(e)}

    async def get_balance(self, wallet_id):
        return await self._get(f"/balance/{wallet_id}")

    async def get_miners(self):
        return await self._get("/miners")

    async def get_epoch(self):
        return await self._get("/epoch")

    async def get_health(self):
        return await self._get("/health")
