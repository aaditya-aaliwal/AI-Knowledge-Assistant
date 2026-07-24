
from app.config import settings

def print_app_info():
    print(f"Application Name    : {settings.APP_NAME}")
    print(f"Application Version : {settings.APP_VERSION}")
    print(f"Debug Mode          : {settings.DEBUG}")
    
