Created this program to get push notifications using pushover api, instead of using smtplib and cluttering my emails even more. this program allows you to send text/image notificaitons with logging. Notifications are grouped by device. The example assumes you have a credentials.py file in the cwd
Usage: 

    device = "some-device"
    title = "test"
    message = "testing classes AGAIN"

    

    noti = Notification(credentials.pushOver_appToken, credentials.pushOver_userKey)
    result = noti.send_textNotification(device, title, message)

    print(f"Text notification result: {result}")

    # if you have 'test_image.jpeg' in cwd
    result = noti.send_textNotification(device, title, message, 'test_image.jpeg)

    logs = noti.notification_logs("some-device")
    print(f"\n\nNotification Logs: {logs}")