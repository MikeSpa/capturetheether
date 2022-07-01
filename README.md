# Capture The Ether


# WRITEUP

## 1) Call Me

Pretty simple, you just call the function `callMe()`.

## 2) Choose a nickname

Again the challenge is simple, you call the function `setNickame()` with your nickname.
2 subtilities:
- One, you need to call `setNickname()` on the CaptureTheEther contract at address `0x71c46Ed333C35e4E6c62D32dc7C8F00D125b4fee` and not the address given on the left.
- Two, you need to be sure to encode your nickname correctly. The contract check the leftmost character to see if its 0 or not so you need to be sure that your nickname is save as 0xYOURNICKNAMEINHEX00000000000000000000...0 instead of 0x00000000000000000000...0YOURNICKNAMEINHEX.