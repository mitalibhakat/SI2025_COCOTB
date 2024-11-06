module shift_register_16bit(
	input wire SC,
	input wire RESET_N,
	input wire d_in,
	output reg [15:0] Q
);


initial begin 
	 $dumpfile("dump.vcd");  // Generate a VCD file called dump.vcd
    $dumpvars(0, shift_register_16bit);  // Dump all signals in the module
end

always @(posedge SC or negedge RESET_N)
begin

	if(!RESET_N)
		Q <= 16'b0; //reset output to zero
	else
		Q <= {Q[14:0],d_in};// shift left and input new biy
end
endmodule 
