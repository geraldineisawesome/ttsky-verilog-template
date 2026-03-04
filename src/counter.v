module counter 
#(parameter width_p = 4,
  parameter[width_p - 1:0]reset_val_p = {width_p{1'b0}}
)
(input clk_i,
 input reset_i,
 input up_i,
 input down_i, 
 output reg [width_p - 1:0]count_o);

 always @(posedge clk_i)begin 
    if (reset_i)
        count_o <= reset_val_p;
    else if(!up_i && down_i)
        count_o <= count_o - 1'b1;
    else if(!down_i && up_i)
        count_o <= count_o + 1'b1;
 end 
endmodule 