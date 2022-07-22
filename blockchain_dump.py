
import asyncio
import logging
from time import time
from web3 import Web3
from web3.types import BlockData, TxData, TxReceipt
from blockchain_extract import Extract
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

        self.extract = Extract(self.rpc_url)
        self.data_save = DataSave()


    async def get_blocks(self, block_start: int, block_end: int):
        tasks = [self.extract.get_block(block_number) for block_number in range(block_start, block_end)]
        blocks = await asyncio.gather(*tasks)
        return blocks

    async def get_receipts(self, tx_hashes) -> List[TxReceipt]:
        tasks = [self.extract.get_receive(hash) for hash in tx_hashes]
        receipts = await asyncio.gather(*tasks)
        return receipts

    async def get_all_block_info(self, block_number):
        block_data = await self.extract.get_block(block_number)
        transactions: List[TxData] = block_data.transactions
        tx_hashes = [tx.hash.hex() for tx in transactions]
        receipts = await self.get_receipts(tx_hashes)
        logs: List[TransactionLog] = []
        for receipt in receipts:
            for log in receipt.logs:
                logs.append(receipt_log_to_log_receipt_schema(log))
        return {
            'block': block_data_to_block_schema(block_data),
            'transactions': [block_tx_data_to_transaction_schema(tx) for tx in transactions],
            'receipts': [receipt_tx_to_receipt_schema(receipt) for receipt in receipts],
            'logs': logs

        }

    async def block_and_receipt_dumps(self, block_start: int, block_end: int, batch: int = 100):
        
        for i in range(block_start, block_end+1, batch):
            pass



if __name__ == "__main__":
    url = config.RPC_URL
    dump = Dump(url)
    
    tik = time()
    blocks = asyncio.run(dump.get_all_block_info(19714214))
    print(time() - tik)
    print(blocks['receipts'][0])
    print(len(blocks['receipts']))
    # print(blocks['block'])
    # print(blocks['transactions'][0])
    # print(blocks['logs'][0])




