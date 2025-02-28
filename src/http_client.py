import requests
from config import config
from logger import logger

class HTTPClient:
    def __init__(self, base_url='http://localhost:5000'):
        self.base_url = base_url
        self.session = requests.Session()
        
    def get_bci_data(self):
        """Získá aktuální data z BCI zařízení"""
        try:
            response = self.session.get(f"{self.base_url}/bci/data")
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Chyba při získávání BCI dat: {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"Chyba HTTP požadavku: {e}")
            return None
            
    def send_robot_command(self, command, speed=0.0):
        """Odešle příkaz robotovi"""
        try:
            data = {
                'command': command,
                'speed': speed
            }
            response = self.session.post(f"{self.base_url}/robot/command", json=data)
            if response.status_code == 200:
                return True
            else:
                logger.error(f"Chyba při odesílání příkazu robotovi: {response.status_code}")
                return False
        except Exception as e:
            logger.error(f"Chyba HTTP požadavku: {e}")
            return False
            
    def get_system_status(self):
        """Získá stav systému"""
        try:
            response = self.session.get(f"{self.base_url}/system/status")
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Chyba při získávání stavu systému: {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"Chyba HTTP požadavku: {e}")
            return None
