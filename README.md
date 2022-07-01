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