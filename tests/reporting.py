import os
from ethereum import tester

contracts = ContractLoader('src', 'controller.se', ['mutex.se', 'cash.se', 'repContract.se'], '', 1)

def test():
    assert(contracts.controller.ok() == 1), "controller.ok did not return 1"

if __name__ == '__main__':
    test()
