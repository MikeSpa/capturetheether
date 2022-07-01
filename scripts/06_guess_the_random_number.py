from scripts.helpful_scripts import get_account, ONE
from brownie import GuessTheRandomNumberChallenge, network, Contract, config
from web3 import Web3

INFURA_KEY = config["infura"]["infura_key"]
w3 = Web3(Web3.HTTPProvider("https://ropsten.infura.io/v3/" + INFURA_KEY))


def main():
    print(network.show_active())
    # accounts
    account = get_account()
    print(f"account address: {account}")

    contract_address = "0x15a9B86036c691b8067Cde5de25a0d21F8B02994"

    contract = Contract.from_abi(
        GuessTheRandomNumberChallenge._name,
        contract_address,
        GuessTheRandomNumberChallenge.abi,
    )
    # convert form bytes to hex to base 10
    answer = int(w3.eth.get_storage_at(contract_address, 0).hex(), base=16)
    contract.guess(answer, {"from": account, "value": ONE})
