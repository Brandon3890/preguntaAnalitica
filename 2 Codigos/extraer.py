import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

#De Octubre 2025
URLCOMUNAS = "https://bidat.gob.cl/details/ficha/dataset/bases-de-datos-octubre-2025"
URLMUNIS = "https://presupuestoabierto.gob.cl/municipalities"

#Carpetas
CARPETA_D = os.path.abspath("1 Fuentes")
os.makedirs(CARPETA_D, exist_ok=True)

# =========================================================
# CONFIGURACIÓN DE CHROME
# =========================================================

options = Options()
options.add_argument("--headless=new")
options.add_argument("--window-size=1920,1080")

prefs = {
    "download.default_directory": CARPETA_D,
    "download.prompt_for_download":False,
    "download.directory_upgrade":True,
}

options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), 
    options=options
)

wait = WebDriverWait(driver, 10)

# =========================================================
# DESCARGAR COMUNAS
# =========================================================

def descargar_comunas():
    driver.get(URLCOMUNAS)
    
    #Comenzar recorrido por la pagina
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    #Esperar hasta encontrar el nombre coincidente que contiene el documento
    fila = wait.until(
        EC.presence_of_element_located(( 
            By.XPATH,
            "//tr[.//text()[contains(., 'IGVUST a nivel comunal')]]"
        ))
    )
    
    boton = fila.find_element(
        By.XPATH, 
        ".//a[contains(@title, 'Descargar')]"
    )
    
    
    driver.execute_script("arguments[0].scrollIntoView(true);", boton)
    time.sleep(1)
    boton.click()
    
    print("Se esta descargando comunas")
    time.sleep(8)

# =========================================================
# DESCARGAR MUNIS
# =========================================================

def descargar_munis():
    driver.get(URLMUNIS)
    
    #Comenzar recorrido por la pagina
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    boton_icono = wait.until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//div[contains(@class,'downloads')]//a[contains(normalize-space(.), 'CSV')]"
            
        ))
    )
    
    driver.execute_script("arguments[0].scrollIntoView(true);", boton_icono)
    time.sleep(1)
    boton_icono.click()
    
    print("Se esta descargando munis")
    time.sleep(5)

# =========================================================
# Ejecutar 
# =========================================================

try:
    descargar_comunas()
    descargar_munis()
finally:
    driver.quit()
    
print("Se descargo todo")