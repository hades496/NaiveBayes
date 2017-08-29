import numpy as np

a = np.array([[1, 5, 6]])
b = np.array([7, 8, 9])
c = np.row_stack((a, b))
print c[1,1]
