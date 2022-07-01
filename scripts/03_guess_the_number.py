from scripts.helpful_scripts import get_account, ONE
from brownie import (
    GuessTheNumberChallenge,
    network,
    Contract,
)


def main():
    print(network.show_active())
    # accounts
    account = get_account()
    print(f"account address: {account}")

    contract_address = "0x86c65403d0cF218e5563399B4349eB0f5A92B317"

    contract = Contract.from_abi(
        GuessTheNumberChallenge._name,
        contract_address,
        GuessTheNumberChallenge.abi,
    )
    contract.guess(42, {"from": account, "value": ONE})
