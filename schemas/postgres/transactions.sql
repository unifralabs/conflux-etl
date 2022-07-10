create table transactions
(
    hash varchar(66),
    nonce bigint,
    transaction_index bigint,
    from_address varchar(42),
    to_address varchar(42),
    value numeric(38),
    gas bigint,
    gas_price bigint,
    data text,
    status text,
    block_timestamp timestamp,
    epoch_number bigint,
    epoch_height bigint,
    chain_id text,
    block_hash varchar(66),
    contract_created varchar(66),
    storage_limit text,
    r text,
    s text,
    v text
);