create table blocks
(
    timestamp timestamp,
    epoch_number bigint,
    height bigint,
    hash varchar(66),
    parent_hash varchar(66),
    nonce varchar(42),
    transactions_root varchar(66),
    deferred_state_root varchar(66),
    deferred_receipts_root varchar(66),
    deferred_logs_bloom_hash varchar(66),
    miner varchar(42),
    difficulty numeric(38),
    size bigint,
    gas_limit bigint,
    gas_used bigint,
    pow_quality numeric(38),
    adaptive boolean,
    blame boolean
);