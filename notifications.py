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
    def __init__(self, app_token, user_key, device_name, title, message):
        super().__init__()
        self.app_token = app_token
        self.user_key = user_key
        self.time_sent = ""
        self.device_name = device_name
        self.title = title
        self.message = message
    def send_textNotification(self):
        url = "https://api.pushover.net/1/messages.json"
        token = self.app_token
        key = self.user_key
        sent_time = self.time_sent
        device = self.device_name
        title = self.title
        message = self.message
        current_time = datetime.now()
        sent_time = current_time.strftime('%Y-%m-%d %H:%M:%S')

        data = {
            "token" : token,
            "user" : key,
            "message" : message,
            "title" : title,
            "device" : device
        }

        try:
            response = requests.post(url, data=data)
            if response.status_code == 200:
                if device not in self.my_dict:
                    self.my_dict[device] = []
                
                self.my_dict[device].append({
                    "time sent" : sent_time,
                    "title" : title,
                    "message" : message
                })
                self.__writeData__()
                return 1
        except Exception as e:
            return f"{e}"
    def send_imageNotification(self, images):
        url = "https://api.pushover.net/1/messages.json"
        token = self.app_token
        key = self.user_key
        sent_time = self.time_sent
        device = self.device_name
        title = self.title
        message = self.message
        current_time = datetime.now()
        sent_time = current_time.strftime('%Y-%m-%d %H:%M:%S')

        data = {
            "token" : token,
            "user" : key,
            "message" : message,
            "title" : title,
            "device" : device
        }
        files = {
            "attachment": (images, open(images, 'rb'), "image/jpeg")
        }


        try:
            response = requests.post(url, data=data, files=files)
            if response.status_code == 200:
                if device not in self.my_dict:
                    self.my_dict[device] = []
                
                self.my_dict[device].append({
                    "time sent" : sent_time,
                    "title" : title,
                    "message" : message,
                    "image" : images
                })
                self.__writeData__()
                return 1
        except Exception as e:
            return f"{e}"
    def notification_logs(self, device_name=None):
        if device_name:
            return self.my_dict.get(device_name, f"No logs found for device: {device_name}")
        return self.my_dict