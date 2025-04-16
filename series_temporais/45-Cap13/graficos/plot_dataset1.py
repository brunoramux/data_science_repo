# Gráfico da Série Temporal Univariada

# Imports
import pandas as pd
import matplotlib.pyplot as plt

# Carrega os dados do arquivo CSV
data = pd.read_csv('../datasets/dataset1.csv', parse_dates=['Data'], index_col='Data')

# Plot da série temporal
plt.figure(figsize=(12, 6))
plt.plot(data.index, data['ConsumoEnergia'], marker='o', linestyle='-')
plt.title('Consumo de Energia ao Longo do Tempo')
plt.xlabel('Data')
plt.ylabel('Consumo de Energia')
plt.grid(True)
plt.show()
