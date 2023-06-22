module TopModule #(
    parameter DATA_WIDTH,
    parameter TIME_WIDTH,
    parameter TIME_SCALE_POW
) (
    input logic clk,
    input logic reset,
    input logic signed [DATA_WIDTH-1:0] sin_y0,
    input logic signed [DATA_WIDTH-1:0] cos_y0,
    input logic signed [TIME_WIDTH-1:0] dt,
    output logic signed [DATA_WIDTH-1:0] sin_y,
    output logic signed [DATA_WIDTH-1:0] cos_y
);

    logic signed [DATA_WIDTH-1:0] sin_dz;
    logic signed [DATA_WIDTH-1:0] cos_dz;

    Euler_DDA #(
        .DATA_WIDTH(DATA_WIDTH),
        .TIME_WIDTH(TIME_WIDTH),
        .TIME_SCALE_POW(TIME_SCALE_POW)
    ) sin (
        .clk(clk),
        .reset(reset),
        .set_y(1'b0),
        .y0(sin_y0),
        .dt(dt),
        .dy(+cos_dz),
        .dz(sin_dz),
        .y(sin_y)
    );

    Euler_DDA #(
        .DATA_WIDTH(DATA_WIDTH),
        .TIME_WIDTH(TIME_WIDTH),
        .TIME_SCALE_POW(TIME_SCALE_POW)
    ) cos (
        .clk(clk),
        .reset(reset),
        .set_y(1'b0),
        .y0(cos_y0),
        .dt(dt),
        .dy(-sin_dz),
        .dz(cos_dz),
        .y(cos_y)
    );

endmodule
