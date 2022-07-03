from brownie import (
    accounts,
    config,
    network,
)
from web3 import Web3

POINT_ONE = Web3.toWei(0.1, "ether")
ONE = Web3.toWei(1, "ether")
TEN = Web3.toWei(10, "ether")
CENT = Web3.toWei(100, "ether")

FORKED_LOCAL_ENVIRNOMENT = ["mainnet-fork", "mainnet-fork2"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local", "hardhat"]


def get_account(index=None):
    if index:
        return accounts[index]
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRNOMENT
    ):
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])


def main():
    pass
