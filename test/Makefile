#enable VCD waveform dumping for Icarus Verilog 
export COCOTB_SIM = 1


SIM ?= icarus

WAVES=1 # set this to 1 to enable waveform dumping 

TOPLEVEL_LANG ?= verilog



#Name of the top-level module
 ifeq ($(DESIGN),counter)
      VERILOG_SOURCES += $(PWD)/../hd1/counter.v
      TOPLEVEL = counter
      MODULE =  test_counter
 endif
 
 ifeq ($(DESIGN), xor_gate)
    VERILOG_SOURCES += $(PWD)/../hd1/xor_gate.v  # Verilog file for the XOR gate
    TOPLEVEL = xor_gate                          # Top-level module in xor_gate.v
    MODULE = test_xor_gate                       # Python test file test_xor_gate.py
endif

ifeq ($(DESIGN), my_design)
    VERILOG_SOURCES += $(PWD)/../hd1/my_design.v     # SystemVerilog file for my_design
    TOPLEVEL = my_design                         # Top-level module in my_design.sv
    MODULE = test_my_design                      # Python test file test_my_design.py
endif

ifeq ($(DESIGN), shift_register)
    VERILOG_SOURCES += $(PWD)/../hd1/shift_register.v
    TOPLEVEL = shift_register
    MODULE   = test_shift_register
endif

ifeq ($(DESIGN),shift_register_16bit)
    VERILOG_SOURCES += $(PWD)/../hd1/shift_register_16bit.v
    TOPLEVEL = shift_register_16bit 
    MODULE   = test_shift_register_16bit
endif 


ifeq ($(DESIGN),count_up)
    VERILOG_SOURCES += $(PWD)/../hd1/count_up.v
    TOPLEVEL = count_up
    MODULE   = test_count_up
endif

include $(shell cocotb-config --makefiles)/Makefile.sim




