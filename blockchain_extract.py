import asyncio
from typing import List, Coroutine, Tuple

from web3 import Web3, AsyncHTTPProvider, WebsocketProvider
from web3.eth import AsyncEth
from web3.types import BlockData, TxData, TxReceipt, RPCEndpoint
from web3._utils.rpc_abi import RPC
from web3.middleware import async_geth_poa_middleware, geth_poa_middleware
from web3.module import apply_result_formatters
from web3._utils.method_formatters import get_result_formatters
from web3.manager import RequestManager



class Web3Provider:
    request_kwargs={"timeout": 500}

    def get_base_provider(self, rpc: str) -> AsyncHTTPProvider:
        base_provider = AsyncHTTPProvider(rpc, request_kwargs = self.request_kwargs)
        # base_provider.middlewares += (http_retry_with_backoff_request_middleware,)        
        return base_provider
    
    def get_web3(self , rpc: str) -> Web3:
        base_provider = self.get_base_provider(rpc)
        web3_modules = {"eth": (AsyncEth,)}
        middlewares= [async_geth_poa_middleware]
        return  Web3(base_provider, modules = web3_modules, middlewares =  middlewares)

    def get_web3_ws(self, rpc: str) -> Web3:
        base_provider = WebsocketProvider(rpc)
        middlewares= [geth_poa_middleware]
        # web3_modules = {"eth": (AsyncEth,)}
        # middlewares= [async_geth_poa_middleware]
        return Web3(base_provider, 
            # modules=web3_modules,
            middlewares=middlewares)

    def result_forrmat(self, rpc: RPCEndpoint, params: list = [], result_raw_json: dict = {}):
        result_json =  RequestManager.formatted_response(result_raw_json, params)
        # TODO: by defult filter for extraData len 32 bytes
        if result_json.get('extraData'):
            result_json['extraData'] = result_json['extraData'][0:32]
        format = get_result_formatters(rpc, None)
        res = apply_result_formatters(format, result_json)
        return res




class Extract:

    def __init__(self, rpc_url):
        ''' http provider'''
        self.web3_provider = Web3Provider()
        self.w3 = self.web3_provider.get_web3(rpc_url)

    async def run_tasks(self, tasks: List[Coroutine]) -> any:
        return await asyncio.gather(*tasks)
    
    async def get_block_async(self, block_number: int) -> BlockData:
        block: BlockData = await self.w3.eth.get_block(block_number, full_transactions=True)
        # print('block_number', block_number)
        return block

    def get_block(self, block_number: int) -> BlockData:
        block = asyncio.run(self.get_block_async(block_number))
        return block

    def get_blocks(self, block_start, block_end) -> List[BlockData]:
        tasks = [self.get_block_async(block_number) for block_number in range(block_start, block_end)]
        blocks: List[BlockData] = asyncio.run(self.run_tasks(tasks))
        return blocks

    async def get_receipt_async(self, tx_hash) -> TxReceipt:
        tx_receive: TxReceipt = await self.w3.eth.get_transaction_receipt(tx_hash)
        return tx_receive

    def get_receipt(self, tx_hash) -> TxReceipt:
        tx_recive: TxReceipt = asyncio.run(self.get_receipt_async(tx_hash))
        return tx_recive
    
    def get_receipts(self, tx_hashes) -> List[TxReceipt]:
        tasks = [self.get_receipt_async(tx_hash) for tx_hash in tx_hashes]
        receipts = asyncio.run(self.run_tasks(tasks))
        return receipts


class ExtractWS:
   
    def __init__(self, rpc_url):
        self.web3_provider = Web3Provider()
        self.w3 = self.web3_provider.get_web3_ws(rpc_url)

    def get_futer_rpc(self, rpc_method: str, params: list = []):
        request_data = self.w3.provider.encode_rpc_request(
                                rpc_method,
                                params)
        futer = asyncio.run_coroutine_threadsafe(
                    self.w3.provider.coro_make_request(request_data),
                    self.w3.provider._loop)
        return futer

    def get_block_futer(self, block_number:int, full_transactions: bool=True ):
        futer_block = self.get_futer_rpc(RPC.eth_getBlockByNumber, [block_number, full_transactions])
        return futer_block

    def get_block(self, block_number: int, full_transactions: bool=True) -> BlockData:
        params = [block_number, full_transactions]
        json_block_raw = self.get_block_futer(*params).result()
        block: BlockData= self.web3_provider.result_forrmat(RPC.eth_getBlockByNumber, params, json_block_raw)
        return block

    def get_receipt_futer(self, tx_hash: str):
        futer_receipt = self.get_futer_rpc(RPC.eth_getTransactionReceipt, [tx_hash])
        return futer_receipt

    def get_receipt(self, tx_hash: str) -> TxReceipt:
        params = [tx_hash]
        json_result_raw = self.get_receipt_futer(*params).result()
        receipt: TxReceipt = self.web3_provider.result_forrmat(RPC.eth_getTransactionReceipt, params, json_result_raw)
        return receipt

    def get_receipts(self, tx_hashes) -> List[TxReceipt]:

        futers  = [ self.get_receipt_futer(tx_hashes[i]) for i in range(len(tx_hashes))]
        assert len(futers) == len(tx_hashes), 'get_receipts: assert len(futers) == len(tx_hashes)'

        receipts = []
        for i in range(len(futers)):
            print(i, 'hash:', tx_hashes[i])

            result = futers[i].result(10)
            receipt = self.web3_provider.result_forrmat(RPC.eth_getTransactionReceipt, [tx_hashes[i]], result)

        receipts = [ self.web3_provider.result_forrmat(RPC.eth_getTransactionReceipt, [tx_hashes[i]], futers[i].result()) for i in range(len(tx_hashes))]
        print(len(receipts))
        print(receipts[0])