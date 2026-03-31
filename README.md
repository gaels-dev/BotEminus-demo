# 📚 Eminus Bot-demo

Un bot en Python que automatiza la consulta de tareas en **Eminus** y envía notificaciones a través de **Telegram**.

---

## 🚀 Requisitos

- Tener instalado **Python 3.10+**
- Instalar las dependencias necesarias:
  ```bash
  pip install selenium python-dotenv requests


📥 Instalación
- Clona este repositorio.
- Crea tu bot de Telegram:
- Abre Telegram y busca @BotFather.
- Usa el comando /newbot para crear tu bot.
- Copia el token que te da BotFather.
- Obtén tu chat ID:
- Inicia una conversación con tu bot.
- Usa alguna herramienta como get_id_bot o revisa la API de Telegram para obtener tu chat_id.

⚙️ Configuración
- Copia el archivo .env.example y renómbralo a .env.
- Edita el archivo .env y coloca tus credenciales:
EMINUS_USER=tu_usuario
EMINUS_PASS=tu_password
TG_TOKEN=tu_token_de_telegram
TG_CHAT_ID=tu_chat_id

▶️ Uso
- Ejecuta el bot con:
- python eminus_bot.py
- Si todo está configurado correctamente, recibirás una notificación en tu bot de Telegram con tus tareas de Eminus.

🛡️ Notas
- El archivo .env no se sube al repositorio por seguridad.
- Usa siempre .env.example como guía para configurar tus credenciales.
- Este proyecto está pensado para uso personal y académico.
