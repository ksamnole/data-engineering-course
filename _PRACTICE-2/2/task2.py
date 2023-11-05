import numpy as np
import json

value = 500 + 25
matrix = np.load('matrix_25_2.npy')

array_x = []
array_y = []
array_z = []

for (x,y), z in np.ndenumerate(matrix):
  if z > value:
    array_x.append(x)
    array_y.append(x)
    array_z.append(x)

np.savez('result.npz', array_x, array_y, array_z)
np.savez_compressed('result_comp.npz', array_x, array_y, array_z)