module TopModule_TB;

    // Parameters
    localparam DATA_WIDTH = 64;
    localparam DATA_SCALE = 1<<62;

    localparam TIME_WIDTH = 8;

    parameter TIME_SCALE_POW = 8;
    localparam TIME_SCALE = 1<<TIME_SCALE_POW;

    localparam CLOCK_PERIOD = 1;

    // Signals
    logic clk;
    logic reset;
    logic signed [DATA_WIDTH-1:0] sin_y0;
    logic signed [DATA_WIDTH-1:0] cos_y0;
    logic signed [TIME_WIDTH-1:0] dt = 1<<(TIME_WIDTH/2);
    logic signed [DATA_WIDTH-1:0] sin_y;
    logic signed [DATA_WIDTH-1:0] cos_y;

    int file=$fopen("./data.csv", "w");;
    real pi=$acos(-1);
    real t_final = 16.0;
    real dt_real = real'(dt) / real'(TIME_SCALE);
    int steps = t_final / dt_real;

    // Instantiate the module under test
    TopModule #(
		.DATA_WIDTH(DATA_WIDTH),
		.TIME_WIDTH(TIME_WIDTH),
        .TIME_SCALE_POW(TIME_SCALE_POW)
    ) dut (
        .clk(clk),
        .reset(reset),
        .sin_y0(sin_y0),
        .cos_y0(cos_y0),
        .dt(dt),
        .sin_y(sin_y),
        .cos_y(cos_y)
    );

    // Clock generation
    always #CLOCK_PERIOD clk = ~clk;

    real t_real;
    real sin_real;
    real cos_real;
    real dut_sum_square_error = 0;

    // Reset initialization
    // Stimulus generation
    initial begin
        clk = 0;
        sin_y0 = $sin(2*pi) * DATA_SCALE;
        cos_y0 = $cos(2*pi) * DATA_SCALE;
        reset = 1;
        #1;
        reset = 0;
        #1;
        $fwrite(file, "DATA_WIDTH,DATA_SCALE,TIME_WIDTH,TIME_SCALE,dt,dt_real,t_real,dut.sin.phase,dut.sin.dy,dut.sin.r,dut.sin.product,dut.sin.product,sin(t_real),sin_y,sin_real,cos(t_real),cos_y,cos_real\n");

        for(int step=0; step<steps; step++) begin
            t_real = step * dt_real;
            sin_real = real'(sin_y) / DATA_SCALE;
            cos_real = real'(cos_y) / DATA_SCALE;
            dut_sum_square_error += (sin_real - $sin(t_real)) ** 2;
            $fwrite(file, "%d,%d,%d,%d,%d,%f,%f,%d,%d,%d,%d,%d,%f,%d,%f,%f,%d,%f\n",DATA_WIDTH,DATA_SCALE,TIME_WIDTH,TIME_SCALE,dt,dt_real,t_real,dut.sin.phase,dut.sin.dy,dut.sin.r,dut.sin.product,dut.sin.product,$sin(t_real),sin_y,sin_real,$cos(t_real),cos_y,cos_real);
            #4;
        end

        $display("%.16f", $sqrt(dut_sum_square_error/real'(steps)));

        $fclose(file);
        $finish;
    end

endmodule

// module euler_testbench();

// 	int fd;
// 	logic rst;
// 	logic clk;
	
// 	logic signed [7:0] dy;
// 	real dxBehavioral;
// 	logic signed [7:0] dx;
// 	logic signed [7:0] dz;
// 	logic signed [7:0] debug1Y;
// 	logic unsigned [7:0] debug1R;
// 	logic signed [7:0] debug1DZ;
// 	logic signed [7:0] debug2Y;
// 	logic unsigned [7:0] debug2R;
// 	logic signed [7:0] debug2DZ;

// 	real zSum;

// 	euler_dda dda1(8'b0, 8'b0, rst, clk, dz, dx, dy, debug1Y, debug1R, debug1DZ); //8'b00000000
// 	euler_dda dda2(8'b0, 8'b01111111, rst, clk, -dy, dx, dz, debug2Y, debug2R, debug2DZ); //8'b11111111

// 	real stepsPerUnit = 4;
// 	real startPoint = 0;
// 	real endPoint = 15;

// 	initial
// 	begin

// 		zSum = 0;

// 		fd = $fopen("./data.txt", "w");
// 		$fwrite(fd, "%f\n", stepsPerUnit);
// 		$fwrite(fd, "%f\n", startPoint);
// 		$fwrite(fd, "%f\n", endPoint);

// 		rst = 0;
// 		clk = 0;

// 		#1;

// 		rst = 1;
// 		clk = 1;

// 		#2;

		

// 		rst = 0;
// 		clk = 1;


// 		#3;

// 		$display("y1 = %d", debug1Y);
// 		$display("r1 = %d", debug1R);
// 		$display("dz1 = %d", debug1DZ);
// 		$display("y2 = %d", debug2Y);
// 		$display("r2 = %d", debug2R);
// 		$display("dz2 = %d", debug2DZ);


// 		for(real i = startPoint; i < endPoint-0.01; i += 1/stepsPerUnit)
// 		begin
// 			clk = 0;
// 			dxBehavioral = $cos(i) - $cos(i - 1/stepsPerUnit);
// 			dx = 2**7*dxBehavioral;

// 			$display("dx = %f", dx);

// 			#4;
// 			clk = 1;
// 			#5;
			
// 			$display("i = %f", i);
// 			$display("y1 = %d", debug1Y);
// 			$display("r1 = %d", debug1R);
// 			$display("dz1 = %d", debug1DZ);
// 			$display("y2 = %d", debug2Y);
// 			$display("r2 = %d", debug2R);
// 			$display("dz2 = %d", debug2DZ);
			
// 			//print to text file
// 			zSum += dz;
// 			$fwrite(fd,"%d,", zSum);
// 		end

// 		$fclose(fd);

// 	end



// endmodule