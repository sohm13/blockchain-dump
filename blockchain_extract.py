from web3 import Web3, AsyncHTTPProvider
from web3.eth import AsyncEth
from web3.types import BlockData, TxData, TxReceipt
from web3._utils.rpc_abi import RPC
from web3.middleware import async_geth_poa_middleware


class Web3Provider:
    request_kwargs={"timeout": 500}

    def get_base_provider(self, rpc: str) -> AsyncHTTPProvider:
        base_provider = AsyncHTTPProvider(rpc, request_kwargs = self.request_kwargs)
        # base_provider.middlewares += (http_retry_with_backoff_request_middleware,)        
        return base_provider
    
    def get_web3(self ,base_provider: AsyncHTTPProvider) -> Web3:
        web3_modules = {"eth": (AsyncEth,)}
        middlewares= [async_geth_poa_middleware]
        return  Web3(base_provider, modules = web3_modules, middlewares =  middlewares)




class Extract:

    def __init__(self, rpc_url):
        self.web3_provider = Web3Provider()
        self.base_provider = self.web3_provider.get_base_provider(rpc_url)
        self.w3 = self.web3_provider.get_web3(self.base_provider)
    
    async def get_block(self, block_number: int) -> BlockData:
        block: BlockData = await self.w3.eth.get_block(block_number, full_transactions=True)
        return block
        
        # can get raw block
        # block = await self.base_provider.make_request(
        #         "eth_getBlockByNumber",
        #         [hex(block_number), True],
        #         )

    async def get_receive(self, tx_hash) -> TxReceipt:
        tx_receive: TxReceipt = await self.w3.eth.get_transaction_receipt(tx_hash)
        return tx_receive


