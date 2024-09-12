Created this program to get push notifications using pushover api, instead of using smtplib and cluttering my emails even more. this program allows you to send text/image notificaitons with logging. Notifications are grouped by device. The example assumes you have a credentials.py file in the cwd
Usage: 

    device = "some-device"
    title = "test"
    message = "testing classes AGAIN"
    noti = Notification(credentials.pushOver_appToken, credentials.pushOver_userKey, device, title, message)
    result = noti.send_textNotification()

    print(f"Text notification result: {result}")

    logs = noti.notification_logs("pauls-iphone")
    print(f"\n\nNotification Logs: {logs}")