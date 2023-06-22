#! /koko/system/anaconda/bin/python

import subprocess
import math
import numpy as np
import matplotlib.pyplot as plt

t_0 = 0.0
t_f = 16.0

N_pows = range(1,16)

RMSEs_euler = []
RMSEs_euler_dda = []

RMSEs_midpoint = []
RMSEs_heun = []

RMSEs_rk = []


for N_pow in N_pows:

	print(f'N_pow={N_pow}')

	N = 1<<N_pow
	h = (t_f-t_0)/N
	xs = np.arange(t_0, t_f, h)
	closed_sin = np.sin(xs)

	euler_sin = [math.sin(t_0)]
	euler_cos = [math.cos(t_0)]
	euler_error = [0.0]

	midpoint_sin = [math.sin(t_0)]
	midpoint_cos = [math.cos(t_0)]
	midpoint_error = [0.0]

	heun_sin = [math.sin(t_0)]
	heun_cos = [math.cos(t_0)]
	heun_error = [0.0]

	rk_sin = [math.sin(t_0)]
	rk_cos = [math.cos(t_0)]
	rk_error = [0.0]

	for step in range(1,N):

		next_euler_sin = euler_sin[-1] + h * euler_cos[-1]
		next_euler_cos = euler_cos[-1] - h * euler_sin[-1]
		euler_sin.append(next_euler_sin)
		euler_cos.append(next_euler_cos)
		euler_error.append(next_euler_sin-closed_sin[step])

		next_midpoint_sin = midpoint_sin[-1] + h * ( midpoint_cos[-1] - h/2 * midpoint_sin[-1] )
		next_midpoint_cos = midpoint_cos[-1] - h * ( midpoint_sin[-1] + h/2 * midpoint_cos[-1] )
		midpoint_sin.append(next_midpoint_sin)
		midpoint_cos.append(next_midpoint_cos)
		midpoint_error.append(next_midpoint_sin-closed_sin[step])

		next_heun_sin = heun_sin[-1] + h/2 * ( heun_cos[-1] + (heun_cos[-1] - h * heun_sin[-1]) )
		next_heun_cos = heun_cos[-1] - h/2 * ( heun_sin[-1] + (heun_sin[-1] + h * heun_cos[-1]) )
		heun_sin.append(next_heun_sin)
		heun_cos.append(next_heun_cos)
		heun_error.append(next_heun_sin-closed_sin[step])

		k1_sin =  rk_cos[-1]
		k1_cos = -rk_sin[-1]
		k2_sin =  rk_cos[-1] + h * ( (1/2)*k1_cos )
		k2_cos = -rk_sin[-1] - h * ( (1/2)*k1_sin )
		k3_sin =  rk_cos[-1] + h * ( (0)*k1_cos + (1/2)*k2_cos )
		k3_cos = -rk_sin[-1] - h * ( (0)*k1_sin + (1/2)*k2_sin )
		k4_sin =  rk_cos[-1] + h * ( (0)*k1_cos + (0)*k2_cos + (1)*k3_cos )
		k4_cos = -rk_sin[-1] - h * ( (0)*k1_sin + (0)*k2_sin + (1)*k3_sin )

		next_rk_sin = rk_sin[-1] + h * ( 1/6*k1_sin + 2/6*k2_sin + 2/6*k3_sin + 1/6*k4_sin )
		next_rk_cos = rk_cos[-1] + h * ( 1/6*k1_cos + 2/6*k2_cos + 2/6*k3_cos + 1/6*k4_cos )
		rk_sin.append(next_rk_sin)
		rk_cos.append(next_rk_cos)
		rk_error.append(next_rk_sin-closed_sin[step])

	# fig = plt.figure()
	# ax = fig.add_subplot()
	# ax.scatter(xs, closed_sin, color='black', label='closed')
	# ax.scatter(xs, euler_sin, color='red', label='euler')
	# ax.scatter(xs, midpoint_sin, color='orange', label='midpoint')
	# ax.scatter(xs, heun_sin, color='yellow', label='heun')
	# ax.scatter(xs, rk_sin, color='green', label='rk')
	# plt.legend()
	# plt.show()

	euler_RMSE = math.sqrt(np.mean(np.square(euler_error)))
	midpoint_RMSE = math.sqrt(np.mean(np.square(midpoint_error)))
	heun_RMSE = math.sqrt(np.mean(np.square(heun_error)))
	rk_RMSE = math.sqrt(np.mean(np.square(rk_error)))

	RMSEs_euler.append(euler_RMSE)
	result = subprocess.run(['iverilog', '-Wall', '-g2009', f'-PTopModule_TB.TIME_SCALE_POW={N_pow}', '../cells/cell_euler.sv', 'sin_cos.sv', 'sin_cos_testbench.sv'], stdout=subprocess.PIPE)
	print(result)
	result = subprocess.run(['./a.out'], stdout=subprocess.PIPE)
	RMSEs_euler_dda.append(float(result.stdout.split()[0]))

	RMSEs_midpoint.append(midpoint_RMSE)
	RMSEs_heun.append(heun_RMSE)
	RMSEs_rk.append(rk_RMSE)

	print(RMSEs_euler_dda)

# exit()

fig = plt.figure()
ax = fig.add_subplot()

ax.scatter(N_pows, np.log(RMSEs_euler), color='red', label='euler')
ax.scatter(N_pows, np.log(RMSEs_heun), color='blue', label='heun')
ax.scatter(N_pows, np.log(RMSEs_midpoint), color='yellow', label='midpoint')
ax.scatter(N_pows, np.log(RMSEs_rk), color='brown', label='rk')
ax.scatter(N_pows, np.log(RMSEs_euler_dda), color='pink', label='euler_dda')

plt.legend()
plt.show()
