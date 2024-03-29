# MIT License
#
# Copyright (c) 2018 Evgeny Medvedev, evge.medvedev@gmail.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


def generate_get_block_by_epoch_number_json_rpc(block_numbers, include_transactions):
    for idx, block_number in enumerate(block_numbers):
        yield generate_json_rpc(method='cfx_getBlockByEpochNumber', params=[hex(block_number), include_transactions], request_id=idx)


def generate_get_blocks_by_epoch_json_rpc(block_numbers):
    for idx, block_number in enumerate(block_numbers):
        yield generate_json_rpc(method='cfx_getBlocksByEpoch', params=[hex(block_number)], request_id=idx)


def generate_get_block_by_hash_json_rpc(block_hashes, include_transactions):
    for idx, block_hash in enumerate(block_hashes):
        yield generate_json_rpc(method='cfx_getBlockByHash', params=[block_hash, include_transactions], request_id=idx)


def generate_get_receipt_json_rpc(transaction_hashes):
    for idx, transaction_hash in enumerate(transaction_hashes):
        yield generate_json_rpc(method='cfx_getTransactionReceipt', params=[transaction_hash], request_id=idx)


def generate_get_code_json_rpc(contract_addresses, block='latest_state'):
    for idx, contract_address in enumerate(contract_addresses):
        yield generate_json_rpc(
            method='cfx_getCode', params=[contract_address, hex(block) if isinstance(block, int) else block], request_id=idx
        )


def generate_get_logs_by_block_ranges_json_rpc(block_ranges, topics=None, address=None):
    for idx, block_range in enumerate(block_ranges):
        yield generate_json_rpc(
            method='cfx_getLogs',
            params=[
                {
                    'fromEpoch': hex(block_range[0]),
                    'toEpoch': hex(block_range[1]),
                    'topics': topics,
                    'address': address,
                }
            ],
            request_id=idx,
        )


def generate_get_logs_json_rpc(from_epoch, to_epoch, topics, address=None):
    return generate_json_rpc(
        method='cfx_getLogs',
        params=[
            {
                'fromEpoch': hex(from_epoch),
                'toEpoch': hex(to_epoch),
                'topics': topics,
                'address': address,
            }
        ],
        request_id=1,
    )


def generate_json_rpc(method, params, request_id=1):
    return {
        'jsonrpc': '2.0',
        'method': method,
        'params': params,
        'id': request_id,
    }
