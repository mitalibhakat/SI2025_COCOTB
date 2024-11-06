module shift_register (
    input wire clk,                // Clock input
    input wire rstn,               // Active-low reset
    input wire data_in,            // 1-bit input data (new data to shift in)
    output reg [3:0] data_out      // 4-bit output data
);

always @(posedge clk or negedge rstn) begin
    if (!rstn) begin
        data_out <= 4'b0000;      // Reset output to 0
    end else begin
        data_out <= {data_out[2:0], data_in}; // Shift left and input new data
    end
end

endmodule



