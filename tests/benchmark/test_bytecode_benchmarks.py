"""
Benchmark test cases.

These test cases are designed to act as simple benchmarks of EVM compiler and
interpreter implementation performance; they are implemented directly as bytecode.
"""

import pytest

from ethereum_test_tools import (
    Address,
    Alloc,
    Environment,
    StateTestFiller,
    Transaction,
)
from ethereum_test_tools.vm.opcode import Opcodes as Op


@pytest.mark.valid_from("Shanghai")
def test_counting_loop(
    state_test: StateTestFiller,
    env: Environment,
    pre: Alloc,
    post: Alloc,
    sender: Address,
):
    """Benchmark a simple loop that just counts up to 0x010000."""
    contract_code = (
        Op.MSTORE(Op.PUSH0, Op.PUSH3(0x010000))
        + Op.PUSH0()
        + Op.JUMPDEST()
        + Op.PUSH1(0x01)
        + Op.ADD(unchecked=True)
        + Op.JUMPI(Op.PUSH1(0x07), Op.ISZERO(Op.EQ(Op.MLOAD(Op.PUSH0), Op.DUP1())))
    )
    contract_address = pre.deploy_contract(contract_code)

    tx = Transaction(
        ty=0x0,
        chain_id=0x01,
        nonce=0,
        to=contract_address,
        gas_limit=100000000,
        gas_price=10,
        sender=sender,
    )

    state_test(
        env=env,
        pre=pre,
        post=post,
        tx=tx,
        tag="benchmark_loop_count",
    )
