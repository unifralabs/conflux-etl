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


from ethereumetl.domain.receipt import CfxReceipt
from ethereumetl.mappers.receipt_log_mapper import CfxReceiptLogMapper
from ethereumetl.utils import hex_to_dec, to_normalized_address


class CfxReceiptMapper(object):
    def __init__(self, receipt_log_mapper=None):
        if receipt_log_mapper is None:
            self.receipt_log_mapper = CfxReceiptLogMapper()
        else:
            self.receipt_log_mapper = receipt_log_mapper

    def json_dict_to_receipt(self, json_dict):
        receipt = CfxReceipt()

        receipt.transaction_hash = json_dict.get('transactionHash')
        receipt.index= hex_to_dec(json_dict.get('index'))
        receipt.block_hash = json_dict.get('blockHash')
        receipt.epoch_number = hex_to_dec(json_dict.get('epochNumber'))
        receipt.from_address = to_normalized_address(json_dict.get('from'))
        receipt.to_address = to_normalized_address(json_dict.get('to'))
        receipt.gas_used = hex_to_dec(json_dict.get('gasUsed'))
        receipt.gas_fee = hex_to_dec(json_dict.get('gasFee'))
        receipt.gas_covered_by_sponsor = json_dict.get('gasCoveredBySponsor')
        receipt.storage_collateralized = hex_to_dec(json_dict.get('storageCollateralized'))
        receipt.storage_covered_by_sponsor = json_dict.get('storageCoveredBySponsor')
        receipt.storage_released = json_dict.get('storageReleased')
        receipt.contract_created = to_normalized_address(json_dict.get('contractCreated'))
        receipt.state_root = json_dict.get('stateRoot')
        receipt.outcome_status = json_dict.get('outcomeStatus')
        receipt.logs_bloom = json_dict.get('logsBloom')

        if 'logs' in json_dict:
            receipt.logs = [
                self.receipt_log_mapper.json_dict_to_receipt_log(log) for log in json_dict['logs']
            ]

        return receipt

    def receipt_to_dict(self, receipt):
        return {
            'type': 'receipt',
            'transaction_hash': receipt.transaction_hash,
            'index': receipt.index,
            'block_hash': receipt.block_hash,
            'epoch_number': receipt.epoch_number,
            'from_address': receipt.from_address,
            'to_address': receipt.to_address,
            'gas_used': receipt.gas_used,
            'gas_fee': receipt.gas_fee,
            'gas_covered_by_sponsor': receipt.gas_covered_by_sponsor,
            'storage_collateralized': receipt.storage_collateralized,
            'storage_covered_by_sponsor': receipt.storage_covered_by_sponsor,
            'storage_released': receipt.storage_released,
            'contract_created': receipt.contract_created,
            'state_root': receipt.state_root,
            'outcome_status': receipt.outcome_status,
            'logs_bloom': receipt.logs_bloom,
        }
