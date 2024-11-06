<h2>SI2025_CoCotb<h2>
<p>This page provides an in-depth study material on Cocotb(Coroutine-based Co-simulation Testbench).</p>
<hr>
<h2>Table Of Contents</h2>
<ul>
  <li><a href="#introduction"> Introduction to Cocotb</a></li>
  <li><a href="#setup">Setting Up The Environmnet</a></li>
  <li><a href="#basics">Cocotb Basics</li>
    <ul>
      <li><a href="#coroutines">Coroutines and Triggers</a></li>
      <li><a href="#dut-interaction">Interacting with the DUT</a></li>
      </ul>
    <li><a href="#tests">Writing Cocotb Tests</a></li>
    <li><a href="#advanced">Advanced Topics</a></li>
    <li><a href="#troubleshooting">Common Issues and Debugging</a></li>
    <li><a href="#resources">Resources and Further Reading</a></li>
</ul>
    
<hr>
<h2 id="introduction">1.Introduction to Cocotb</h2>
<p>Cocotb (Coroutine-based Co-Simulation Testbench) is a Python-based library for testing digital designs in <strong> Verilog</strong>. Unlike traditional testbenches written in HDL,Cocotb allows you to write testbenches in Python , making them easier to read,write and maintain.
<h3> Key Benefits</h3>
<ul>
  <li><strong>Python-based Testing:</strong>Use Python's extensive libraries to simplify complex testing tasks.</li>
  <li><strong>Coroutines for concurrency:</strong>Schedule tasks and trigger events using coroutines.</li>
  <li><strong>Reusable and Modular:</strong>Easily maintain and extend testbenches.</li>
  <li><strong>Provides Interface:</strong>Provides Python interface to control standard RTL simulators(Cadence,Ouesta,VCS,etc.).</li>
  <li>Cocotb is completely free,open source.</li>
</ul>

<hr>

<h2 id="setup">2.Setting Up The Environment</h2>
<ol>
  <li><strong> Install Python(Python3.6+)recommended :</strong></li>
  <pre><code>sudo apt-get install make python3 python3-pip libpython3-dev</code></pre>
  <li><strong>Check the Python version :</strong></li>
  <pre><code> python3 --version </code></pre>
  <li><strong>Set up a Virtual Environment :</strong></li>
  <pre><code>python3 -m venv file_name </code></pre>
  <p>Example: Create One Directory & set-up virtual environment
  <pre><code>mkdir venv
  cd venv
  python3 -m venv venv_env
</code></pre>
Note:- here venv is my directory name </p>
   <li><strong>Activate the virtual environment :</strong></li>
   On Linux:
  <pre><code>source file_name/bin/activate</code></pre>
  On Windows:
  <pre><code>.\cocotb_env\Scripts\activate</code></pre>
  <li><strong>Install Cocotb :</strong></li>
  <pre><code>pip install cocotb</code></pre>
  <li><strong>Install Cocotb Bus :</strong></li>
<pre><code>pip install cocotb[bus] </code></pre>
  <li><strong>Install a Supported Simulator :</strong></li>
  Cocotb supports several simulators,such as Icarus Verilog, ModelSim, Xcelium, and VCS.Here's how to install Icarus Verilig for Open-Source Simulation:
  Linux(use your package manager,e.g.,apt for Debian/Ubuntu):
  <pre><code>sudo apt update
sudo apt install iverilog
  </code></pre>
  <li>Verify Installation :</li>
  <pre><code>python -m cocotb.config
iverilog -v</code></pre>
  <li><strong>Makefile :</strong></li>
   Cocotb requires a Makefile for configuring simulator options and specifying the design files to be tested.Here is the basic structure of makefile:
  <pre><code>SIM ?= icarus
TOPLEVEL_LANG ?= verilog
MODULE = test_module_name

VERILOG_SOURCES = $(PWD)/path_to_verilog_file.v
TOPLEVEL = your_dut_module

