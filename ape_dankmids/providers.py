
import shutil
from urllib.parse import urlparse

from ape.api.networks import LOCAL_NETWORK_NAME
from ape.exceptions import ProviderError
from ape.logging import logger
from ape_geth.providers import AsyncGethProvider, EphemeralGeth, GethNotInstalledError
from dank_mids import setup_dank_w3
from multicall.utils import get_async_w3
from web3 import HTTPProvider, Web3
from web3.gas_strategies.rpc import rpc_gas_price_strategy


class DankProvider(AsyncGethProvider):
    async def connect(self):
        self._client_version = None  # Clear cached version when connecting to another URI.
        self._web3 = setup_dank_w3(get_async_w3(Web3(HTTPProvider(self.uri))))
        self._web3.provider._request_kwargs["timeout"] = 30 * 60

        if not await self._web3.isConnected():
            if self.network.name != LOCAL_NETWORK_NAME:
                raise ProviderError(
                    f"When running on network '{self.network.name}', "
                    f"the Geth plugin expects the Geth process to already "
                    f"be running on '{self.uri}'."
                )

            # Start an ephemeral geth process.
            parsed_uri = urlparse(self.uri)

            if parsed_uri.hostname not in ("localhost", "127.0.0.1"):
                raise ConnectionError(f"Unable to connect web3 to {parsed_uri.hostname}.")

            if not shutil.which("geth"):
                raise GethNotInstalledError()

            # Use mnemonic from test config
            config_manager = self.network.config_manager
            test_config = config_manager.get_config("test")
            mnemonic = test_config["mnemonic"]
            num_of_accounts = test_config["number_of_accounts"]

            self._geth = EphemeralGeth(
                self.data_folder,
                parsed_uri.hostname,
                parsed_uri.port,
                mnemonic,
                number_of_accounts=num_of_accounts,
            )
            self._geth.connect()

            if not await self._web3.isConnected():
                self._geth.disconnect()
                raise ConnectionError("Unable to connect to locally running geth.")
        else:
            client_version = await self.client_version
            if "geth" in client_version.lower():
                logger.info(f"Connecting to existing Geth node at '{self.uri}'.")
            elif "erigon" in client_version.lower():
                logger.info(f"Connecting to existing Erigon node at '{self.uri}'.")
                self.concurrency = 8
                self.block_page_size = 40_000
            else:
                network_name = client_version.split("/")[0]
                logger.warning(f"Connecting Geth plugin to non-Geth network '{network_name}'.")

        self._web3.eth.set_gas_price_strategy(rpc_gas_price_strategy)
