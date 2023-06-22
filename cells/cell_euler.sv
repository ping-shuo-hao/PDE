module Euler_DDA #(
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
    output logic signed [DATA_WIDTH-1:0] dz,
    output logic signed [DATA_WIDTH-1:0] y
);
    parameter R_WIDTH = TIME_SCALE_POW;
    parameter PRODUCT_WIDTH = DATA_WIDTH + R_WIDTH;

    logic phase;
    logic unsigned [R_WIDTH-1:0] r;
    logic signed [R_WIDTH:0] signed_r;
    logic signed [PRODUCT_WIDTH-1:0] product;

    assign signed_r = r;
    assign product = signed_r + dt * y;

    always_ff @(posedge clk or posedge reset) begin
        if (reset) begin
            y <= y0;
            r <= 0;
            phase <= 0;
        end else begin
            if (phase == 0) begin
                dz <= product[PRODUCT_WIDTH-1:R_WIDTH];
                r <= product[R_WIDTH-1:0];
            end else begin
                if (set_y) begin
                    y <= y0;
                end else begin
                    y <= y + dy;
                end
            end
            phase <= ~phase; // Alternate between phase 0 and phase 1
        end
    end

endmodule