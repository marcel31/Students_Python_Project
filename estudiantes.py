import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Cargo el archivo CSV con las calificaciones de los estudiantes
df = pd.read_csv('calificaciones_estudiantes_trimestres.csv', index_col=0)

# Convierto las columnas de las notas a numéricas y redondeo a 2 decimales
asignaturas = ['Matemáticas', 'Inglés', 'Ciencias', 'Historia', 'Arte']
for asignatura in asignaturas:
    for trimestre in ['T1', 'T2', 'T3']:
        columna = f'{asignatura}_{trimestre}'
        df[columna] = pd.to_numeric(df[columna], errors='coerce').round(2)

# Elimino las filas con valores nulos
df = df.dropna()

# Agrupo por grupo de edad y género y calculo estadísticas
grouped = df.groupby(['Edad', 'Género']).agg({
    **{f'{asignatura}_{trimestre}': ['mean', 'median', 'std'] for asignatura in asignaturas for trimestre in ['T1', 'T2', 'T3']}
})

# Guardo el informe en un archivo CSV
grouped.to_csv('informe_estadisticas.csv', index=False)

# Muesto el informe en consola
print(grouped)

# Gráficos de líneas para las notas de cada estudiante en cada trimestre
for asignatura in asignaturas:
    # Ajusto el tamaño del gráfico
    plt.figure(figsize=(8, 5))
    x = np.array([1, 2, 3])
    for i, row in df.iterrows():
        y = np.array([row[f'{asignatura}_T1'], row[f'{asignatura}_T2'], row[f'{asignatura}_T3']])
        plt.plot(x, y, 'o-', label=f'{row.Nombre}')

    plt.title(f'{asignatura}')
    plt.xlabel('Trimestre')
    plt.ylabel('Nota')
    
    # Ajusto los ticks del eje X para mostrar valores enteros
    plt.gca().xaxis.set_major_locator(plt.MaxNLocator(integer=True))
    # Ajusto los ticks del eje Y para mostrar 1 decimal
    plt.gca().yaxis.set_major_formatter(plt.FormatStrFormatter('%.1f'))
    
    # Ajusto los ticks del eje Y para mostrar valores de 0.1 en 0.1
    y_ticks = np.arange(5, 10, 0.1)
    plt.gca().set_yticks(y_ticks)
    
    # Pongo la leyenda fuera del gráfico
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5)) 
    plt.grid(True)
    plt.show()
