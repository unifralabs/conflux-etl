# Conflux ETL

[![Discord](https://img.shields.io/badge/discord-join%20chat-blue.svg)](https://discord.gg/erww7xrffc)

Conflux ETL is a tool for extracting data from the Conflux blockchain and loading it into a datastore.

It's a fork of the [ethereum-etl](https://github.com/blockchain-etl/ethereum-etl) project.

Supported instructions:

- export_blocks_and_transactions
- export_token_transfers
- export_receipts_and_logs
- export_contracts
- export_tokens
- export_logs
- extract_csv_column
- get_block_range_for_date
- get_keccak_hash

Supported data outputs:

- Console
- CSV files

Welcome to contribute to the project by submitting a pull request.

---

[Full documentation available here](http://ethereum-etl.readthedocs.io/).

## Quickstart

Install Ethereum ETL:

```bash
pip3 install .
```

Export blocks and transactions ([Schema](docs/schema.md#blockscsv), [Reference](docs/commands.md#export_blocks_and_transactions)):

```bash
> ethereumetl export_blocks_and_transactions --start-block 0 --end-block 500000 \
--blocks-output blocks.csv --transactions-output transactions.csv \
--provider-uri https://conflux-core-public.unifra.io
```

Export ERC20 and ERC721 transfers ([Schema](docs/schema.md#token_transferscsv), [Reference](docs/commands.md##export_token_transfers)):

```bash
> ethereumetl export_token_transfers --start-block 0 --end-block 500000 \
--provider-uri https://conflux-core-public.unifra.io --output token_transfers.csv
```

---

Stream blocks, transactions, logs, token_transfers continually to console ([Reference](docs/commands.md#stream)):

```bash
> pip3 install ethereum-etl[streaming]
> ethereumetl stream --start-block 500000 -e block,transaction,log,token_transfer --log-file log.txt \
--provider-uri https://conflux-core-public.unifra.io
```

Find other commands [here](https://ethereum-etl.readthedocs.io/en/latest/commands/).

For the latest version, check out the repo and call

```bash
> pip3 install -e .
> python3 ethereumetl.py
```

## Useful Links

- [Schema](https://ethereum-etl.readthedocs.io/en/latest/schema/)
- [Command Reference](https://ethereum-etl.readthedocs.io/en/latest/commands/)
- [Documentation](https://ethereum-etl.readthedocs.io/)
- [Public Datasets in BigQuery](https://github.com/blockchain-etl/public-datasets)
- [Exporting the Blockchain](https://ethereum-etl.readthedocs.io/en/latest/exporting-the-blockchain/)
- [Querying in Amazon Athena](https://ethereum-etl.readthedocs.io/en/latest/amazon-athena/)
- [Querying in Google BigQuery](https://ethereum-etl.readthedocs.io/en/latest/google-bigquery/)
- [Querying in Kaggle](https://www.kaggle.com/bigquery/ethereum-blockchain)
- [Airflow DAGs](https://github.com/blockchain-etl/ethereum-etl-airflow)
- [Postgres ETL](https://github.com/blockchain-etl/ethereum-etl-postgresql)
- [Ethereum 2.0 ETL](https://github.com/blockchain-etl/ethereum2-etl)

## Running Tests

```bash
> pip3 install -e .[dev,streaming]
> export ETHEREUM_ETL_RUN_SLOW_TESTS=True
> export PROVIDER_URL=<your_porvider_uri>
> pytest -vv
```

### Running Tox Tests

```bash
> pip3 install tox
> tox
```

## Running in Docker

1.  Install Docker: https://docs.docker.com/get-docker/

2.  Build a docker image > docker build -t ethereum-etl:latest . > docker image ls
3.  Run a container out of the image

        > docker run -v $HOME/output:/ethereum-etl/output ethereum-etl:latest export_all -s 0 -e 5499999 -b 100000 -p https://conflux-core-public.unifra.io
        > docker run -v $HOME/output:/ethereum-etl/output ethereum-etl:latest export_all -s 2018-01-01 -e 2018-01-01 -p https://conflux-core-public.unifra.io

4.  Run streaming to console or Pub/Sub

        > docker build -t ethereum-etl:latest .
        > echo "Stream to console"
        > docker run ethereum-etl:latest stream --start-block 500000 --log-file log.txt
        > echo "Stream to Pub/Sub"
        > docker run -v /path_to_credentials_file/:/ethereum-etl/ --env GOOGLE_APPLICATION_CREDENTIALS=/ethereum-etl/credentials_file.json ethereum-etl:latest stream --start-block 500000 --output projects/<your-project>/topics/crypto_ethereum

If running on Apple M1 chip add the `--platform linux/x86_64` option to the `build` and `run` commands e.g.:

```
docker build --platform linux/x86_64 -t ethereum-etl:latest .
docker run --platform linux/x86_64 ethereum-etl:latest stream --start-block 500000
```

## Projects using Ethereum ETL

- [Google](https://goo.gl/oY5BCQ) - Public BigQuery Ethereum datasets
- [Nansen](https://www.nansen.ai/?ref=ethereumetl) - Analytics platform for Ethereum
