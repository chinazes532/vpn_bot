import typing
from dataclasses import dataclass

import httpx

UNABLE_TO_GET_METRICS_ERROR = "Unable to get metrics"


@dataclass
class OutlineKey:
    """
    Describes a key in the Outline server
    """

    key_id: str
    name: str
    password: str
    port: int
    method: str
    access_url: str
    used_bytes: int
    data_limit: typing.Optional[int]

    def __init__(self, response: dict, metrics: dict = None):
        self.key_id = response.get("id")
        self.name = response.get("name")
        self.password = response.get("password")
        self.port = response.get("port")
        self.method = response.get("method")
        self.access_url = response.get("accessUrl")
        self.used_bytes = (
            metrics.get("bytesTransferredByUser Id").get(response.get("id"))
            if metrics
            else 0
        )
        self.data_limit = response.get("dataLimit", {}).get("bytes")


class OutlineServerErrorException(Exception):
    pass


class OutlineLibraryException(Exception):
    pass


class OutlineVPN:
    """
    An Outline VPN connection
    """

    def __init__(self, api_url: str, cert_sha256: str):
        self.api_url = api_url
        self.client = httpx.AsyncClient(verify=False)

    async def get_keys(self, timeout: int = None):
        """Get all keys in the outline server"""
        response = await self.client.get(
            f"{self.api_url}/access-keys/", timeout=timeout
        )
        if response.status_code == 200 and "accessKeys" in response.json():
            response_metrics = await self.client.get(
                f"{self.api_url}/metrics/transfer", timeout=timeout
            )
            if (
                response_metrics.status_code >= 400
                or "bytesTransferredByUser Id" not in response_metrics.json()
            ):
                raise OutlineServerErrorException(UNABLE_TO_GET_METRICS_ERROR)

            response_json = response.json()
            result = []
            for key in response_json.get("accessKeys"):
                result.append(OutlineKey(key, response_metrics.json()))
            return result
        raise OutlineServerErrorException("Unable to retrieve keys")

    async def get_key(self, key_id: str, timeout: int = None) -> OutlineKey:
        response = await self.client.get(
            f"{self.api_url}/access-keys/{key_id}", timeout=timeout
        )
        if response.status_code == 200:
            key = response.json()

            response_metrics = await self.client.get(
                f"{self.api_url}/metrics/transfer", timeout=timeout
            )
            if (
                response_metrics.status_code >= 400
                or "bytesTransferredByUser Id" not in response_metrics.json()
            ):
                raise OutlineServerErrorException(UNABLE_TO_GET_METRICS_ERROR)

            return OutlineKey(key, response_metrics.json())
        else:
            raise OutlineServerErrorException("Unable to get key")

    async def create_key(
        self,
        key_id: str = None,
        name: str = None,
        method: str = None,
        password: str = None,
        data_limit: int = None,
        port: int = None,
        timeout: int = None,
    ) -> OutlineKey:
        """Create a new key"""

        payload = {}
        if name:
            payload["name"] = name
        if method:
            payload["method"] = method
        if password:
            payload["password"] = password
        if data_limit:
            payload["limit"] = {"bytes": data_limit}
        if port:
            payload["port"] = port
        if key_id:
            payload["id"] = key_id
            response = await self.client.put(
                f"{self.api_url}/access-keys/{key_id}",
                json=payload,
                timeout=timeout,
            )
        else:
            response = await self.client.post(
                f"{self.api_url}/access-keys",
                json=payload,
                timeout=timeout,
            )

        if response.status_code == 201:
            key = response.json()
            outline_key = OutlineKey(key)
            return outline_key

        raise OutlineServerErrorException(f"Unable to create key. {response.text}")

    async def delete_key(self, key_id: str, timeout: int = None) -> bool:
        """Delete a key"""
        response = await self.client.delete(
            f"{self.api_url}/access-keys/{key_id}",
            verify=False,
            timeout=timeout
        )

        return response.status_code == 204

