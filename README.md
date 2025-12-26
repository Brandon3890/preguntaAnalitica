# Análisis de vulnerabilidad municipal Región Metropolitana - Octubre 2025

Este caso tiene como objetivo analizar el nivel de vulnerabilidad socioterritorial de las comunas de la Región Metropolitana, tanto rural, mixta o urbana, en relación con el gasto municipal total y el gasto promedio por habitante. Con el fin de identificar brechas territoriales y posibles casos críticos en la asignación de recursos en Octubre del 2025. 



# Fuente de datos:

    Bases de datos con información del Índice Global de Vulnerabilidad Socioterritorial (IGVUST):
        https://bidat.gob.cl/details/ficha/dataset/bases-de-datos-octubre-2025

    Monitor de Gasto Municipal Octubre 2025
        https://presupuestoabierto.gob.cl/municipalities


# Limpieza y transformación de datos 

-Me centro en la Región Metropolitana 

-Me aseguro de que los códigos por comuna y región cumplan con el estándar chileno de, región dos números y comuna cinco números.

-Para mejor claridad, estandarizo los nombres de las columnas de los gastos municipales, para que sean consistentes con la base de vulnerabilidades.

-Creación de la columna “gasto_por_habitante” que se refiere al gasto de la municipalidad dividido en la población de cada una

-Creación de funcionalidad para identificar vulnerabilidades por unidad vecinal 

-Antes de terminar y exportar me aseguro de que “gasto_por_habitante” y “gasto_por_hogar” sean redondeados a solo un decimal 


# Dashboard 

-Se crean indicadores mostrando los datos importantes de la Región Metropolitana, como el recuento de las comunas, la cantidad total de habitantes, el gasto total municipal y un promedio de gasto por habitante

- ¿Dónde está concentrada la población según su nivel de vulnerabilidad? 

Gráfico: “cantidad de población por nivel de vulnerabilidad”

- ¿Qué comunas concentran mayor gasto municipal y en qué nivel de vulnerabilidad están? 

Treemap: “Comunas que más gastan por nivel de vulnerabilidad”

- ¿Influye el tipo de comuna (Urbana, mixta, rural) en el patrón de gasto y vulnerabilidad ? 

Barras apiladas: “Gasto por tipo de comuna y nivel de vulnerabilidad”

- ¿Dónde están territorialmente las comunas más vulnerables dentro de la Región Metropolitana?

Mapa: “Comunas por nivel de vulnerabilidad”

- ¿Existe relación entre el nivel de vulnerabilidad de las comunas, el gasto municipal por habitante y el tamaño de su población dentro de la Región Metropolitana? 

Gráfico de dispersión: “Distribución de nivel de vulnerabilidad por cantidad de comunas” 


# Ejecución de código

- Instalacion de ambiente virtual 

    pip install pipenv 
    

Luego, desde el directorio donde se encuentra el archivo Pipfile, ejecuta

    pipenv install  

- Carpeta “2 Codigos”

    cd ./2\ Codigos

    pipenv run python extraer.py

    pipenv run python transformacion.py

 


# Notas adicionales 

-Recomiendo instalar el navegador de Chrome para realizar el web scraping 

-Inicialmente el dashboard lo hice en Power BI, pero por temas de licencia en mi cuenta con Microsoft 365 no pude compartirlo en la web, así que lo realicé en Looker Studio. De todas formas, dejaré el archivo de Power BI y el enlace al dashboard en Looker Studio.

-El código extraer.py crea una carpeta llamada “1 Fuentes”

-El código transformacion.py crea una carpeta llamada “3 exportado”
