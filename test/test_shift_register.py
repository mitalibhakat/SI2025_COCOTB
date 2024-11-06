import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer

# Test the shift register design
@cocotb.test()
async def shift_register_test(dut):
    """ Test the 4-bit shift register """

    # Start a clock with a 10 ns period (100 MHz)
    clock = Clock(dut.clk, 10, units="ns")  # Clock frequency = 100 MHz
    cocotb.start_soon(clock.start())  # Start the clock

    # Initialize input signals
    dut.data_in.value = 0
    dut.rstn.value = 0
    await Timer(20, units="ns")  # Hold reset for 20ns

    # Release reset and log the values
    dut.rstn.value = 1
    await RisingEdge(dut.clk)  # Wait for rising edge after reset
    cocotb.log.info(f"After reset: data_out = {dut.data_out.value}")

    # Check if data_out is reset
    assert dut.data_out.value == 0, f"Error: data_out after reset = {dut.data_out.value}"

    # Apply input and shift data
    test_data = [1, 0, 1, 1]  # Example input data stream
    expected_output = 0

    for i in range(len(test_data)):
        dut.data_in.value = test_data[i]  # Set input value
        await RisingEdge(dut.clk)  # Wait for next clock edge

        # Wait a small delay for signal propagation
        await Timer(1, units="ns")

        # Shift the expected output
        expected_output = ((expected_output << 1) & 0xF) | test_data[i]

        # Log current state
        cocotb.log.info(f"Cycle {i+1}: data_in = {test_data[i]}, data_out = {dut.data_out.value}, expected_output = {expected_output}")

        # Check the result
        assert dut.data_out.value == expected_output, \
            f"Error: data_out = {dut.data_out.value}, expected = {expected_output}"

    cocotb.log.info("Shift register test passed.")



