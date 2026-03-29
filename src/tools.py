import os
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build

load_dotenv()

SERVICE_ACCOUNT_FILE = 'service_account.json'

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

SHEET_ID = os.getenv("SPREADSHEET_ID")
SHEET_NAME = os.getenv("SHEET_NAME")
RANGE_NAME = f"{SHEET_NAME}!A1:Z20"

def get_authenticated_service():
    """Autentica usando una Service Account."""
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        raise FileNotFoundError(f"No se encontró el archivo {SERVICE_ACCOUNT_FILE}")
    
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    
    return build("sheets", "v4", credentials=creds)

def read_spreadsheet(spreadsheet_id: str, range_name: str) -> str:
    """Lee datos de un rango específico en una Google Sheet."""
    try:
        service = get_authenticated_service()
        sheet = service.spreadsheets()
        result = sheet.values().get(
            spreadsheetId=SHEET_ID, range=RANGE_NAME).execute()

        
        values = result.get("values", [])
        if not values:
            return "No se encontraron datos."
            
        return "\n".join([", ".join(map(str, row)) for row in values])
    except Exception as err:
        return f"Error al leer la hoja: {err}"

def update_spreadsheet(spreadsheet_id: str, range_name: str, values_list: list) -> str:
    """Modifica o añade datos en la hoja."""
    try:
        service = get_authenticated_service()
        body = {'values': values_list}
        result = service.spreadsheets().values().update(
            spreadsheetId=SHEET_ID, 
            range=RANGE_NAME,
            valueInputOption="USER_ENTERED", 
            body=body).execute()
            
        return f"Celdas actualizadas: {result.get('updatedCells')}"
    except Exception as err:
        return f"Error al actualizar: {err}"