import numpy as np
import json

matrix = np.load('matrix_25.npy')

summa = np.sum(matrix)
avg = np.average(matrix)

summaMD = np.sum(np.diag(matrix))
avgMD = np.average(np.diag(matrix))

summaSD = np.sum(np.diag(np.fliplr(matrix)))
avgSD = np.average(np.diag(np.fliplr(matrix)))

maxValue = np.max(matrix)
minValue = np.min(matrix)

dictionary = {
    'sum': str(summa),
    'avr': str(avg),
    'sumMD': str(summaMD),
    'avrSD': str(avgMD),
    'sumSD': str(summaSD),
    'avrSD': str(avgSD),
    'max': str(maxValue),
    'min': str(minValue),
}

with open(f"result1.json", "w") as file_stream:
    json.dump(dictionary, file_stream)
    file_stream.write('\n')

frobenius_norm = np.linalg.norm(matrix, 'fro')
normalized_matrix = matrix / frobenius_norm
np.save('result1.npy', normalized_matrix)