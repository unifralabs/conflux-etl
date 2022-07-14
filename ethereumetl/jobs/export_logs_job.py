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
import logging
from logging import info

from blockchainetl.jobs.base_job import BaseJob
from ethereumetl.executors.batch_work_executor import BatchWorkExecutor
from ethereumetl.json_rpc_requests import generate_get_logs_by_block_ranges_json_rpc
from ethereumetl.mappers.receipt_log_mapper import CfxReceiptLogMapper
from ethereumetl.utils import rpc_response_batch_to_results, validate_range
from ethereumetl.web3_utils import make_request


# Exports logs
class ExportLogsJob(BaseJob):
    def __init__(self, start_block, end_block, batch_size, span, web3_provider, max_workers, item_exporter, export_logs=True):
        validate_range(start_block, end_block)
        self.start_block = start_block
        self.end_block = end_block
        self.web3_provider = web3_provider
        self.span = span

        self.batch_size = batch_size
        self.batch_work_executor = BatchWorkExecutor(batch_size, max_workers)
        self.item_exporter = item_exporter

        self.export_logs = export_logs
        if not self.export_logs:
            raise ValueError('At least export_logs must be True')

        self.receipt_log_mapper = CfxReceiptLogMapper()

    def _start(self):
        self.item_exporter.open()

    def _export(self):
        block_ranges = []
        pivot_block = self.start_block
        while pivot_block <= self.end_block:
            block_ranges.append([pivot_block, pivot_block + self.span])
            pivot_block += self.span + 1
        # reset the last block range to end_block
        block_ranges[-1][1] = self.end_block

        self.batch_work_executor.execute(iter(block_ranges), self._export_logs, total_items=self.end_block - self.start_block)

    def _export_logs(self, block_ranges):
        logging.info('Exporting logs for block ranges: %s', block_ranges)
        logs_rpc = list(generate_get_logs_by_block_ranges_json_rpc(block_ranges))
        response = make_request(self.web3_provider, json.dumps(logs_rpc))
        results = rpc_response_batch_to_results(response)
        logs = []
        for result in results:
            if not result:
                continue
            logs.extend(self.receipt_log_mapper.json_dict_to_receipt_log(log) for log in result)
        for log in logs:
            self.item_exporter.export_item(self.receipt_log_mapper.log_to_dict(log))

    def _end(self):
        self.batch_work_executor.shutdown()
        self.item_exporter.close()
