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

from conflux import Conflux
from web3._utils.request import make_post_request
from web3.middleware import geth_poa_middleware


def build_web3(provider):
    return Conflux(provider)

def make_request(provider, text):
    provider.logger.debug("Making request HTTP. URI: %s, Request: %s",
                        provider.endpoint_uri, text)
    request_data = text.encode('utf-8')
    raw_response = make_post_request(
        provider.endpoint_uri,
        request_data,
        **provider.get_request_kwargs()
    )
    response = provider.decode_rpc_response(raw_response)
    provider.logger.debug("Getting response HTTP. URI: %s, "
                        "Request: %s, Response: %s",
                        provider.endpoint_uri, text, response)
    return response
