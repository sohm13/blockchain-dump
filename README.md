examples:
    https://github.com/flashbots/mev-inspect-py
    https://github.com/blockchain-etl/ethereum-etl
        - https://medium.com/coinmonks/how-to-export-the-entire-ethereum-blockchain-to-csv-in-2-hours-for-10-69fef511e9a2
    https://www.tarlogic.com/blog/download-ethereum-blockchain/


_______________________
WEB3

get_transaction_receipt(tx_hash)
get_block(block_number) # Delegates to eth_getBlockByNumber


___________________________

____________

 db for read only
 banch save to db

 load EVM have 2 states: 
    1. Transaction result
    2. Transaction receipts (contain the result of such transactions: gas used, status (failed or successful) and logs generated.)
 load EVM data from Full archive node
______
