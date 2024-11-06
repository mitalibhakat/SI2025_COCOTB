import cocotb
from cocotb.triggers import Timer

@cocotb.test()
async def test_xor_gate_simple(dut):
    """Test XOR gate with simple inputs"""

    # Test Case 1: a=0, b=0, y should be 0
    dut.a.value = 0
    dut.b.value = 0
    await Timer(1, units='ns')
    assert dut.y.value == 0, f"Test failed with a = 0, b = 0, expected y=0, got y={dut.y.value}"

    # Test Case 2: a=0, b=1, y should be 1
    dut.a.value = 0
    dut.b.value = 1
    await Timer(1, units='ns')
    assert dut.y.value == 1, f"Test failed with a = 0, b = 1, expected y=1, got y={dut.y.value}"

    # Test Case 3: a=1, b=0, y should be 1
    dut.a.value = 1
    dut.b.value = 0
    await Timer(1, units='ns')
    assert dut.y.value == 1, f"Test failed with a = 1, b = 0, expected y=1, got y={dut.y.value}"

    # Test Case 4: a=1, b=1, y should be 0
    dut.a.value = 1
    dut.b.value = 1
    await Timer(1, units='ns')
    assert dut.y.value == 0, f"Test failed with a = 1, b = 1, expected y=0, got y={dut.y.value}"