include $(shell cocotb-config --makefiles)/Makefile.sim
</code></pre>
Note: Make sure that $Path should be correct.
</ol>
<h2 id="basics">2.Cocotb Basics</h2>
<p>Cocotb is a revolutionary coroutine-based framework that brings the simplicity of Python to the complex world of hardware verification. By allowing developers to write testbenches in Python, Cocotb bridges the gap between software development practices and hardware verification methodologies.
<br>
 <ol>
   <li><strong>Basic Architecture</strong></li></p>
The Ingredients:
<ul>
  <li> A Design Under Test(DUT):Verilog or VHDL</li
  <li>A Makefile</li>
  <li>Testbench in Python</li></ul>
  <p><strong></strong>Below is the basic architecture of Cocotb:</strong></p>
<table>
        <tr>
            <td><img src="image/architecture.png" alt="Image 1" style="width: 100%;"></td>
            <td><img src="image/overview.png" alt="Image 2" style="width: 100%;"></td>
        </tr>
    </table>
   <br>
</p>
  <p style="test-align: left;"> Working :</p>
  <ul>
    <li>Design Under Test(DUT) runs in standard simulator.</li>
    <li>Cocotb provides interface between simulator and Python.</li>
    <li>Uses Verilog Procedural Interface(VPI) or VHDL procedural Interface(VHPI).VPI -> Verilog and VHPI -> VHDL.</li>
    <li>Python Testbench code can :
    <ul>
      <li> Reach into DUT hierarchy and change values.</li>
      <li>Wait for simulation time to pass.</li>
      <li>Wait for a rising or falling edge of a signal.</li>
    </ul></li>
    <p>Basic Example :
    <br>
    DUT of xor_gate.</p>
  <pre><code>// xor_gate.v
module xor_gate (
    input wire a,
    input wire b,
    output wire y
);
    assign y = a ^ b;  // XOR gate logic
endmodule
  </code></pre>
    <br>
    <p>Testbench in python</p>
    <pre><code> import cocotb
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
</code></pre>
<p><ul>
  <li>In the above example @cocotb.test() decorator marks the test_xor_gate_simple function as test.</li>
  <li>The test function accepts a dut(device under test),which is the XOR gate module,as its argument.</li>
  <li>Assertion Check:</li>
  <ul><li>For each case,the test uses an assert statement to verify that the output matched the expected result.</li>
    <li>If the assertion fails(i.e.,the output is not as expected),an error message is printed showing the input values and the actual result.</li>
  </ul> 
  <li>Use of Timer:</li>
  <ul>The Timer(1, units='ns') is used to wait for 1 nanosecond after changing the inputs, allowing the circuit to settle before checking the output 
</ul> 
  <li>Test Completion:</li>
  <ul>
    <li>If all assertions pass,the test completes successfully without any error messages.</li>
  <li>If any assertion fails,the test stops at the failed test case and reports the failure.</li>
  </ul>
  </ul>
  <hr>
  <h3 id="coroutines">Coroutines and Triggers</h3>
<p>Cocotb uses <strong>coroutines</strong> and <strong>triggers</strong> to manage timing and events. This allows tasks to run concurrently within the same test.It allows suspending and resuming execution using <strong>await</strong>.
  
  <br>
  
  <strong>Coroutines</strong> help run multiple test tasks at once,even if they involve waiting for different times or events.</p>
  <ul> <li>A coroutine in Python is defined with <strong>async def</strong></li>
  <li>Cocotb coroutines typically represent test steps or procedures that involve waiting for signals or time delays.</li></ul>
  <br>
  <strong>Triggers</strong> are events that can be awaited by coroutines.They are used to pause a coroutine until a specific condition, time delay, or signal change occurs in the simulation. Cocotb provides various built-in triggers.
  Example of Coroutines with Triggers in Cocotb
  <pre><code>
import cocotb
from cocotb.triggers import Timer, RisingEdge, FallingEdge

