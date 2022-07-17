from asyncio import iscoroutine

import pytest
from ape import Contract, networks
from ape.exceptions import ProviderNotConnectedError
from ape.types import ContractLog
from multicall.utils import await_awaitable

from ape_dankmids import DankProvider


def test_connect_disconnect():
    with networks.ethereum.mainnet.use_provider("dankmids") as provider:
        assert isinstance(provider, DankProvider)
        assert await_awaitable(provider.get_balance("0x0000000000000000000000000000000000000000")) > 0
    
    with pytest.raises(ProviderNotConnectedError):
        await_awaitable(provider.get_balance("0x0000000000000000000000000000000000000000"))

def test_chain_id():
    with networks.ethereum.mainnet.use_provider("dankmids") as provider:
        assert await_awaitable(provider.chain_id) == 1

def test_client_version():
    with networks.ethereum.mainnet.use_provider("dankmids") as provider:
        assert isinstance(await_awaitable(provider.client_version), str)
    
def test_context_switching_for_contract_calls():
    with networks.ethereum.mainnet.use_provider("dankmids") as provider:
        weth = await_awaitable(Contract("0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2"))
        assert iscoroutine(weth.totalSupply())
        assert await_awaitable(weth.totalSupply()) >= 0
    with networks.ethereum.mainnet.use_default_provider() as provider:
        weth = Contract("0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2")
        assert weth.totalSupply() >= 0

def test_getLogs():
    with networks.ethereum.mainnet.use_provider("dankmids") as provider:
        weth = await_awaitable(Contract("0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"))
        coro = weth.Transfer.range(14_000_000, 14_100_000)
        assert iscoroutine(coro)
        async def validate_logs(async_generator):
            logs = []
            async for log in async_generator:
                assert isinstance(log, ContractLog)
                assert isinstance(log.block_number, int)
                assert isinstance(log.transaction_hash, str)
                assert log.name == "Transfer"
                assert log.contract_address == "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"
                logs.append(log)
            return logs
        logs = await_awaitable(validate_logs(await_awaitable(coro)))
        assert len(logs) == 1717503
        