import matplotlib.pyplot as plt
import seaborn as sns

def plot_linear(data, col1, col2, name):
	sns.lineplot(data=data, x=col1, y=col2, errorbar=None)
	plt.title('Линейный график')
	plt.savefig(f'results\{name}.png')