import os
os.system("cls")
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import glob

print("Primer cambio para comprobar local a remoto")

#\\<=>=//#||''
archis = glob.glob("C:/Python/Aanalisis_Data/Reto_Nivel_02/*.csv")

archis_unidos = []
errores = []

for archivo in archis:
    df = pd.read_csv(archivo)

    df = df.copy()
    print(f"Lectura del Archivo: {archivo}")

    ## Sección Limpieza
    df["Salario"] = df["Salario"].astype(str).str.replace(r"[^\d.]", "", regex=True)

    df["Edad"] = pd.to_numeric(df["Edad"], errors = "coerce")
    df["Salario"] = pd.to_numeric(df["Salario"], errors = "coerce")

    ## Sección errores
    error = df[df["Edad"].isnull() | df["Salario"].isnull()]
    errores.append(error)

    ## Sección de eliminación
    df = df.dropna(subset = ["Edad", "Salario"])  
    df = df[df["Edad"] >= 18 ]

    ## Seccion Departamental
    df["Departamento"] = df["Departamento"].str.upper().str.strip()

    ## Corrección de nombres inconsistentes
    df["Departamento"] = df["Departamento"].replace({
    "RH" : "RECURSOS HUMANOS",
    "IT" : "TECNOLOGIA",
    })

    ## Eliminar duplicados y Nulos
    df = df.drop_duplicates()
    df = df.dropna()

    ## Archivo limpio
    archis_unidos.append(df)


print()
print("El reporte limpio final es:")
archis_final = pd.concat(archis_unidos, ignore_index = True)
print(archis_final)
print()
print("El reporte de errores es:")
errors_final = pd.concat(errores, ignore_index = True)
print(errors_final)
print()
## 5.-Guardar resultados
#archis_final.to_csv("Archivo_final.csv", index = False)
#print(os.getcwd())
## Guardar errores
#errors_final.to_csv("Errores_final.csv", index = False)

## Detección de Outliers
# Esto detecta salarios sospechosos
"""
plt.figure()
archis_final["Salario"].plot(kind="box")
plt.title("Detección de Outliers en Salario")
plt.ylabel("Salario")
plt.show()

q1 = archis_final["Salario"].quantile(0.25)
q3 = archis_final["Salario"].quantile(0.75)

iqr = q3 - q1

outliers = archis_final[
    (archis_final["Salario"] < q1 - 1.5*iqr) |
    (archis_final["Salario"] > q3 + 1.5*iqr)
]

print("\nOutliers detectados:")
print(outliers)
print()
"""

#🟦 1. Empleados por departamento

archis_final["Departamento"].value_counts().plot(kind="bar")
plt.title("Empleados por Departamento")
plt.xlabel("Departamento")
plt.ylabel("Cantidad de empleados")
plt.show()


#🟥 2. Salario promedio por departamento
"""
archis_final.groupby("Departamento")["Salario"].mean().plot(kind="bar")
plt.xlabel("Departamento")
plt.ylabel("Salarium")
plt.title("Puro Pudiente")
plt.show()
"""

#🟩 3. Distribución de salarios
"""
archis_final["Salario"].plot(kind="hist", bins=10)
plt.xlabel("Cantidad")
plt.ylabel("Salario")
plt.title("Distribución de Salarios")
plt.show()
"""

## Reporte ejecutivo
dep_salarios = archis_final.groupby("Departamento")["Salario"].mean()
dep_menor = dep_salarios.idxmin()
print("REPORTE EJECUTIVO")
print(f"El departamento con más empleados es: \n{archis_final['Departamento'].value_counts().idxmax()}")
print("Para reducir la carga de trabajo de los departamentos con pocos empleados, se debe contratar más personal")
print(f"EL salario promedio es: \n{archis_final['Salario'].mean()}  ")
print(f"{dep_menor} tiene menor promedio salarial")
print()

## Guardar Reporte ejecutivo
"""
with open("reporte.txt", "w") as f:
    f.write(f"Departamento con más empleados: {archis_final['Departamento'].value_counts().idxmax()}\n")
    f.write(f"Salario promedio: {archis_final['Salario'].mean()}\n")
    f.write(f"Departamento con menor salario: {dep_menor}\n")
"""

## Insight
# Conclusiones
print("CONCLUSIONES")
print("RH y Tecnología tienen los sueldos más grandes, debe analizarse el porqué de esto")
print(dep_salarios.sort_values(ascending=False))
print("Se detectaron outliers")
print("VENTAS tiene el menor promedio salarial, debe de realizarse un aumento, debido a ser el dto. donde vienen las ganancias")
print("El promedio de salario debe revisarse, ya que no logra visualizarse del todo, los rangos altos de salario")
