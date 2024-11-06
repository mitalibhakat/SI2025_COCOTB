import cocotb
from cocotb.triggers import RisingEdge, Timer
from cocotb.clock import Clock
import random

# Constant for clock period
CLOCK_PERIOD_NS = 10

async def reset_dut(dut):
    """Reset the DUT"""
    dut.reset_n.value = 0  # Active low reset
    dut.cs_bar.value = 1   # Ensure cs_bar is high during reset
    await Timer(100, units='ns')  # Wait for reset duration
    dut.reset_n.value = 1  # Release reset
    await RisingEdge(dut.sc)  # Wait for a rising edge on the clock

#async def shift_in_data(dut, data):
    """Shift data serially into the shift register"""
    """for i in range(16):
        dut.si.value = (data >> (15 - i)) & 0x1  # Set the serial input bit
        await Timer(1, units='ns')  # Small delay to ensure si is stable
        await RisingEdge(dut.sc)    # Wait for clock rising edge"""

async def shift_in_data(dut, data):
    """Shift data serially into the shift register with validation."""
    # Validate that data is a 16-bit number
    if not (0 <= data <= 0xFFFF):
     raise ValueError("Data must be a 16-bit value (0 to 65535).")

    i = 15  # Start with the most significant bit
    while i >= 0:
     dut.si.value = (data & (1 << i)) >> i
    await Timer(1, units='ns')
    await RisingEdge(dut.sc)
    i -= 1


@cocotb.test()
async def test_sipo_shift_register(dut):
    """Test for SIPO shift register with active-low reset and cs_bar"""

    # Create a clock on 'sc' signal
    cocotb.start_soon(Clock(dut.sc, CLOCK_PERIOD_NS, units='ns').start())

    # Apply reset
    await reset_dut(dut)

    # Ensure that cs_bar is high and check the parallel output is zero
    dut.cs_bar.value = 1
    await Timer(100, units='ns')  # Short wait to check the initial state

    assert dut.po.value == 0, "Parallel output should be zero after reset"

    # Bring cs_bar low to start shifting
    dut.cs_bar.value = 0

    # Generate random 16-bit data to shift in
    data_in = random.randint(0, 0xFFFF)
    dut._log.info(f"Data to be shifted in: {hex(data_in)}")
    # Shift in the data
    await shift_in_data(dut, data_in)

    # Bring cs_bar high to stop shifting
    dut.cs_bar.value = 1

    # Wait for a few clock cycles to stabilize
    await Timer(50, units='ns')

    # Check the parallel output
    #assert dut.po.value == data_in, f"Expected {hex(data_in)}, but got {hex(dut.po.value)}"

    dut._log.info(f"Shifted in data: {hex(data_in)}, Parallel output: {hex(dut.po.value)}")
    assert dut.po.value == data_in,f"Expected {hex(data_in)}, but got {hex(dut.po.value)}"

