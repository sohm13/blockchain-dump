
import asyncio
from web3 import Web3
from web3.types import BlockData, TxData

from blockchain_extract import Extract
from mappers import BlockMapper
from schemas import Block, Transaction
import config

from time import time
  



class Dump:

    def __init__(self, rpc_url):

        self.rpc_url = rpc_url

        self.extract = Extract(self.rpc_url)
        self.block_mapper = BlockMapper()

    async def block_dump(self, block_number):
        block_data = await self.extract.get_block(block_number)
        return block_data
    
    async def blocks_dump(self, block_start: int, block_end: int):
        tasks = [self.block_dump(block_number) for block_number in range(block_start, block_end)]
        blocks = await asyncio.gather(*tasks)
        return blocks

    async def receive_dump(self, tx_hash):
        recevie = await self.extract.get_receive(tx_hash)
        return recevie

    async def receives_dump(self, tx_hashes):
        tasks = [self.receive_dump(hash) for hash in tx_hashes]
        receives = await asyncio.gather(*tasks)
        print(len(receives))
        return receives



if __name__ == "__main__":
    url = config.RPC_URL
    dump = Dump(url)
    
    tik = time()
    blocks = asyncio.run(dump.blocks_dump(19714214, 19714214+2))
    print(time() - tik)
    all_transactions = [ block.transactions for block in blocks]
    # all_hash = [tx.hash for tx in all_transactions]
    print( 'blocks:',len(all_transactions) )

    # tik = time()
    # for block_transactions in all_transactions:
    #     tx_hs = [tx.hash.hex() for tx in block_transactions]
    #     print('tx_hs', len(tx_hs))
    # asyncio.run(dump.receives_dump(tx_hs))
    
    # print(time() - tik)



