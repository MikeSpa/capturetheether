# Capture The Ether


# WRITEUP

## 2) Call Me

Pretty simple, you just call the function `callMe()`.

## 3) Choose a nickname

Again the challenge is simple, you call the function `setNickame()` with your nickname.
2 subtilities:
- One, you need to call `setNickname()` on the CaptureTheEther contract at address `0x71c46Ed333C35e4E6c62D32dc7C8F00D125b4fee` and not the address given on the left.
- Two, you need to be sure to encode your nickname correctly. The contract check the leftmost character to see if its 0 or not so you need to be sure that your nickname is save as 0xYOURNICKNAMEINHEX00000000000000000000...0 instead of 0x00000000000000000000...0YOURNICKNAMEINHEX.

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