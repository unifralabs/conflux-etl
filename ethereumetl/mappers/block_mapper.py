# MIT License
#
# Copyright (c) 2018 Evgeny Medvedev, evge.medvedev@gmail.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the 'Software'), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


from ethereumetl.domain.block import CfxBlock
from ethereumetl.mappers.transaction_mapper import EthTransactionMapper
from ethereumetl.utils import hex_to_dec, to_normalized_address


class EthBlockMapper(object):
    def __init__(self, transaction_mapper=None):
        if transaction_mapper is None:
            self.transaction_mapper = EthTransactionMapper()
        else:
            self.transaction_mapper = transaction_mapper

    def json_dict_to_block(self, json_dict):
        block = CfxBlock()
        block.hash = json_dict.get('hash')
        block.height = hex_to_dec(json_dict.get('height'))
        block.miner = to_normalized_address(json_dict.get('miner'))
        block.nonce = json_dict.get('nonce')
        block.difficulty = hex_to_dec(json_dict.get('difficulty'))
        block.epoch_number = hex_to_dec(json_dict.get('epochNumber'))
        block.gas_limit = hex_to_dec(json_dict.get('gasLimit'))
        block.gas_used = hex_to_dec(json_dict.get('gasUsed'))
        block.deferred_logs_bloom_hash = json_dict['deferredLogsBloomHash']
        block.deferred_receipts_root = json_dict['deferredReceiptsRoot']
        block.deferred_state_root = json_dict['deferredStateRoot']
        block.transactions_root = json_dict.get('transactionsRoot')
        block.parent_hash = json_dict.get('parentHash')
        block.pow_quality = hex_to_dec(json_dict.get('powQuality'))
        block.size = hex_to_dec(json_dict.get('size'))
        block.timestamp = hex_to_dec(json_dict.get('timestamp'))
        block.adaptive = json_dict.get('adaptive')
        block.blame = json_dict.get('blame')
        block.referee_hashes = json_dict.get('refereeHashes')

        if 'transactions' in json_dict:
            block.transactions = [
                self.transaction_mapper.json_dict_to_transaction(
                    tx, block_timestamp=block.timestamp, epoch_number=block.epoch_number
                )
                for tx in json_dict['transactions']
                if isinstance(tx, dict)
            ]

            block.transaction_count = len(json_dict['transactions'])

        return block

    def block_to_dict(self, block):
        return {
            'type': 'block',
            'hash': block.hash,
            'height': block.height,
            'miner': block.miner,
            'nonce': block.nonce,
            'difficulty': block.difficulty,
            'epoch_number': block.epoch_number,
            'gas_limit': block.gas_limit,
            'gas_used': block.gas_used,
            'deferred_logs_bloom_hash': block.deferred_logs_bloom_hash,
            'deferred_receipts_root': block.deferred_receipts_root,
            'deferred_state_root': block.deferred_state_root,
            'transactions_root': block.transactions_root,
            'parent_hash': block.parent_hash,
            'pow_quality': block.pow_quality,
            'size': block.size,
            'timestamp': block.timestamp,
            'adaptive': block.adaptive,
            'blame': block.blame,
            'referee_hashes': block.referee_hashes,
        }
