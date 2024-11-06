module sipo_shift_register (
	input wire cs_bar, //active low chip select
	input wire reset_n,//sctive low reset 
	input wire sc,//seril clock
	input wire si,//serial input 
	output reg [15:0] po //16-bit parallel output 
);
      reg[15:0] shift_reg; //internal 16-bit shift register 

      always @(posedge sc or negedge reset_n) begin
	      if (!reset_n) begin 
//active low reset : clear the shift register and parallel output 
              shift_reg <= 16'b0;
	      po <= 16'b0;

      end 
      else if(!cs_bar) begin 
	      
	      po <= shift_reg;//update parallel output
	      //shift data in when cs_bar is low 
	      shift_reg <= {shift_reg[14:0], si};  // Shift left, input si into LSB
            //po <= shift_reg;  // Update parallel output
        end
    end

endmodule

