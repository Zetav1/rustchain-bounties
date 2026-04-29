import httpx
import os
import logging

logger = logging.getLogger(__name__)

class RustChainAPI:
    """
    Core API Client for RustChain Node interaction.
    Designed for scalability and reuse across different interfaces.
    """
    def __init__(self, node_url=None, verify_ssl=True):
        self.node_url = node_url or os.getenv("RUSTCHAIN_NODE_URL", "https://50.28.86.131")
        self.verify_ssl = verify_ssl

    async def _get(self, endpoint, params=None):
        try:
            async with httpx.AsyncClient(verify=self.verify_ssl, timeout=10.0) as client:
                response = await client.get(f"{self.node_url}{endpoint}", params=params)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPError as e:
            logger.error(f"API Error at {endpoint}: {str(e)}")
            return {"error": "Node unreachable or invalid response"}

    async def get_balance(self, wallet_id):
        return await self._get("/wallet/balance", {"wallet_id": wallet_id})

    async def get_miners(self):
        return await self._get("/api/miners")

    async def get_epoch(self):
        return await self._get("/epoch")

    async def get_health(self):
        return await self._get("/health")
