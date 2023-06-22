#! /koko/system/anaconda/bin/python

import math
import numpy as np
import matplotlib.pyplot as plt

t_0 = 0.0
t_f = 4.0

quantity_precision = 48
quantity_scaling = 1<<quantity_precision

temporal_precision = 8
temporal_scaling = 1<<temporal_precision
register_overflow = 1<<temporal_precision

t_0_fixed = int(t_0*temporal_scaling)
t_f_fixed = int(t_f*temporal_scaling)

N_pows = range(1,12)

RMSEs_euler = []
RMSEs_euler_fixed = []
RMSEs_euler_dda = []

RMSEs_midpoint = []
RMSEs_midpoint_fixed = []
RMSEs_adams_dda = []

RMSEs_heun = []
RMSEs_heun_fixed = []
RMSEs_rk_dda = []

RMSEs_rk = []
RMSEs_rk_fixed = []

class Euler_DDA:

	def __init__(self, y=0):
		self.y = y
		self.r = 0

	def phase_0(self, dt=0):
		self.r += dt * self.y
		self.dz = self.r // register_overflow
		self.r %= register_overflow

	def phase_1(self, dy=0):
		self.y += dy

class Adams_DDA:

	def __init__(self, y=0):
		self.y = y
		self.r = 0

	def phase_0(self, dt=0):
		self.r += dt * self.y
		self.dz1 = self.r // register_overflow
		self.r %= register_overflow

	def phase_1(self, dt=0, dy1=0):
		self.dy1 = dy1
		self.r += dt * ( self.y + 1*self.dy1//1 )
		self.dz2 = self.r // register_overflow
		self.r %= register_overflow

	def phase_2(self, dy2=0):
		self.dy2 = dy2
		self.y += 1*self.dy1//2 + 1*self.dy2//2

class Heun_DDA:

	def __init__(self, y=0):
		self.y = y
		self.r1 = 0
		self.r2 = 0
		self.dy1 = 0
		self.dy2 = 0

	def phase_0(self, dt=0):
		self.r1 += dt * self.y
		self.dz1 = self.r1 // register_overflow
		self.r1 %= register_overflow

	def phase_1(self, dt=0, dy1=0):
		self.dy1 = dy1
		self.r2 += dt * ( self.y + 1*self.dy1//1 )
		self.dz2 = self.r2 // register_overflow
		self.r2 %= register_overflow

	def phase_2(self, dy2=0):
		self.dy2 = dy2
		self.y += (1*self.dy1//2) + (1*self.dy2//2)

class RK_DDA:

	def __init__(self, y=0):
		self.y = y
		self.r = 0

	def phase_0(self, dt=0):
		self.r += dt * self.y
		self.dz1 = self.r // register_overflow
		self.r %= register_overflow

	def phase_1(self, dt=0, dy1=0):
		self.dy1 = dy1
		self.r += dt * ( self.y + self.dy1//2 )
		self.dz2 = self.r // register_overflow
		self.r %= register_overflow

	def phase_2(self, dt=0, dy2=0):
		self.dy2 = dy2
		self.r += dt * ( self.y - 0*self.dy1//3 + self.dy2//2 )
		self.dz3 = self.r // register_overflow
		self.r %= register_overflow

	def phase_3(self, dt=0, dy3=0):
		self.dy3 = dy3
		self.r += dt * ( self.y + 0*self.dy1 - 0*self.dy2 + self.dy3 )
		self.dz4 = self.r // register_overflow
		self.r %= register_overflow

	def phase_4(self, dy4=0):
		self.dy4 = dy4
		self.y += 1*self.dy1//6 + 2*self.dy2//6 + 2*self.dy3//6 + 1*self.dy4//6

for N_pow in N_pows:

	N = 1<<N_pow
	h = (t_f-t_0)/N
	h_fixed = (t_f_fixed-t_0_fixed)//N
	xs = np.arange(t_0, t_f, h)
	closed_sin = np.sin(xs)

	euler_sin = [math.sin(t_0)]
	euler_cos = [math.cos(t_0)]
	euler_error = [0.0]

	euler_fixed_sin = [int(math.sin(t_0)*quantity_scaling)]
	euler_fixed_cos = [int(math.cos(t_0)*quantity_scaling)]
	euler_fixed_error = [0.0]

	euler_dda_sin = Euler_DDA(y=int(math.sin(t_0)*quantity_scaling)) 
	euler_dda_y_sin = euler_dda_sin.y
	euler_dda_cos = Euler_DDA(y=int(math.cos(t_0)*quantity_scaling)) 
	euler_dda_error = [0.0]

	midpoint_sin = [math.sin(t_0)]
	midpoint_cos = [math.cos(t_0)]
	midpoint_error = [0.0]

	midpoint_fixed_sin = [int(math.sin(t_0)*quantity_scaling)]
	midpoint_fixed_cos = [int(math.cos(t_0)*quantity_scaling)]
	midpoint_fixed_error = [0.0]

	adams_dda_sin = Adams_DDA(y=int(math.sin(t_0)*quantity_scaling))
	adams_dda_y_sin = adams_dda_sin.y
	adams_dda_cos = Adams_DDA(y=int(math.cos(t_0)*quantity_scaling))
	adams_dda_error = [0.0]

	heun_sin = [math.sin(t_0)]
	heun_cos = [math.cos(t_0)]
	heun_error = [0.0]

	heun_fixed_sin = [int(math.sin(t_0)*quantity_scaling)]
	heun_fixed_cos = [int(math.cos(t_0)*quantity_scaling)]
	heun_fixed_error = [0.0]

	rk_dda_sin = RK_DDA(y=int(math.sin(t_0)*quantity_scaling))
	rk_dda_y_sin = rk_dda_sin.y
	rk_dda_cos = RK_DDA(y=int(math.cos(t_0)*quantity_scaling))
	rk_dda_error = [0.0]

	rk_sin = [math.sin(t_0)]
	rk_cos = [math.cos(t_0)]
	rk_error = [0.0]

	rk_fixed_sin = [int(math.sin(t_0)*quantity_scaling)]
	rk_fixed_cos = [int(math.cos(t_0)*quantity_scaling)]
	rk_fixed_error = [0.0]

	for step in range(1,N):

		next_euler_sin = euler_sin[-1] + h * euler_cos[-1]
		next_euler_cos = euler_cos[-1] - h * euler_sin[-1]
		euler_sin.append(next_euler_sin)
		euler_cos.append(next_euler_cos)
		euler_error.append(next_euler_sin-closed_sin[step])

		next_euler_fixed_sin = euler_fixed_sin[-1] + h_fixed * euler_fixed_cos[-1] // temporal_scaling
		next_euler_fixed_cos = euler_fixed_cos[-1] - h_fixed * euler_fixed_sin[-1] // temporal_scaling
		euler_fixed_sin.append(next_euler_fixed_sin)
		euler_fixed_cos.append(next_euler_fixed_cos)
		euler_fixed_error.append(next_euler_fixed_sin/quantity_scaling-closed_sin[step])

		euler_dda_sin.phase_0(dt = h_fixed)
		euler_dda_cos.phase_0(dt = h_fixed)
		euler_dda_sin.phase_1(dy = +euler_dda_cos.dz)
		euler_dda_cos.phase_1(dy = -euler_dda_sin.dz)
		euler_dda_error.append(euler_dda_sin.y/quantity_scaling-closed_sin[step])

		next_midpoint_sin = midpoint_sin[-1] + h * ( midpoint_cos[-1] - h/2 * midpoint_sin[-1] )
		next_midpoint_cos = midpoint_cos[-1] - h * ( midpoint_sin[-1] + h/2 * midpoint_cos[-1] )
		midpoint_sin.append(next_midpoint_sin)
		midpoint_cos.append(next_midpoint_cos)
		midpoint_error.append(next_midpoint_sin-closed_sin[step])

		next_midpoint_fixed_sin = midpoint_fixed_sin[-1] + h_fixed * ( midpoint_fixed_cos[-1] - h_fixed * midpoint_fixed_sin[-1] // 2 // temporal_scaling ) // temporal_scaling
		next_midpoint_fixed_cos = midpoint_fixed_cos[-1] - h_fixed * ( midpoint_fixed_sin[-1] + h_fixed * midpoint_fixed_cos[-1] // 2 // temporal_scaling ) // temporal_scaling
		midpoint_fixed_sin.append(next_midpoint_fixed_sin)
		midpoint_fixed_cos.append(next_midpoint_fixed_cos)
		midpoint_fixed_error.append(next_midpoint_fixed_sin/quantity_scaling-closed_sin[step])

		adams_dda_sin.phase_0(dt = h_fixed)
		adams_dda_cos.phase_0(dt = h_fixed)
		adams_dda_sin.phase_1(dt = h_fixed, dy1 = +adams_dda_cos.dz1)
		adams_dda_cos.phase_1(dt = h_fixed, dy1 = -adams_dda_sin.dz1)
		adams_dda_sin.phase_2(dy2 = +adams_dda_cos.dz2)
		adams_dda_cos.phase_2(dy2 = -adams_dda_sin.dz2)
		adams_dda_error.append(adams_dda_sin.y/quantity_scaling-closed_sin[step])

		next_heun_sin = heun_sin[-1] + h/2 * ( heun_cos[-1] + (heun_cos[-1] - h * heun_sin[-1]) )
		next_heun_cos = heun_cos[-1] - h/2 * ( heun_sin[-1] + (heun_sin[-1] + h * heun_cos[-1]) )
		heun_sin.append(next_heun_sin)
		heun_cos.append(next_heun_cos)
		heun_error.append(next_heun_sin-closed_sin[step])

		next_heun_fixed_sin = heun_fixed_sin[-1] + h_fixed * ( heun_fixed_cos[-1] + (heun_fixed_cos[-1] - h_fixed * heun_fixed_sin[-1] // temporal_scaling) ) // 2 // temporal_scaling
		next_heun_fixed_cos = heun_fixed_cos[-1] - h_fixed * ( heun_fixed_sin[-1] + (heun_fixed_sin[-1] + h_fixed * heun_fixed_cos[-1] // temporal_scaling) ) // 2 // temporal_scaling
		heun_fixed_sin.append(next_heun_fixed_sin)
		heun_fixed_cos.append(next_heun_fixed_cos)
		heun_fixed_error.append(next_heun_fixed_sin/quantity_scaling-closed_sin[step])

		rk_dda_sin.phase_0(dt = h_fixed)
		rk_dda_cos.phase_0(dt = h_fixed)
		rk_dda_sin.phase_1(dt = h_fixed, dy1 = +rk_dda_cos.dz1)
		rk_dda_cos.phase_1(dt = h_fixed, dy1 = -rk_dda_sin.dz1)
		rk_dda_sin.phase_2(dt = h_fixed, dy2 = +rk_dda_cos.dz2)
		rk_dda_cos.phase_2(dt = h_fixed, dy2 = -rk_dda_sin.dz2)
		rk_dda_sin.phase_3(dt = h_fixed, dy3 = +rk_dda_cos.dz3)
		rk_dda_cos.phase_3(dt = h_fixed, dy3 = -rk_dda_sin.dz3)
		rk_dda_sin.phase_4(dy4 = +rk_dda_cos.dz4)
		rk_dda_cos.phase_4(dy4 = -rk_dda_sin.dz4)
		rk_dda_error.append(rk_dda_sin.y/quantity_scaling-closed_sin[step])

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

		k1_fixed_sin =  rk_fixed_cos[-1]
		k1_fixed_cos = -rk_fixed_sin[-1]
		k2_fixed_sin =  rk_fixed_cos[-1] + h_fixed * ( (1/3)*k1_fixed_cos ) // temporal_scaling
		k2_fixed_cos = -rk_fixed_sin[-1] - h_fixed * ( (1/3)*k1_fixed_sin ) // temporal_scaling
		k3_fixed_sin =  rk_fixed_cos[-1] + h_fixed * ( (-1/3)*k1_fixed_cos + (1)*k2_fixed_cos ) // temporal_scaling
		k3_fixed_cos = -rk_fixed_sin[-1] - h_fixed * ( (-1/3)*k1_fixed_sin + (1)*k2_fixed_sin ) // temporal_scaling
		k4_fixed_sin =  rk_fixed_cos[-1] + h_fixed * ( (1)*k1_fixed_cos + (-1)*k2_fixed_cos + (1)*k3_fixed_cos ) // temporal_scaling
		k4_fixed_cos = -rk_fixed_sin[-1] - h_fixed * ( (1)*k1_fixed_sin + (-1)*k2_fixed_sin + (1)*k3_fixed_sin ) // temporal_scaling

		next_rk_fixed_sin = rk_fixed_sin[-1] + h_fixed * ( 1/8*k1_fixed_sin + 3/8*k2_fixed_sin + 3/8*k3_fixed_sin + 1/8*k4_fixed_sin ) // temporal_scaling
		next_rk_fixed_cos = rk_fixed_cos[-1] + h_fixed * ( 1/8*k1_fixed_cos + 3/8*k2_fixed_cos + 3/8*k3_fixed_cos + 1/8*k4_fixed_cos ) // temporal_scaling
		rk_fixed_sin.append(next_rk_fixed_sin)
		rk_fixed_cos.append(next_rk_fixed_cos)
		rk_fixed_error.append(next_rk_fixed_sin/quantity_scaling-closed_sin[step])

	fig = plt.figure()
	ax = fig.add_subplot()
	ax.scatter(xs, closed_sin, color='black', label='closed')
	ax.scatter(xs, euler_sin, color='red', label='euler')
	ax.scatter(xs, np.divide(euler_fixed_sin,quantity_scaling), color='orange', label='euler_fixed')
	# ax.scatter(xs, np.divide(euler_dda_y_sin,quantity_scaling), color='pink', label='euler_dda')
	ax.scatter(xs, midpoint_sin, color='yellow', label='midpoint')
	ax.scatter(xs, np.divide(midpoint_fixed_sin,quantity_scaling), color='green', label='midpoint_fixed')
	# ax.scatter(xs, np.divide(adams_dda_y_sin,quantity_scaling), color='cyan', label='adams_dda')
	ax.scatter(xs, heun_sin, color='blue', label='heun')
	ax.scatter(xs, np.divide(heun_fixed_sin,quantity_scaling), color='violet', label='heun_fixed')
	# ax.scatter(xs, np.divide(rk_dda_y_sin,quantity_scaling), color='magenta', label='rk_dda')
	ax.scatter(xs, rk_sin, color='brown', label='rk')
	plt.legend()
	plt.show()

	euler_RMSE = math.sqrt(np.mean(np.square(euler_error)))
	euler_fixed_RMSE = math.sqrt(np.mean(np.square(euler_fixed_error)))
	euler_dda_RMSE = math.sqrt(np.mean(np.square(euler_dda_error)))

	midpoint_RMSE = math.sqrt(np.mean(np.square(midpoint_error)))
	midpoint_fixed_RMSE = math.sqrt(np.mean(np.square(midpoint_fixed_error)))
	adams_dda_RMSE = math.sqrt(np.mean(np.square(adams_dda_error)))

	heun_RMSE = math.sqrt(np.mean(np.square(heun_error)))
	heun_fixed_RMSE = math.sqrt(np.mean(np.square(heun_fixed_error)))
	rk_dda_RMSE = math.sqrt(np.mean(np.square(rk_dda_error)))

	rk_RMSE = math.sqrt(np.mean(np.square(rk_error)))
	rk_fixed_RMSE = math.sqrt(np.mean(np.square(rk_fixed_error)))

	RMSEs_euler.append(euler_RMSE)
	RMSEs_euler_fixed.append(euler_fixed_RMSE)
	RMSEs_euler_dda.append(euler_dda_RMSE)

	RMSEs_midpoint.append(midpoint_RMSE)
	RMSEs_midpoint_fixed.append(midpoint_fixed_RMSE)
	RMSEs_adams_dda.append(adams_dda_RMSE)

	RMSEs_heun.append(heun_RMSE)
	RMSEs_heun_fixed.append(heun_fixed_RMSE)
	RMSEs_rk_dda.append(rk_dda_RMSE)

	RMSEs_rk.append(rk_RMSE)
	RMSEs_rk_fixed.append(rk_fixed_RMSE)
	# print(RMSEs)

# exit()

fig = plt.figure()
ax = fig.add_subplot()

ax.scatter(N_pows, np.log(RMSEs_euler), color='red', label='euler')
ax.scatter(N_pows, np.log(RMSEs_euler_fixed), color='orange', label='euler_fixed')
ax.scatter(N_pows, np.log(RMSEs_euler_dda), color='pink', label='euler_dda')

ax.scatter(N_pows, np.log(RMSEs_midpoint), color='yellow', label='midpoint')
ax.scatter(N_pows, np.log(RMSEs_midpoint_fixed), color='green', label='midpoint_fixed')
ax.scatter(N_pows, np.log(RMSEs_adams_dda), color='cyan', label='adams_dda')

# ax.scatter(N_pows, np.log(RMSEs_heun), color='blue', label='heun')
# ax.scatter(N_pows, np.log(RMSEs_heun_fixed), color='violet', label='heun_fixed')

ax.scatter(N_pows, np.log(RMSEs_rk), color='brown', label='rk')
ax.scatter(N_pows, np.log(RMSEs_rk_fixed), color='black', label='rk_fixed')
ax.scatter(N_pows, np.log(RMSEs_rk_dda), color='magenta', label='rk_dda')

plt.legend()
plt.show()