@cocotb.test()
async def test_example(dut):
    print("Test started")
    
    # Wait for a specific time period
    await Timer(100, units="ns")
    print("Waited for 100 ns")

    # Wait for a rising edge on the clock signal
    await RisingEdge(dut.clk)
    print("Detected rising edge of the clock")

    # Wait for a falling edge on the clock signal
    await FallingEdge(dut.clk)
    print("Detected falling edge of the clock")

    # Wait for a combination of multiple edges
    await Combine(RisingEdge(dut.clk), FallingEdge(dut.reset))
    print("Detected rising edge of clk and falling edge of reset")
 </code></pre>
 <br>
 In this example
 <ul>
   <li>The coroutine first waits for 100 ns using the Timer trigger.</li>
   <li> Then, it waits for a rising edge on dut.clk.</li>
   <li> It then waits for a falling edge on dut.clk.</li>
   <li> Finally, it waits for both a rising edge on clk and a falling edge on reset simultaneously.</li>
 </ul>
 <h3 id="dut-interaction">Interacting with the DUT</h3>
<p>Each signal in the DUT can be accessed directly as an attribute of the <code>dut</code> object:</p>

<pre><code>dut.signal_name.value = 1
await RisingEdge(dut.clk)
assert dut.output_signal.value == expected_value</code></pre>

<hr>

<h2 id="tests">4. Writing Cocotb Tests</h2>
<p>Structure a Cocotb test with setup, stimulus, assertions, and logging.</p>

<pre><code>import cocotb
from cocotb.triggers import RisingEdge

@cocotb.test()
async def test_simple(dut):
    """Basic test that toggles a clock and checks output."""
    dut.reset.value = 1
    await Timer(5, units='ns')
    dut.reset.value = 0

    for i in range(10):
        await RisingEdge(dut.clk)
        dut.input_signal.value = i
        assert dut.output_signal.value == expected_output(i)</code></pre>

<hr>

<h2 id="advanced">5. Advanced Topics</h2>

<h3>Clock and Reset Management</h3>
<pre><code>async def clock_gen(dut, period_ns=10):
    while True:
        dut.clk.value = 0
        await Timer(period_ns / 2, units='ns')
        dut.clk.value = 1
        await Timer(period_ns / 2, units='ns')</code></pre>

<h3>Using Assertions and Logging</h3>
<p>Assertions help validate DUT outputs. Cocotb also provides <code>cocotb.log</code> for detailed logging.</p>
<pre><code>
dut.a.value = 1
dut.b.value = 1
await Timer(1, units='ns')
assert dut.y.value == 0, f"Test failed with a = 1, b = 1, expected y=0, got y={dut.y.value}"
</code></pre>
<pre><code>
  cocotb.log.info("Simulation started")
assert dut.output_signal.value == expected_value, "Test failed: Output did not match"

</code></pre>

<hr>

<h2 id="troubleshooting">6. Common Issues and Debugging</h2>
<ul>
    <li><strong>Simulator Path Issue:</strong> Ensure the simulator is in your <code>$PATH</code>.</li>
    <li><strong>Signal Scoping:</strong> Use <code>dut.&lt;signal&gt;</code> to access DUT signals.</li>
    <li><strong>Timing Conflicts:</strong> Use <code>await Timer()</code> to manage timing precisely.</li>
</ul>

<hr>

<h2 id="resources">7. Resources and Further Reading</h2>
<ul>
    <li><a href="https://cocotb.readthedocs.io/">Cocotb Documentation</a></li>
    <li><a href="https://docs.python.org/3/">Python Documentation</a></li>
    <li><a href="https://github.com/cocotb/cocotb">Cocotb GitHub Repository</a></li>
    <li><a href="https://docs.cocotb.org/en/stable/coroutines.html">Coroutines and tasks</a></li>
  <li><a href="https://hardwareteams.com/docs/fpga-asic/cocotb/getting-started/"></a></li>
</ul>

</html>

 
  
  


    
    
    


  
</p>

