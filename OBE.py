import numpy as np

# Matriks A (12x12)
A = np.array([
    [-4, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, -4, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, -4, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, -4, 1, 0, 1, 0, 0, 0, 0, 0],
    [0, 1, 0, 1, -4, 1, 0, 1, 0, 0, 0, 0],
    [0, 0, 1, 0, 1, -4, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, -4, 1, 0, 1, 0, 0],
    [0, 0, 0, 0, 1, 0, 1, -4, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 1, 0, 1, -4, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, -4, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 1, -4, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, -4]
])

# Vektor b (12x1)
b = np.array([
    -50, 0, -50, -50, 0, -50, -50, 0, -50, -150, -100, -150
])

# Menyelesaikan persamaan Ax = b
x = np.linalg.solve(A, b)

# Menampilkan hasil
for i, val in enumerate(x, 1):
    print(f"x{i} = {val}")
