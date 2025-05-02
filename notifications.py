import requests
from datetime import datetime
import json
import os

class DataInteraction:
    def __init__(self):
        self.file = "notificationsSent.json"
        self.my_dict = self.__loadData__()
    def __loadData__(self):
        # if file doesnt exist create it
        if not os.path.exists(self.file):
                with open(self.file, 'w') as f:
                    json.dump({}, f)
        with open(self.file, 'r') as f:
            try:
                my_dict = json.load(f)
            except json.JSONDecodeError:
                my_dict = {}
        return my_dict
    
    def __writeData__(self):
        # Safely write the dictionary to the file
        try:
            with open(self.file, 'w') as f:
                json.dump(self.my_dict, f, indent=4)
        except IOError as e:
            print(f"Error writing to file: {e}")
            return False
        return True
    
class Notification(DataInteraction):
    def __init__(self, app_token=None, user_key=None):
        super().__init__()
        self.app_token = app_token
        self.user_key = user_key
        self.get_credentials()

    def get_credentials(self):
        if not self.app_token:
            self.app_token = os.environ.get('PUSHOVER_APP_TOKEN')
        if not self.user_key:
            self.user_key = os.environ.get('PUSHOVER_USER_KEY')

        if not self.app_token or not self.user_key:
            raise ValueError("App token and user key must both be set. Provide them or set them as environment variables.")

        return self.app_token, self.user_key
    def get_currentTime(self):
        current_time = datetime.now()

        # change to ('%Y-%m-%d %I:%M:%S %p') for 12hr time format         
        return current_time.strftime('%Y-%m-%d %H:%M:%S')
    def send_textNotification(self, device=None, title="", message=""):
        url = "https://api.pushover.net/1/messages.json"
        current_time = self.get_currentTime()

        data = {
            "token" : self.app_token,
            "user" : self.user_key,
            "message" : message,
            "title" : title,
            "device" : device
        }

        if device:
            data["device"] = device

        try:
            response = requests.post(url, data=data)
            if response.status_code == 200:

                log_key = device if device else 'all-devices'

                if log_key not in self.my_dict:
                    self.my_dict[log_key] = []
                
                self.my_dict[log_key].append({
                    "time sent" : current_time,
                    "title" : title,
                    "message" : message
                })
                self.__writeData__()
                return 1
        except Exception as e:
            return f"{e}"
    def send_imageNotification(self, device=None, title="", message="", images=None):
        url = "https://api.pushover.net/1/messages.json"
        current_time = self.get_currentTime()

        data = {
            "token" : self.app_token,
            "user" : self.user_key,
            "message" : message,
            "title" : title,
            "device" : device
        }
        files = {
            "attachment": (images, open(images, 'rb'), "image/jpeg")
        }

        if device:
            data["device"] = device
        try:
            response = requests.post(url, data=data, files=files)
            if response.status_code == 200:

                log_key = device if device else 'all-devices'

                if log_key not in self.my_dict:
                    self.my_dict[log_key] = []
                
                self.my_dict[log_key].append({
                    "time sent" : current_time,
                    "title" : title,
                    "message" : message,
                    "image" : images
                })
                self.__writeData__()
                return 1
        except Exception as e:
            return f"{e}"
    def notification_logs(self, device_name=None):
        # returns logs for speicfied devices or logs for notifications sent to device: all-devices
        if device_name:
            return self.my_dict.get(device_name, f"No logs found for device: {device_name}")
        #returns all logs 
        return self.my_dict