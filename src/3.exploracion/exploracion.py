import matplotlib.pyplot as plt
import seaborn as sns

def correlacion(data):
    """Muestra de forma gráfica la correlación entre las variables"""
    correlation_matrix = data.corr()
    correlation_matrix
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Matriz de correlación')
    plt.show()