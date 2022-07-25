
import asyncio
import logging
from time import time
from web3 import Web3
from web3.types import BlockData, TxData, TxReceipt
from blockchain_extract import Extract, ExtractWS
from mappers import (
    block_data_to_block_schema, 
    block_tx_data_to_transaction_schema, 
    receipt_tx_to_receipt_schema,
    receipt_log_to_log_receipt_schema
)
from schemas import Block, Transaction, TransactionLog
from typing import List
import config


logger = logging.getLogger(__name__)


class DataSave:
    '''
        Сохраниения данных 
    '''
    def __init__(self,):
        pass

    def save_blocks(self, blokcs: List[Block]):
        pass



class Dump:
    '''
        Получаем и сохранияем данные
    '''

    def __init__(self, rpc_url):

        self.rpc_url = rpc_url

        self.extract = ExtractWS(rpc_url) if 'wss' in rpc_url[:6] else Extract(self.rpc_url)
        self.data_save = DataSave()
        self.requests_count = 0

    async def get_blocks(self, block_start: int, block_end: int):
        tasks = [self.extract.get_block(block_number) for block_number in range(block_start, block_end)]
        blocks = await asyncio.gather(*tasks)
        return blocks

    async def get_receipts(self, tx_hashes) -> List[TxReceipt]:
        tasks = [self.extract.get_receipt_async(hash) for hash in tx_hashes]
        receipts = await asyncio.gather(*tasks)
        return receipts
    

    async def get_all_block_info_async(self, block_number):
        block_data = await self.extract.get_block_async(block_number)
        transactions: List[TxData] = block_data.transactions
        tx_hashes = [tx.hash.hex() for tx in transactions]
        receipts = await self.get_receipts(tx_hashes)
        logs: List[TransactionLog] = []
        for receipt in receipts:
            for log in receipt.logs:
                logs.append(receipt_log_to_log_receipt_schema(log))
        self.requests_count += len(receipts) + 1
        print('receipts', len(receipts), 'all requests:', self.requests_count)

        return {
            'block': block_data_to_block_schema(block_data),
            'transactions': [block_tx_data_to_transaction_schema(tx) for tx in transactions],
            'receipts': [receipt_tx_to_receipt_schema(receipt) for receipt in receipts],
            'logs': logs

        }

    def get_all_block_info(self, block_number):
        block_data = self.extract.get_block(block_number)
        transactions: List[TxData] = block_data.transactions
        tx_hashes = [tx.hash.hex() for tx in transactions]
        print('transactions', len(tx_hashes))
        receipts =  self.extract.get_receipts(tx_hashes)
        # logs: List[TransactionLog] = []
        # for receipt in receipts:
        #     for log in receipt.logs:
        #         logs.append(receipt_log_to_log_receipt_schema(log))
        # self.requests_count += len(receipts) + 1
        # print('receipts', len(receipts), 'all requests:', self.requests_count)

        # return {
        #     'block': block_data_to_block_schema(block_data),
        #     'transactions': [block_tx_data_to_transaction_schema(tx) for tx in transactions],
        #     'receipts': [receipt_tx_to_receipt_schema(receipt) for receipt in receipts],
        #     'logs': logs

        # }

    async def block_and_receipt_dumps(self, block_start: int, block_end: int, batch: int = 10):
        res = []
        for cur_block_start in range(block_start, block_end, batch):
            cur_block_end = cur_block_start + batch if (cur_block_start + batch) < block_end else block_end
            print('blocks:',cur_block_start, cur_block_end)
            tasks = [self.get_all_block_info(cur_block) for cur_block in range(cur_block_start, cur_block_end)]
            res_info = await asyncio.gather(*tasks)
            # print(len(res_info))
            res.append(res_info)
        return res

if __name__ == "__main__":

    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    url = config.RPC_URL
    extract = Extract(url)
    extractWs = ExtractWS(config.PRC_WS)

    dump = Dump(url)
    
    tik = time()
    # blocks = asyncio.run(dump.get_blocks(19714214, 19714214+50))
    # tx_hashes = [tx.hash.hex() for tx in blocks[0].transactions]
    # print('tx_hashes', len(tx_hashes))
    # receipts = asyncio.run(dump.get_receipts(tx_hashes[:20]))

    # blocks = extract.get_blocks(19714214, 19714214+50)

    # blocks = asyncio.run(dump.get_all_block_info_async(19714214+2))
    # blocks = Dump(config.PRC_WS).get_all_block_info(19714214)
    # blocks = asyncio.run(dump.block_and_receipt_dumps(19714214, 19714214+100, 5))
    # block = extractWs.get_block(19714214)
    # fblock = block_data_to_block_schema(block)
    # print(fblock)

    receipts = extractWs.get_receipts(['0xeb19fdd1a9dd026b6f5a7c53da6c09530b4493d43f3a10e9afb670d9e59c47df', '0x8d66350df851e30990e765a76159b54bae31e301b769d60730d18da777587373'])
    # print(receipts)
    # res = extractWs.get_receipt('0xeb19fdd1a9dd026b6f5a7c53da6c09530b4493d43f3a10e9afb670d9e59c47df')
    # print('blocks', len(blocks))
    print(time() - tik)





