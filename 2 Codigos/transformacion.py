import pandas as pd
from pathlib import Path 


#=====================
# Configuracion para rutas de datos y archivos
#=====================

SCRIPT_DIR = Path(__file__).parent.absolute()
PROJECT_ROOT = SCRIPT_DIR.parent
INPUT_DIR = PROJECT_ROOT / "1 Fuentes"
OUTPUT_DIR = PROJECT_ROOT / "3 Exportado"
OUTPUT_DIR.mkdir(exist_ok=True)

#Voy a enfocarme solo en la region metropolitana 
REGION_METROPOLITANA = '13'



#=====================
# Cargar datos
#=====================
#==================Bases de datos con información del Índice Global de Vulnerabilidad Socioterritorial (IGVUST)==================
df_igvust = pd.read_csv(
    INPUT_DIR / "202510_igvust_comunal_cuartil.csv",
    sep=';',
    decimal=',',
    encoding='utf-8',
    dtype={'cod_com':str, 'cod_reg': str}
)

df_igvust = df_igvust.rename(columns={
    'c_ig_nac': 'cuartil_vulnerabilidad_nacional',
    'pob_rsh_com': 'poblacion_rsh',
    'hog_com': 'hogares_rsh',
    'p_cobertura_com': 'cobertura_rsh_porcentaje',
    'Clasificación': 'tipo_comuna'
})

#Asegurar formato de los codigos - los proceso mejor
df_igvust['cod_com'] = df_igvust['cod_com'].astype(str).str.zfill(5)
df_igvust['cod_reg'] = df_igvust['cod_reg'].astype(str).str.zfill(2)

#filtrar por la region metropolitana 
df_igvust_rm = df_igvust[df_igvust['cod_reg']==REGION_METROPOLITANA].copy()

#==================Monitor de Gasto Municipal (MGM)==================
df_municipios = pd.read_csv(
    INPUT_DIR / 'municipios.csv',
    encoding='utf-8',
    dtype={'comuna':str, 'region': str}
)

df_municipios['comuna'] = df_municipios['comuna'].astype(str).str.zfill(5)
df_municipios['region'] = df_municipios['region'].astype(str).str.zfill(2)


df_municipios = df_municipios.rename(columns={
    'comuna': 'cod_com',
    'sum': 'gasto_total_municipalidad',
    'count': 'cantidad_transacciones'
})

df_municipios_rm = df_municipios[df_municipios['region']==REGION_METROPOLITANA].copy()

#=====================
# Funsionar y crear columnas
#=====================

df_completo = pd.merge(
    df_igvust_rm,
    df_municipios_rm[['cod_com', 'gasto_total_municipalidad', 'cantidad_transacciones']],
    on='cod_com',
    how='left'
)

#crear columnas
df_completo['gasto_por_habitante'] = (
    df_completo['gasto_total_municipalidad'] / df_completo['poblacion_rsh']
).round(0)

df_completo['gasto_por_hogar'] = (
    df_completo['gasto_total_municipalidad'] / df_completo['hogares_rsh']
).round(1)

#clasificar vulnerabilidades

def clasificar_vulnerabilidades(cuartil):
    try:
        cuartil = int(cuartil)
        if cuartil == 1:
            return 'Muy alta'
        elif cuartil == 2:
            return 'Alta'
        elif cuartil == 3:
            return 'Media'
        elif cuartil == 4:
            return 'Baja'
        else:
            return 'No clasifica'
    except:
        return 'No clasificada'
    
df_completo['nivel_vulnerabilidad'] = df_completo['cuartil_vulnerabilidad_nacional'].apply(clasificar_vulnerabilidades)


#clasificar para auditar por el gasto que de los habitantes

df_completo['es_caso_critico'] = 'NO'
mask_critico= (
    (df_completo['nivel_vulnerabilidad'].isin(['Muy alta', 'Alta'])) &
    (df_completo['gasto_por_habitante']  < 50000) #Estimacion para probar datos
) | (
    (df_completo['nivel_vulnerabilidad'].isin(['Baja'])) &
    (df_completo['gasto_por_habitante']  > 300000) #Estimacion para probar datos
)

df_completo.loc[mask_critico,'es_caso_critico'] = 'SI'



#=====================
# Exportar
#=====================

df_exportar = df_completo[[
    'cod_com', 'Comuna', 'Region', 'cod_reg',
    'cuartil_vulnerabilidad_nacional', 'nivel_vulnerabilidad',
    'poblacion_rsh', 'hogares_rsh', 'cobertura_rsh_porcentaje',
    'tipo_comuna', 'rank_nac',
    'gasto_total_municipalidad', 'gasto_por_habitante', 'gasto_por_hogar',
    'cantidad_transacciones', 'es_caso_critico'
]].copy()

#exportar el pimer analisis
df_exportar['gasto_por_habitante'] = df_exportar['gasto_por_habitante'].round(1)
df_exportar['gasto_por_hogar'] = df_exportar['gasto_por_hogar'].round(1)

df_exportar.to_csv(
    OUTPUT_DIR / "RM_analisis_eficiencia.csv",
    index=False,
    encoding='utf-8-sig',
    sep=';',
    decimal=','
)
