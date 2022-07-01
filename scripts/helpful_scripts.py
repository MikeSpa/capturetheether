from brownie import (
    accounts,
    config,
)
from web3 import Web3

POINT_ONE = Web3.toWei(0.1, "ether")
ONE = Web3.toWei(1, "ether")
TEN = Web3.toWei(10, "ether")
CENT = Web3.toWei(100, "ether")


def get_account(index=None):
    if index:
        return accounts[index]
    return accounts.add(config["wallets"]["from_key"])


def main():
    pass
