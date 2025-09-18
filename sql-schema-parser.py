import re

def extraer_tablas_y_columnas(sql_string):
    """
    Analiza un string de SQL para extraer las tablas y las columnas utilizadas en cada una.

    Args:
        sql_string (str): Un string que contiene una o más sentencias SQL.

    Returns:
        dict: Un diccionario donde las claves son los nombres de las tablas
              y los valores son listas de las columnas utilizadas para cada tabla.
    """
    # Expresión regular para encontrar las tablas (buscando después de FROM y JOIN)
    # y capturar todo el bloque de la consulta para esa tabla.
    # Usamos re.DOTALL para que '.' incluya saltos de línea.
    regex_tablas = re.compile(r"FROM\s+([\w\d_]+)|JOIN\s+([\w\d_]+)", re.IGNORECASE)

    # Dividimos el string en sentencias individuales por si hay más de una.
    sentencias = sql_string.strip().split(';')

    resultado_final = {}

    for sentencia in sentencias:
        if not sentencia.strip():
            continue

        # Encontrar todas las tablas en la sentencia actual
        tablas_encontradas = [tabla[0] or tabla[1] for tabla in regex_tablas.finditer(sentencia)]
        if not tablas_encontradas:
            continue
        
        # Asumimos que la primera tabla encontrada después de FROM es la principal de esta sentencia
        tabla_principal = tablas_encontradas[0]
        if tabla_principal not in resultado_final:
            resultado_final[tabla_principal] = []

        # Expresión regular para encontrar las columnas.
        # Busca palabras que son parte de SELECT, GROUP BY, o dentro de funciones como SUM().
        # \b asegura que solo capturemos palabras completas.
        # Se excluyen palabras clave comunes que no son columnas.
        regex_columnas = re.compile(
            r"\b(?!SELECT|FROM|GROUP|BY|AS|CASE|WHEN|THEN|ELSE|END|SUM|ON|JOIN|INNER|LEFT|RIGHT\b)\w+\b",
            re.IGNORECASE
        )

        # Extraer todas las posibles columnas de la sentencia
        columnas_potenciales = regex_columnas.findall(sentencia)

        # Limpiamos y añadimos las columnas encontradas al diccionario.
        # Usamos un set para evitar duplicados.
        columnas_actuales = set(resultado_final[tabla_principal])
        for col in columnas_potenciales:
            columnas_actuales.add(col)
        
        resultado_final[tabla_principal] = sorted(list(columnas_actuales))

    return resultado_final

# String de ejemplo proporcionado
sql_query = """
 SELECT numanio, numsemana, num_periodo, dia, SUM(gastos) AS suma_gastos
 FROM tabla_1
 GROUP BY numanio, numsemana, num_periodo, dia;

 SELECT fecha, CASE WHEN consumo > 100 THEN 'exceso' ELSE 'no exceso' END AS presupuesto
 FROM tabla_2;
"""

# Llamamos a la función e imprimimos el resultado
tablas_y_columnas = extraer_tablas_y_columnas(sql_query)
print(tablas_y_columnas)