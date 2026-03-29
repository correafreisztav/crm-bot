### 🚀 Instalación Rápida
Sigue estos pasos para tener el bot corriendo localmente:

Clonar el repositorio:
```bash
git clone https://github.com/correafreisztav/crm-bot.git
cd crm-bot
```
Configurar el entorno:
```bash
python -m venv .venv
source .venv/bin/activate
uv sync
```
Configurar las variables:
Crea un archivo .env en la raíz y pega lo siguiente:

GOOGLE_CLOUD_PROJECT=response-bot
GOOGLE_CLOUD_LOCATION=us-central1
SPREADSHEET_ID=your-spreadsheet-id
SHEET_NAME=CRM General
AGENT_MODEL=gemini-2.5-flash
📊 Configuración de Google Sheets
El bot utiliza una Service Account para entrar a tu Excel.

Obtener la llave: Debes tener un archivo llamado service_account.json en la carpeta raíz.

Compartir el acceso: Abre tu Google Sheet, haz clic en Compartir y agrega el correo electrónico de tu Service Account (termina en @developer.gserviceaccount.com) con permiso de Editor.

### ☁️ Despliegue en la Nube (Cloud Run)
Para que el bot esté disponible 24/7 sin que tu computadora esté prendida, lo subimos a Google Cloud Run.

#### ⚠️ Requisitos Previos en Google Cloud
Antes de hacer el primer despliegue en un proyecto nuevo, asegúrate de habilitar las APIs y darle los permisos necesarios a la cuenta de servicio por defecto de Cloud Run (`TU_NUMERO_DE_PROYECTO-compute@developer.gserviceaccount.com`):

```bash
# Habilitar APIs
gcloud services enable run.googleapis.com secretmanager.googleapis.com cloudbuild.googleapis.com aiplatform.googleapis.com

# Dar permiso para hablar con Vertex AI
gcloud projects add-iam-policy-binding TU_PROJECT_ID \
    --member="serviceAccount:TU_NUMERO_DE_PROYECTO-compute@developer.gserviceaccount.com" \
    --role="roles/aiplatform.user"

Configuración de Seguridad
No subimos el archivo JSON a la nube. Lo guardamos en el Secret Manager:

Bash
gcloud secrets create GOOGLE_SHEETS_CREDENTIALS --data-file=\"service_account.json\"
Comando de Despliegue
Usamos ADK para subir todo automáticamente:

Bash
adk deploy cloud_run \\
  --project=response-bot \\
  --region=us-central1 \\
  --service_name=\"crm-behavioral-bot\" \\
  --with_ui \\
  ./src \\
  -- \\
  --set-secrets=\"SERVICE_ACCOUNT_JSON_DATA=GOOGLE_SHEETS_CREDENTIALS:latest\" \\
  --set-env-vars=\"SPREADSHEET_ID=your-spreadsheet-id,SHEET_NAME=CRM General\"

Acceso Público para que todos puedan entrar a la URL generada:

Bash
gcloud run services add-iam-policy-binding crm-behavioral-bot \\
    --region=us-central1 \\
    --member=allUsers \\
    --role=roles/run.invoker