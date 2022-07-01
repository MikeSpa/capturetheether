from scripts.helpful_scripts import get_account, ONE
from brownie import (
    GuessTheSecretNumberChallenge,
    network,
    Contract,
)
from web3 import Web3


def main():
    print(network.show_active())
    # accounts
    account = get_account()
    print(f"account address: {account}")

    answerHash = "0xDB81B4D58595FBBBB592D3661A34CDCA14D7AB379441400CBFA1B78BC447C365"
    contract_address = "0x212DD11f7d6cE2a86d5F543E6741EF0C4Dd37F04"

    contract = Contract.from_abi(
        GuessTheSecretNumberChallenge._name,
        contract_address,
        GuessTheSecretNumberChallenge.abi,
    )

    # range of uint8
    for i in range(2 ** 8):
        # if the hash matches, guess the number
        if Web3.solidityKeccak(["uint8"], [i]).hex().upper() == answerHash.upper():
            contract.guess(i, {"from": account, "value": ONE})
