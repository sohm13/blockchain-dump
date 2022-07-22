from typing import List, Optional
from dataclasses import dataclass

@dataclass
class Block:
    block_number: int
    timestamp: int
    miner: str
    nonce: str
    size: int
    difficulty: int
    gas_limit: int
    gas_used: int
    hash: str
    state_root: str
    logs_bloom: str


@dataclass
class Transaction:
    block_hash: str # '0x4e3a3754410177e6937ef1f84bba68ea139e8d1a2258c5f85db9f1cd715a1bdd'
    block_number: int # 46147
    address_from: str #'0xA1E4380A3B1f749673E270229993eE55F35663b4'
    gas: int #21000
    gas_price: Optional[int] #None
    hash: str # '0x5c504ed432cb51138bcf09aa5e8a410dd4a1e204ef84bfed1be16dfba1b22060'
    input: str # '0x'
    nonce: int #0
    address_to: str #'0x5DF9B87991262F6BA471F09758CDE1c0FC1De734'
    transactionIndex: int #0
    value: int #31337


@dataclass
class TransactionReceipt:
    transaction_hash: str #hex_string
    transaction_index: int #bigint
    block_number: int  #bigint
    gas_used: int	#bigint
    contract_address: str #address
    status:	int #bigint
    address_from: str
    address_to: str

@dataclass
class TransactionLog:
    log_index:	int
    transaction_hash:	str
    transaction_index:	int
    block_hash:	str
    block_number:	int
    address:	str
    data:	str
    topics:	str