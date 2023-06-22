module RK2_DDA #(
    parameter DATA_WIDTH,
    parameter TIME_WIDTH,
    parameter TIME_SCALE_POW
) (
    input logic clk,
    input logic reset,
    input logic set_y,
    input logic signed [DATA_WIDTH-1:0] y0,
    input logic signed [TIME_WIDTH-1:0] dt,
    input logic signed [DATA_WIDTH-1:0] dy,
    output reg signed [DATA_WIDTH-1:0] dz,
    output reg signed [DATA_WIDTH-1:0] y
);
    parameter R_WIDTH = TIME_SCALE_POW;
    parameter PRODUCT_WIDTH = DATA_WIDTH + R_WIDTH;

    reg [1:0] phase;

    reg signed [DATA_WIDTH-1:0] dy1;
    reg unsigned [R_WIDTH-1:0] r;
    logic signed [R_WIDTH:0] signed_r;
    logic signed [PRODUCT_WIDTH-1:0] product_0;
    logic signed [PRODUCT_WIDTH-1:0] product_1;

    assign signed_r = r;
    assign product_0 = signed_r + dt * y;
    assign product_1 = signed_r + dt * ( y + (dy>>>1) );

    always_ff @(posedge clk or posedge reset) begin
        if (reset) begin
            y <= y0;
            r <= 0;
            phase <= 0;
        end else begin
            if (phase == 0) begin
                dz <= product_0[PRODUCT_WIDTH-1:R_WIDTH];
                r <= product_0[R_WIDTH-1:0];
                phase <= 2'd1;
            end
            else if (phase == 1) begin
                dy1 <= dy;
                dz <= product_1[PRODUCT_WIDTH-1:R_WIDTH];
                r <= product_1[R_WIDTH-1:0];
                phase <= 2'd2;
            end
            else begin
                if (set_y) begin
                    y <= y0;
                end else begin
                    // y <= y + ((dy1+dy)>>>1);
                    y <= y + dy;
                end
                phase <= 2'd0;
            end
        end
    end

endmodule