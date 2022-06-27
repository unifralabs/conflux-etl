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
import json

from blockchainetl.jobs.base_job import BaseJob
from ethereumetl.executors.batch_work_executor import BatchWorkExecutor
from ethereumetl.json_rpc_requests import generate_get_logs_json_rpc
from ethereumetl.mappers.receipt_log_mapper import CfxReceiptLogMapper
from ethereumetl.mappers.token_transfer_mapper import CfxTokenTransferMapper
from ethereumetl.service.token_transfer_extractor import (
    TRANSFER_EVENT_TOPIC, CfxTokenTransferExtractor)
from ethereumetl.utils import rpc_response_to_result, validate_range
from ethereumetl.web3_utils import make_request


class ExportTokenTransfersJob(BaseJob):
    def __init__(
            self,
            start_block,
            end_block,
            batch_size,
            web3,
            item_exporter,
            max_workers,
            tokens=None):
        validate_range(start_block, end_block)
        self.start_block = start_block
        self.end_block = end_block

        self.web3 = web3
        self.tokens = tokens
        self.item_exporter = item_exporter

        self.batch_work_executor = BatchWorkExecutor(batch_size, max_workers)

        self.receipt_log_mapper = CfxReceiptLogMapper()
        self.token_transfer_mapper = CfxTokenTransferMapper()
        self.token_transfer_extractor = CfxTokenTransferExtractor()

    def _start(self):
        self.item_exporter.open()

    def _export(self):
        self.batch_work_executor.execute(
            range(self.start_block, self.end_block + 1),
            self._export_batch,
            total_items=self.end_block - self.start_block + 1
        )

    def _export_batch(self, block_number_batch):
        assert len(block_number_batch) > 0

        address = None
        if self.tokens is not None and len(self.tokens) > 0:
            address = self.tokens

        logs_rpc = generate_get_logs_json_rpc(block_number_batch[0], block_number_batch[-1], [TRANSFER_EVENT_TOPIC], address) 
        response = make_request(self.web3, json.dumps(logs_rpc))
        events = rpc_response_to_result(response)
        
        for event in events:
            log = self.receipt_log_mapper.json_dict_to_receipt_log(event)
            token_transfer = self.token_transfer_extractor.extract_transfer_from_log(log)
            if token_transfer is not None:
                self.item_exporter.export_item(self.token_transfer_mapper.token_transfer_to_dict(token_transfer))

    def _end(self):
        self.batch_work_executor.shutdown()
        self.item_exporter.close()
