#  MIT License
#
#  Copyright (c) 2020 Evgeny Medvedev, evge.medvedev@gmail.com
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

from sqlalchemy import (
    TIMESTAMP,
    VARCHAR,
    BigInteger,
    Boolean,
    Column,
    Integer,
    MetaData,
    Numeric,
    PrimaryKeyConstraint,
    String,
    Table,
)
from sqlalchemy.dialects.postgresql import ARRAY

metadata = MetaData()

# SQL schema is here https://github.com/blockchain-etl/ethereum-etl-postgres/tree/master/schema

BLOCKS = Table(
    'blocks',
    metadata,
    Column('timestamp', TIMESTAMP),
    Column('epoch_number', BigInteger),
    Column('height', BigInteger),
    Column('hash', String, primary_key=True),
    Column('parent_hash', String),
    Column('nonce', String),
    Column('transactions_root', String),
    Column('deferred_state_root', String),
    Column('deferred_receipts_root', String),
    Column('deferred_logs_bloom_hash', String),
    Column('miner', String),
    Column('difficulty', Numeric(38)),
    Column('size', BigInteger),
    Column('gas_limit', BigInteger),
    Column('gas_used', BigInteger),
    Column('pow_quality', Numeric(38)),
    Column('adaptive', Boolean),
    Column('blame', Boolean),
)

TRANSACTIONS = Table(
    'transactions',
    metadata,
    Column('hash', String, primary_key=True),
    Column('nonce', BigInteger),
    Column('transaction_index', BigInteger),
    Column('from_address', String),
    Column('to_address', String),
    Column('value', Numeric(38)),
    Column('gas', BigInteger),
    Column('gas_price', BigInteger),
    Column('data', String),
    Column('status', String),  # TODO: udpate status to numeric
    Column('block_timestamp', TIMESTAMP),
    Column('epoch_number', BigInteger),
    Column('epoch_height', BigInteger),
    Column('block_hash', String),
    Column('chain_id', String),  # TODO: update chain_id to numeric
    Column('contract_created', String),
    Column('storage_limit', String),  # TODO: update storage_limit to numeric
    Column('r', String),
    Column('s', String),
    Column('v', String),
)

LOGS = Table(
    'logs',
    metadata,
    Column('log_index', BigInteger, primary_key=True),
    Column('transaction_log_index', BigInteger),
    Column('transaction_hash', String, primary_key=True),
    Column('transaction_index', BigInteger),
    Column('address', String),
    Column('data', String),
    Column('topic0', String),
    Column('topic1', String),
    Column('topic2', String),
    Column('topic3', String),
    Column('epoch_number', BigInteger),
    Column('block_hash', String),
)

TOKEN_TRANSFERS = Table(
    'token_transfers',
    metadata,
    Column('token_address', String),
    Column('from_address', String),
    Column('to_address', String),
    Column('value', Numeric(78)),
    Column('transaction_hash', String, primary_key=True),
    Column('log_index', BigInteger, primary_key=True),
    Column('epoch_number', BigInteger),
    Column('block_hash', String),
)

TOKENS = Table(
    'tokens',
    metadata,
    Column('address', VARCHAR(42)),
    Column('name', String),
    Column('symbol', String),
    Column('decimals', Integer),
    Column('function_sighashes', ARRAY(String)),
    Column('total_supply', Numeric(78)),
    Column('epoch_number', BigInteger),
    PrimaryKeyConstraint('address', 'epoch_number', name='tokens_pk'),
)

CONTRACTS = Table(
    'contracts',
    metadata,
    Column('address', VARCHAR(42)),
    Column('bytecode', String),
    Column('function_sighashes', ARRAY(String)),
    Column('is_erc20', Boolean),
    Column('is_erc721', Boolean),
    Column('epoch_number', BigInteger),
    PrimaryKeyConstraint('address', 'epoch_number', name='contracts_pk'),
)
