"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel


import re
import pandas as pd  # type: ignore


def pregunta_01():
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.


    """

    #----------------- Leer informacion archivo ---------------------
    file_dir = 'files/input'
    file_name = "clusters_report.txt"
    file_path = f"{file_dir}/{file_name}"

    lines = get_file_lines(file_path)

    #------------------- Nombres columnas -------------------------

    col_nombres = get_col_nombres(lines)
    
    df = pd.DataFrame(columns=col_nombres)

    #----------------- Obtener contenido ---------------------
    inicio_contenido = 4
    real_row = -1
    obtener_contenido_dataframe(lines, col_nombres, df, inicio_contenido, real_row)

    #----------------- Formatear columnas df ---------------------
    formatear_columnas_dataframe(df)


    return df


# obtener cada linea del archivo
def get_file_lines(file_path):
    lines = []
    with open(file_path, encoding="utf-8") as f:
      for i, line in enumerate(f, start=1):
          lines.append(line)
    return lines

# Los nombres de las columnas estan en las dos primeras filas
# Algunos son nombres compuestos entonces juntamos el nombre de la primera fila con el correspondiente en la segunda
def get_col_nombres(lines):
    
    linea1 = re.split(r"\s{2,}", lines[0])
    linea2 = re.split(r"\s{2,}", lines[1])
    col_nombres = []

    for i in range(len(linea1)):
        a1 = linea1[i].strip().replace(' ', '_').lower() if i < len(linea1) else ''
        a2 = linea2[i].strip().replace(' ', '_').lower() if i < len(linea2) else ''

        if a1 == '' and a2 == '':
            continue

        col_nom = a1
        if a2 != '':
          col_nom = f"{col_nom}_{a2}"

        col_nombres.append(col_nom)
    return col_nombres

# para obtener el contenido:
# De separador utilizamos que sea mas de dos espacio
# Si el primer valor de la linea es numero, quiere decir que en esta linea tenemos el dato del cluster, cantidad, porcentaje, y primera linea de palabras clave
# Si no es numero, toda la fila es de palabras clave

def obtener_contenido_dataframe(lines, col_nombres, df, inicio_contenido, real_row):
    for i in range(inicio_contenido, len(lines)):
        line = re.split(r"\s{2,}", lines[i])

        if line and line[0].strip() == '':
            line = line[1:]

        if line and line[-1].strip() == '':
            line = line[:-1]

        if len(line) == 0:
            continue

        primera_col_int = pd.to_numeric(line[0], errors='coerce')  # intenta convertir a número

        if not pd.isna(primera_col_int):
            real_row = real_row + 1

            df.at[real_row, col_nombres[0]] = line[0]
            df.at[real_row, col_nombres[1]] = line[1]
            df.at[real_row, col_nombres[2]] = line[2]
            df.at[real_row, col_nombres[3]] = ' '.join(s.replace('\n', ' ') for s in line[3:])

        else:
            df.at[real_row, col_nombres[3]] = df.at[real_row, col_nombres[3]].strip() + ' ' + ' '.join(s.replace('\n', ' ') for s in line[0:])


#Formatear columnas del dataframe segun el requirimiento
def formatear_columnas_dataframe(df):
    df['cluster'] = df['cluster'].astype(int)    
    df['cantidad_de_palabras_clave'] = df['cantidad_de_palabras_clave'].astype(int)    
    df['porcentaje_de_palabras_clave'] = df['porcentaje_de_palabras_clave'].str.replace('%', '').str.replace(',', '.').astype(float)
    df['principales_palabras_clave'] = df['principales_palabras_clave'].str.replace('.', '').str.strip()
    df['principales_palabras_clave'] = df['principales_palabras_clave'].str.replace(', ', ',')
    df['principales_palabras_clave'] = df['principales_palabras_clave'].str.replace(',', ', ')

if __name__ == "__main__":
    pregunta_01()