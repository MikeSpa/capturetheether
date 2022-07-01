from scripts.helpful_scripts import get_account
from brownie import (
    CaptureTheEther,
    NicknameChallenge,
    network,
    Contract,
)


def main():
    print(network.show_active())
    # accounts
    account = get_account()
    print(f"account address: {account}")

    # Choose your nickname
    nickname = "MikeSpa".encode().hex()
    print(nickname)
    nickname_len = len(nickname)
    print(nickname_len)
    # Since the contract check the first character (leftmost character), you need to order the 0x string in the right way
    # i.e. 0xYOURNICKNAMEINHEX00000000000000000000...0 instead of 0x00000000000000000000...0YOURNICKNAMEINHEX which get returned by str.encode().hex()
    # a 32 bytes hey string has 64 character so you add x 0 with x = 64-  number of character already taken by your name
    nickname = "0x" + nickname + "0" * (64 - nickname_len)
    print(nickname)

    CaptureTheEther_contract_address = "0x71c46Ed333C35e4E6c62D32dc7C8F00D125b4fee"

    contract = Contract.from_abi(
        CaptureTheEther._name, CaptureTheEther_contract_address, CaptureTheEther.abi
    )
    contract.setNickname(nickname, {"from": account})

    # Check your nickname
    # nickname_challenge_contract_address = (
    #     "0xDB76818fBB587faC6e3caf0FB200BB3Aebd98DcF"  # add your contract address
    # )
    # nickname_contract = Contract.from_abi(
    #     NicknameChallenge._name,
    #     nickname_challenge_contract_address,
    #     NicknameChallenge.abi,
    # )
    # print(contract.nicknameOf(account))
    # print(nickname_contract.isComplete())
