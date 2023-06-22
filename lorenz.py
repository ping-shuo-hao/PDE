import numpy as np
import matplotlib.pyplot as plt

def lorenz_butterfly(sigma, rho, beta, num_steps, integration_scheme):
    dt = 0.01
    xs = np.empty(num_steps + 1)
    ys = np.empty(num_steps + 1)
    zs = np.empty(num_steps + 1)
    
    xs[0], ys[0], zs[0] = (0.1, 0.0, 0.0)
    
    for i in range(num_steps):
        x = xs[i]
        y = ys[i]
        z = zs[i]
        
        if integration_scheme == "euler":
            x_dot = sigma * (y - x)
            y_dot = x * (rho - z) - y
            z_dot = x * y - beta * z
            
            xs[i+1] = x + (x_dot * dt)
            ys[i+1] = y + (y_dot * dt)
            zs[i+1] = z + (z_dot * dt)
            
        elif integration_scheme == "midpoint":
            x_dot = sigma * (y - x)
            y_dot = x * (rho - z) - y
            z_dot = x * y - beta * z
            
            x_mid = x + (x_dot * dt / 2)
            y_mid = y + (y_dot * dt / 2)
            z_mid = z + (z_dot * dt / 2)
            
            x_dot_mid = sigma * (y_mid - x_mid)
            y_dot_mid = x_mid * (rho - z_mid) - y_mid
            z_dot_mid = x_mid * y_mid - beta * z_mid
            
            xs[i+1] = x + (x_dot_mid * dt)
            ys[i+1] = y + (y_dot_mid * dt)
            zs[i+1] = z + (z_dot_mid * dt)
    
    return xs, ys, zs

# Parameters
sigma = 10.0
rho = 28.0
beta = 8.0 / 3.0
num_steps = np.logspace(2, 5, num=10, dtype=int)  # Varying number of time steps

# Analytical solution (reference)
def lorenz_analytical(t):
    x = 0.1 * np.exp(sigma * t)
    y = 0.0
    z = 0.0
    return x, y, z

# Compute errors for Euler and Midpoint schemes
errors_euler = []
errors_midpoint = []

for steps in num_steps:
    t = np.linspace(0, (steps-1) * 0.01, steps)
    xs_analytical, _, _ = lorenz_analytical(t)
    
    xs_euler, _, _ = lorenz_butterfly(sigma, rho, beta, steps, "euler")
    error_euler = np.abs(xs_euler - xs_analytical)
    avg_error_euler = np.mean(error_euler)
    errors_euler.append(avg_error_euler)
    
    xs_midpoint, _, _ = lorenz_butterfly(sigma, rho, beta, steps, "midpoint")
    error_midpoint = np.abs(xs_midpoint - xs_analytical)
    avg_error_midpoint = np.mean(error_midpoint)
    errors_midpoint.append(avg_error_midpoint)

# Plot convergence diagram
plt.figure()
plt.loglog(num_steps, errors_euler, marker='o', label='Euler')
plt.loglog(num_steps, errors_midpoint, marker='o', label='Midpoint')
plt.xlabel('Number of Steps')
plt.ylabel('Average Error')
plt.title('Convergence of Euler and Midpoint Methods')
plt.legend()
plt.grid(True)
plt.show()
