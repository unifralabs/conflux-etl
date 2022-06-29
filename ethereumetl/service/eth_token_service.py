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
import logging

from ethereumetl.domain.token import CfxToken
from ethereumetl.erc20_abi import ERC20_ABI, ERC20_ABI_ALTERNATIVE_1
from web3.exceptions import BadFunctionCallOutput

logger = logging.getLogger('eth_token_service')


class CfxTokenService(object):
    def __init__(self, web3, function_call_result_transformer=None):
        self._web3 = web3
        self._function_call_result_transformer = function_call_result_transformer

    def get_token(self, token_address):
        symbol = self._get_first_result(
            CfxContractFunc(token_address, ERC20_ABI, 'symbol'),
            CfxContractFunc(token_address, ERC20_ABI, 'SYMBOL'),
            CfxContractFunc(token_address, ERC20_ABI_ALTERNATIVE_1, 'symbol'),
            CfxContractFunc(token_address, ERC20_ABI_ALTERNATIVE_1, 'SYMBOL'),
        )
        if isinstance(symbol, bytes):
            symbol = self._bytes_to_string(symbol)

        name = self._get_first_result(
            CfxContractFunc(token_address, ERC20_ABI, 'name'),
            CfxContractFunc(token_address, ERC20_ABI, 'NAME'),
            CfxContractFunc(token_address, ERC20_ABI_ALTERNATIVE_1, 'name'),
            CfxContractFunc(token_address, ERC20_ABI_ALTERNATIVE_1, 'NAME'),
        )
        
        if isinstance(name, bytes):
            name = self._bytes_to_string(name)

        decimals = self._get_first_result(
            CfxContractFunc(token_address, ERC20_ABI, 'decimals'),
            CfxContractFunc(token_address, ERC20_ABI, 'DECIMALS'),
        )
        total_supply = self._get_first_result(CfxContractFunc(token_address, ERC20_ABI, 'totalSupply'))

        token = CfxToken()
        token.address = token_address
        token.symbol = symbol
        token.name = name
        token.decimals = decimals
        token.total_supply = total_supply

        return token

    def _get_first_result(self, *funcs):
        for func in funcs:
            result = self._call_contract_function(func)
            if result is not None:
                return result
        return None

    def _call_contract_function(self, func):
        # BadFunctionCallOutput exception happens if the token doesn't implement a particular function
        # or was self-destructed
        # OverflowError exception happens if the return type of the function doesn't match the expected type
        result = self.call_contract_function(
            func=func,
            ignore_errors=(BadFunctionCallOutput, OverflowError, ValueError),
            default_value=None)

        if self._function_call_result_transformer is not None:
            return self._function_call_result_transformer(result)
        else:
            return result

    def call_contract_function(self, func, ignore_errors, default_value=None):
        try:
            result = self._web3.call_contract_method(func.contract_address, func.contract_abi, func.name)
            return result
        except Exception as ex:
            if type(ex) in ignore_errors:
                logger.debug('An exception occurred in function {} of contract {}. '.format(func.name, func.contract_address)
                                + 'This exception can be safely ignored.', exc_info=True)
                return default_value
            else:
                raise ex

    def _bytes_to_string(self, b, ignore_errors=True):
        if b is None:
            return b

        try:
            b = b.decode('utf-8')
        except UnicodeDecodeError as e:
            if ignore_errors:
                logger.debug('A UnicodeDecodeError exception occurred while trying to decode bytes to string', exc_info=True)
                b = None
            else:
                raise e

        if self._function_call_result_transformer is not None:
            b = self._function_call_result_transformer(b)
        return b


class CfxContractFunc():
    def __init__(self, contract_address, contract_abi, name):
        self.contract_address = contract_address
        self.contract_abi = contract_abi
        self.name = name
