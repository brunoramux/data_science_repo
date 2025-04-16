# Gráfico da Série Temporal Multivariada

# Imports
import pandas as pd
import matplotlib.pyplot as plt

# Carrega os dados do arquivo CSV
data = pd.read_csv('../datasets/dataset2.csv', parse_dates=['Data'], index_col='Data')

# Cria uma figura e eixos para os gráficos
fig, ax1 = plt.subplots(figsize=(14, 7))

# Plot do Consumo de Energia
ax1.plot(data.index, data['ConsumoEnergia'], color='tab:blue', marker='o', linestyle='-', label='Consumo de Energia')
ax1.set_xlabel('Data')
ax1.set_ylabel('Consumo de Energia', color='tab:blue')
ax1.tick_params(axis='y', labelcolor='tab:blue')
ax1.grid(True)

# Cria um segundo eixo y para a Temperatura
ax2 = ax1.twinx()
ax2.plot(data.index, data['Temperatura'], color='tab:red', marker='x', linestyle='--', label='Temperatura')
ax2.set_ylabel('Temperatura (°C)', color='tab:red')
ax2.tick_params(axis='y', labelcolor='tab:red')

# Adiciona título e legendas
plt.title('Consumo de Energia e Temperatura ao Longo do Tempo')
fig.tight_layout()  # Para ajustar bem o layout
plt.show()
