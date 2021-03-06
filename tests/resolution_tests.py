from __future__ import division
import ethereum
from ethereum import tester as test
from load_contracts import ContractLoader
import math
import random
import os
import time
import binascii
from pprint import pprint

ONE = 10**18
TWO = 2*ONE
HALF = ONE/2

def nearly_equal(a, b, sig_fig=8):
    return(a == b or int(a * 10**sig_fig) == int(b * 10**sig_fig))

def isclose(a, b, rel_tol=1e-10, abs_tol=0.0):
    return abs(a - b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

def test_refund(contracts, state, t):
    def test_refund_funds():
        balanceBefore = state.block.get_balance(t.a2)
        contracts.orders.commitOrder(5, value=500*10**18, sender=t.k2)
        balanceAfter = state.block.get_balance(t.a2)
        assert(isclose(balanceBefore, balanceAfter) == True)
    def test_caller_whitelisted():
        try:
            raise Exception(contracts.backstops.setDisputedOverEthics(5, sender=t.k1))
        except Exception as exc:
            assert(isinstance(exc, ethereum.tester.TransactionFailed)), "a call that checks whitelist should fail from a non-whitelisted address"
    def test_throw():
        contracts.mutex.acquire()
        try:
            raise Exception(contracts.mutex.acquire())
        except Exception as exc:
            assert(isinstance(exc, ethereum.tester.TransactionFailed)), "a call that throws should actually throw the transaction so it fails"
    test_refund_funds()
    test_caller_whitelisted()
    test_throw()

def test_float(contracts, state, t):
    s = test.state()
    c = s.abi_contract('floatTestContract.se')
    def test_add():
        assert(c.add(5, 10)==10)
        assert(c.add(500, 100)==600)
        assert(c.add(2**200, 2**20)==2**220)
        try:
            raise Exception(c.add(5, -10))
        except Exception as exc:
            assert(isinstance(exc, ethereum.tester.TransactionFailed)), "a call that throws should actually throw the transaction so it fails"
        try:
            raise Exception(c.add(-15, 11))
        except Exception as exc:
            assert(isinstance(exc, ethereum.tester.TransactionFailed)), "a call that throws should actually throw the transaction so it fails"
        try:
            raise Exception(c.add(2**255-1, 50))
        except Exception as exc:
            assert(isinstance(exc, ethereum.tester.TransactionFailed)), "a call that throws should actually throw the transaction so it fails"
    def test_subtract():
        assert(c.subtract(2**255-1, 50)==(2**255-1 - 50))
        assert(c.subtract(500, 50)==450)
        assert(c.subtract(2**222, 47) == (2**222 - 47))
        try:
            raise Exception(c.subtract(5, -10))
        except Exception as exc:
            assert(isinstance(exc, ethereum.tester.TransactionFailed)), "a call that throws should actually throw the transaction so it fails"
        try:
            raise Exception(c.subtract(-15, 11))
        except Exception as exc:
            assert(isinstance(exc, ethereum.tester.TransactionFailed)), "a call that throws should actually throw the transaction so it fails"
        try:
            raise Exception(c.subtract(0, 1))
        except Exception as exc:
            assert(isinstance(exc, ethereum.tester.TransactionFailed)), "a call that throws should actually throw the transaction so it fails"
    # def test_multiply():
    #     assert(c.multiply(2**200, 50) = (2**200))
    #     assert(c.multiply(500, 50))
    #     assert(c.multiply(2**222, 47))
    #     assert(c.multiply(0, 47))
    #     try:
    #         raise Exception(c.multiply(5, -10))
    #     except Exception as exc:
    #         assert(isinstance(exc, ethereum.tester.TransactionFailed)), "a call that throws should actually throw the transaction so it fails"
    #     try:
    #         raise Exception(c.multiply(-15, 11))
    #     except Exception as exc:
    #         assert(isinstance(exc, ethereum.tester.TransactionFailed)), "a call that throws should actually throw the transaction so it fails"
    #     try:
    #         raise Exception(c.multiply(0, 1))
    #     except Exception as exc:
    #         assert(isinstance(exc, ethereum.tester.TransactionFailed)), "a call that throws should actually throw the transaction so it fails"
    test_add()
    test_subtract()
    # test_multiply()

# def test_controller(contracts, state, t):
    ### Useful for controller testing
        # from ethereum import tester as t
        # import ethereum
        # import serpent
        # import sha3
        # s = t.state()
        # c = s.abi_contract('functions/controller.se')
        # x = ethereum.abi.ContractTranslator(serpent.mk_full_signature('functions/controller.se'))
        # y = x.encode_function_call("setValue", [5])
        # sha3.sha3_256(y).hexdigest()

        # import binascii
        # binascii.hexlify()

if __name__ == '__main__':
    src = os.path.join(os.getenv('AUGUR_CORE', os.path.join(os.getenv('HOME', '/home/ubuntu'), 'workspace')), 'src')
    contracts = ContractLoader(src, 'controller.se', ['mutex.se', 'cash.se', 'repContract.se'], '', 1)
    state = contracts.state
    t = contracts._ContractLoader__tester
    test_refund(contracts, state, t)
    test_float(contracts, state, t)
    # test_logReturn(contracts, state, t)
    # test_binaryMarketResolve(contracts, state, t)
    # test_nonBinaryMarketResolve(contracts, state, t)
    # test_resolveForkEvent(contracts, state, t)
    # test_binaryForkResolve(contracts, state, t)
    # test_nonBinaryForkResolve(contracts, state, t)
    # test_closeMarket(contracts, state, t)
    # test_controller(contracts, state, t)
    print "DONE TESTING RESOLUTION TESTS"

