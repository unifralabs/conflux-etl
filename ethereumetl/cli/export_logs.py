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


from email.policy import default

import click
from blockchainetl.logging_utils import logging_basic_config
from ethereumetl.jobs.export_logs_job import ExportLogsJob
from ethereumetl.jobs.exporters.logs_item_exporter import logs_item_exporter
from ethereumetl.providers.auto import get_provider_from_uri
from ethereumetl.thread_local_proxy import ThreadLocalProxy
from ethereumetl.utils import check_classic_provider_uri

logging_basic_config()


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option('-s', '--start-block', default=0, show_default=True, type=int, help='Start block')
@click.option('-e', '--end-block', required=True, type=int, help='End block')
@click.option('-b', '--batch-size', default=10, show_default=True, type=int, help='The number of logs to export at a time.')
@click.option('--span', default=100, show_default=True, type=int, help='The range of cfx_getLogs to query at a time.')
@click.option(
    '-p',
    '--provider-uri',
    default='https://main.confluxrpc.com',
    show_default=True,
    type=str,
    help='The URI of the web3 provider e.g. ' 'https://main.confluxrpc.com',
)
@click.option('-w', '--max-workers', default=5, show_default=True, type=int, help='The maximum number of workers.')
@click.option(
    '--logs-output',
    default=None,
    show_default=True,
    type=str,
    help='The output file for logs. ' 'If not provided logs will not be exported. Use "-" for stdout',
)
def export_logs(start_block, end_block, batch_size, span, provider_uri, max_workers, logs_output):
    """Exports logs."""
    if logs_output is None:
        raise ValueError('--logs_output options must be provided')
    job = ExportLogsJob(
        start_block=start_block,
        end_block=end_block,
        batch_size=batch_size,
        span=span,
        web3_provider=ThreadLocalProxy(lambda: get_provider_from_uri(provider_uri, batch=False)),
        max_workers=max_workers,
        item_exporter=logs_item_exporter(logs_output),
        export_logs=logs_output is not None,
    )

    job.run()
