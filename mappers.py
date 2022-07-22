import re
from web3.types import BlockData, TxData, TxReceipt, LogReceipt
from schemas import (
    Block,
    Transaction,
    TransactionReceipt,
    TransactionLog
)


def block_data_to_block_schema(block_data: BlockData):
    return Block(
        block_number = block_data.number,
        timestamp = block_data.timestamp,
        miner = block_data.miner,
        nonce = block_data.nonce,
        size = block_data.size,
        difficulty = block_data.difficulty,
        gas_limit = block_data.gasLimit,
        gas_used = block_data.gasUsed,
        hash = block_data.hash,
        state_root = block_data.stateRoot,
        logs_bloom = block_data.logsBloom
    )

def block_tx_data_to_transaction_schema( tx_data: TxData):
    return Transaction(
        block_hash = tx_data.blockHash,
        block_number = tx_data.blockNumber,
        address_from = tx_data['from'],
        gas = tx_data.gas,
        gas_price= tx_data.gasPrice,
        hash = tx_data.hash,
        input = tx_data.input,
        nonce = tx_data.nonce,
        address_to = tx_data.to,
        transactionIndex = tx_data.transactionIndex,
        value = tx_data.value
    )

def receipt_tx_to_receipt_schema(tx_receipt: TxReceipt):
    return TransactionReceipt(
        transaction_hash = tx_receipt.transactionHash,
        transaction_index =  tx_receipt.transactionIndex,
        block_number = tx_receipt.blockNumber,
        gas_used = tx_receipt.gasUsed,
        contract_address = tx_receipt.contractAddress,
        status = tx_receipt.status,
        address_from =  tx_receipt['from'],
        address_to = tx_receipt.to
    )

def receipt_log_to_log_receipt_schema(log_receipt: LogReceipt):

    return TransactionLog(
        log_index = log_receipt.logIndex,
        transaction_hash = log_receipt.transactionHash,
        transaction_index = log_receipt.transactionIndex,
        block_hash = log_receipt.blockHash,
        block_number = log_receipt.blockNumber,
        address = log_receipt.address,
        data = log_receipt.data,
        topics = log_receipt.topics,
    )