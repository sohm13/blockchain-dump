from blockchain_extract import Web3Provider
import asyncio
import config
import logging
import time
from concurrent.futures import as_completed, ThreadPoolExecutor
from web3.method import Method, default_root_munger, _apply_request_formatters
import web3
from web3.types import BlockIdentifier, ParityBlockTrace, RPCEndpoint, BlockData
from web3._utils.rpc_abi import RPC
from web3.module import apply_result_formatters
from web3.manager import RequestManager

from typing import Callable, List

from web3._utils.method_formatters import (
    get_error_formatters,
    get_null_result_formatters,
    get_request_formatters,
    get_result_formatters,
)



## MODEL FOR TEST
# logging.basicConfig(level=logging.DEBUG)

w3 = Web3Provider().get_web3_ws(config.PRC_WS)


def get_block_futer(w3, params):
    request_data = w3.provider.encode_rpc_request(
                            "eth_getBlockByNumber",
                            params)
    # print('request_data', request_data)

    futer = asyncio.run_coroutine_threadsafe(
                w3.provider.coro_make_request(request_data),
                w3.provider._loop)
    return futer



def result_forrmat(rpc: RPCEndpoint, params: list = [], result_raw_json: dict = {}):
    result_json =  RequestManager.formatted_response(result_raw_json, params)
    # TODO: by defult filter for extraData len 32 bytes
    if result_json.get('extraData'):
        result_json['extraData'] = result_json['extraData'][0:32]
    format = get_result_formatters(rpc, None)
    res = apply_result_formatters(format, result_json)
    return res


def get_blocks(block_start, block_end):
    params = [ [block_number, True] for block_number in range(block_start, block_end) ]
    futer_blocks = [get_block_futer(w3, param) for param in params ]
    blocks = [  result_forrmat(RPC.eth_getBlockByNumber, params[i], futer_block.result())for i, futer_block in enumerate(futer_blocks)]
    # blocks = []
    # for i, futer_block in enumerate(futer_blocks):
    #     block_raw = futer_block.result()
    #     # block = RequestManager.formatted_response(block_raw, params[i])
    #     block: BlockData = result_forrmat(RPC.eth_getBlockByNumber, params[i], block_raw)
    #     blocks.append(block)
    #     # print(dir(block), block.keys())
    #     # print(int(block['number'], 16), len(block['transactions']), params[i])

    print(len(blocks))
    # print(type(block))
    # for k  in block:
    #     print(k, type(block[k]))


    # res: BlockData = result_forrmat(RPC.eth_getBlockByNumber, block)
    # # res = w3.module.apply_result_formatters(result_format, block)
    # print(type(res), )
    # for k in res:
    #     print(k, type(res[k]))




def rewrite_w3():
    def coro_request(*args, **kwargs):
        print('hello form coro')
        return None
    w3.manager.coro_request = coro_request

    print(w3.manager.coro_request())



tik = time.time()
get_blocks(19714214, 19714214+200)
print('time:', time.time() - tik)

# method = Method(
#         RPC.eth_blockNumber,
#         mungers=None,)
# request, response_formatters = method.process_params({}, )
# print( method.process_params({}))
# print(method())
# rpc = RPC.eth_getBlockByNumber
# # print('rpc', rpc)
# # format = get_request_formatters(rpc)
# # # print(format, type(format))
# result_format = get_result_formatters(rpc, None)
# print(result_format)
# res = web3.module.apply_result_formatters(result_format, {'number':'0x12cd0a6'})

# # res = w3.eth.blockNumber
# print(res)

