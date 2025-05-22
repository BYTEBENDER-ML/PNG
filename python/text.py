import matplotlib.pyplot as plt
import numpy as np

# 1. Define x range and functions
x = np.linspace(-5 * np.pi, 5 * np.pi, 500)
y1 = x
y2 = -x
y3 = np.sin(x)
y4 = x * np.sin(x)

# 2. Plot the functions
plt.plot(x, y1, label='x')
plt.plot(x, y2, label='-x')
plt.plot(x, y3, label='sin(x)')
plt.plot(x, y4, label='x*sin(x)')

# 3. Add legend
plt.legend()

# 4. Annotate the origin
plt.annotate('Origin', xy=(0, 0), xytext=(-10, 10),
            textcoords='offset points',
            arrowprops=dict(arrowstyle='->'))

# 5. Set axes limits to match the x range
plt.xlim(-5 * np.pi, 5 * np.pi)

plt.grid(True)
plt.title("Plot of x, -x, sin(x), and x*sin(x)")
plt.xlabel("x")
plt.ylabel("y")
plt.show()
