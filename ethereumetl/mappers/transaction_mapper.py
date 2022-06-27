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


from ethereumetl.domain.transaction import CfxTransaction
from ethereumetl.utils import hex_to_dec, to_normalized_address


class EthTransactionMapper(object):
    def json_dict_to_transaction(self, json_dict, **kwargs):
        transaction = CfxTransaction()
        transaction.hash = json_dict.get('hash')
        transaction.nonce = hex_to_dec(json_dict.get('nonce'))
        transaction.block_hash = json_dict.get('blockHash')
        transaction.epoch_number = kwargs.get('epoch_number')
        transaction.epoch_height = hex_to_dec(json_dict.get('epochHeight'))
        transaction.block_timestamp = kwargs.get('block_timestamp')
        transaction.chain_id = json_dict.get('chainId')
        transaction.contract_created = json_dict.get('contractCreated')
        transaction.transaction_index = hex_to_dec(json_dict.get('transactionIndex'))
        transaction.from_address = to_normalized_address(json_dict.get('from'))
        transaction.to_address = to_normalized_address(json_dict.get('to'))
        transaction.value = hex_to_dec(json_dict.get('value'))
        transaction.gas = hex_to_dec(json_dict.get('gas'))
        transaction.gas_price = hex_to_dec(json_dict.get('gasPrice'))
        transaction.data = json_dict.get('input')
        transaction.status = json_dict.get('status')
        transaction.storage_limit = hex_to_dec(json_dict.get('storageLimit'))
        transaction.r = json_dict.get('r')
        transaction.s = json_dict.get('s')
        transaction.v = hex_to_dec(json_dict.get('v'))
        return transaction

    def transaction_to_dict(self, transaction):
        return {
            'type': 'transaction',
            'hash': transaction.hash,
            'nonce': transaction.nonce,
            'block_hash': transaction.block_hash,
            'epoch_number': transaction.epoch_number,
            'epoch_height': transaction.epoch_height,
            'block_timestamp': transaction.block_timestamp,
            'chain_id': transaction.chain_id,
            'contract_created': transaction.contract_created,
            'transaction_index': transaction.transaction_index,
            'from_address': transaction.from_address,
            'to_address': transaction.to_address,
            'value': transaction.value,
            'gas': transaction.gas,
            'gas_price': transaction.gas_price,
            'data': transaction.data,
            'status': transaction.status,
            'storage_limit': transaction.storage_limit,
            'r': transaction.r,
            's': transaction.s,
            'v': transaction.v,
        }
