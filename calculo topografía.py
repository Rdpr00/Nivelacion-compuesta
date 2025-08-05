"""PROGRAMA PARA CALCULAR Y GRAFICAR LA TOPOGRAFÍA"""

import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd

def calcular_posiciones_electrodos(separacion: float, num_electrodos: int) -> tuple:
    """Calcula las posiciones de los electrodos en el perfil"""
    distancias = [round(separacion * i, 3) for i in range(num_electrodos)]
    return distancias, list(range(1, num_electrodos + 1))

# Ingreso de datos
a = float(input('Ingresa la abertura en m: '))
e = int(input('Ingresa la cantidad de electrodos: '))
cota1 = float(input('Ingresa la cota del primer electrodo (a.s.n.m.m.): '))

x, elec = calcular_posiciones_electrodos(a, e)

# Listas para almacenar datos
Va = []
Vint = []
Vf = []
empates = []  # Para registrar qué electrodos son empates

# Lectura de datos
i = 0
while i < e:
    print(f'\nElectrodo {i+1}/{e}:')
    lectura = input('Ingresa la lectura del estadal o "emp" para empate: ')
    
    if not Va:  # Primer electrodo
        Va.append(float(lectura))
        Vint.append(0.0)
        Vf.append(0.0)
        empates.append(False)
    elif lectura.lower() == 'emp':
        print(f'\nRegistro de empate para electrodo {i+1}:')
        lectura_ea = float(input('Ingresa lectura de empate estación actual: '))
        lectura_en = float(input('Ingresa lectura de empate estación nueva: '))
        Va.append(lectura_en)
        Vint.append(0.0)
        Vf.append(lectura_ea)
        empates.append(True)
    else:
        Va.append(0.0)
        Vint.append(float(lectura))
        Vf.append(0.0)
        empates.append(False)
    i += 1

# Ajuste para el último electrodo
Vf[-1] = Vint[-1]
Vint[-1] = 0.0

# Creación del DataFrame
df = pd.DataFrame({
    'Electrodo': elec,
    'Distancia (m)': x,
    'V_atras': Va,
    'V_intermedia': Vint,
    'V_adelante': Vf,
    'Es empate': empates,
    'H aparato': np.nan,
    'Cota': np.nan
})

# Cálculo de cotas y alturas de aparato
df.at[0, 'Cota'] = cota1
df.at[0, 'H aparato'] = df.at[0, 'V_atras'] + cota1

for i in range(1, len(df)):
    if df.at[i, 'Es empate']:
        # Para empates: Cota se calcula con H aparato anterior
        df.at[i, 'Cota'] = df.at[i-1, 'H aparato'] - df.at[i, 'V_adelante']
        # H aparato se calcula con Cota actual + V_atras
        df.at[i, 'H aparato'] = df.at[i, 'Cota'] + df.at[i, 'V_atras']
    else:
        # Para lecturas normales
        df.at[i, 'H aparato'] = df.at[i-1, 'H aparato']
        df.at[i, 'Cota'] = df.at[i, 'H aparato'] - df.at[i, 'V_intermedia'] - df.at[i, 'V_adelante']

df['Cota']=df['Cota']/100

# Exportación a Excel
df.to_excel("output-filename.xlsx", index=False)
print("\nEl archivo Excel ha sido creado exitosamente.")

# Gráfico
plt.figure(figsize=(10, 6))
plt.plot(df['Distancia (m)'], df['Cota'], '--', color='red', label='Perfil topográfico')
plt.xlabel('Distancia (m)')
plt.ylabel('Elevación (m.s.n.m.)')
plt.title('Perfil Topográfico de la Sección')
plt.grid(True)
plt.legend()

plt.show()

