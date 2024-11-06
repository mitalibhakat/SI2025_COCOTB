import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer

@cocotb.test()
async def shift_register_16bit_test(dut):
    """Test shift register reset and shifting functionality"""

    # Start a clock on SC with a period of 10ns (100 MHz)
    clock = Clock(dut.SC, 10, units="ns")
    cocotb.start_soon(clock.start())

    # Apply reset
    dut.RESET_N.value = 0  # Assert reset (active low)
    await Timer(2, units="ns")  # Wait for reset to take effect
    dut.RESET_N.value = 1  # De-assert reset
    await Timer(2, units="ns")  # Wait for the system to stabilize

    # Check if the shift register has been reset
    assert dut.Q.value == 0, f"Shift register not reset properly! Got: {dut.Q.value}"

    # Shift in some bits
    dut.d_in.value = 1
    await RisingEdge(dut.SC)  # Wait for the clock rising edge

    dut.d_in.value = 0
    await RisingEdge(dut.SC)  # Wait for the clock rising edge

    # Check if the shifting happened correctly
    assert dut.Q.value == 0b0000000000000001, f"Shift register not shifting properly! Got: {dut.Q.value}"


