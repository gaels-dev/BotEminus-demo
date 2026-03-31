import os
import json
import requests
import time

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# =========================
# VARIABLES
# =========================
load_dotenv()

USUARIO = os.getenv("EMINUS_USER")
PASSWORD = os.getenv("EMINUS_PASS")
BOT_TOKEN = os.getenv("TG_TOKEN")
CHAT_ID = os.getenv("TG_CHAT_ID")

URL = "https://eminus.uv.mx"
DASHBOARD_URL = "https://eminus.uv.mx/eminus4/page/course/list"

# =========================
# TELEGRAM
# =========================
def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": mensaje})

# =========================
# HISTORIAL
# =========================
def cargar_historial():
    try:
        with open("tareas.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def guardar_historial(data):
    with open("tareas.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# =========================
# NAVEGADOR
# =========================
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 15)

driver.get(URL)

# =========================
# LOGIN
# =========================
wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(USUARIO)
driver.find_element(By.NAME, "password").send_keys(PASSWORD + Keys.ENTER)

# esperar cursos
wait.until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "mat-card.CourseCard .CardHeaderContainer b"))
)

# =========================
# PROCESAR CURSOS
# =========================
historial = cargar_historial()
nuevas_global = []

titulos = driver.find_elements(By.CSS_SELECTOR, "mat-card.CourseCard .CardHeaderContainer b")
total = len(titulos)

for i in range(total):

    titulos = wait.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "mat-card.CourseCard .CardHeaderContainer b")
        )
    )

    titulo = titulos[i]
    nombre = titulo.text.strip()

    if not nombre:
        continue

    #print(f"\n📘 Entrando a: {nombre}")

    driver.execute_script("arguments[0].scrollIntoView();", titulo)

    try:
        driver.execute_script("arguments[0].click();", titulo)
    except:
        titulo.click()

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(
            (By.XPATH, "//span[contains(text(),'Actividades') or contains(text(),'Contenido')]")
        )
    )

    time.sleep(3)

    try:
        print(f"📘 Entrando a: {nombre}")

        actividades_btn = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//a[.//span[contains(text(),'Actividades')]]")
            )
        )
        driver.execute_script("arguments[0].click();", actividades_btn)

        time.sleep(2)

        # Cambiar al iframe real
        iframe = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "iframe"))
        )
        driver.switch_to.frame(iframe)

        # Esperar a que aparezcan los títulos
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h5.card-title"))
        )

        # Guardar HTML renderizado para inspección
        with open("debug.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)

        # Capturar títulos
        titulos_act = driver.find_elements(By.CSS_SELECTOR, "h5.card-title")
        tareas_actuales = [t.text.strip() for t in titulos_act if t.text.strip()]

        print("📄 Tareas encontradas:", tareas_actuales)

    except Exception as e:
        print(f"Error en {nombre}: {repr(e)}")
        tareas_actuales = []

    finally:
        driver.switch_to.default_content()

    tareas_guardadas = historial.get(nombre, [])
    nuevas = list(set(tareas_actuales) - set(tareas_guardadas))

    if nuevas:
        for t in nuevas:
            nuevas_global.append(f"{nombre} → {t}")

    historial[nombre] = tareas_actuales

    driver.get(DASHBOARD_URL)
    wait.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "mat-card.CourseCard .CardHeaderContainer b")
        )
    )

# =========================
# NOTIFICAR
# =========================
if nuevas_global:
    mensaje = "📚 NUEVAS TAREAS DETECTADAS:\n\n"
    mensaje += "\n".join(f"• {t}" for t in nuevas_global)
    enviar_telegram(mensaje)
    print("\nTiene tareas nuevas, revise su bot de telegram...")
else:
    print("\nNo tiene tareas nuevas...")

# =========================
# GUARDAR HISTORIAL
# =========================
guardar_historial(historial)

driver.quit()