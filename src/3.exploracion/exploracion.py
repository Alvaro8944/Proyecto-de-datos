import matplotlib.pyplot as plt
import seaborn as sns

def correlacion(data):
    correlation_matrix = df.corr()
    correlation_matrix
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Matriz de correlación')
    plt.show()