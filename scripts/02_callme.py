from scripts.helpful_scripts import get_account
from brownie import (
    CallMeChallenge,
    network,
    Contract,
)


def main():
    print(network.show_active())
    # accounts
    account = get_account()
    print(f"account address: {account}")

    callme_address = "0x6922C21D166ADF620235C30A90DA565FD89C1AFB"

    callMe = Contract.from_abi(
        CallMeChallenge._name, callme_address, CallMeChallenge.abi
    )
    callMe.callme({"from": account})
