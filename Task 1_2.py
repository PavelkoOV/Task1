import sqlite3
import smtplib
from email.mime.multipart import MIMEMultipartж
from email.mime.text import MIMEText
from datetime import datetime, timedelta

# Налаштування бази даних і поштового серверу
DATABASE = 'database.db'
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SMTP_USER = 'email@gmail.com'
SMTP_PASSWORD = 'your_password'
REC_EMAIL = 'recipient_email@gmail.com'

def send_email(subject, body):
    msg = MIMEMultipart()
    msg['From'] = SMTP_USER
    msg['To'] = REC_EMAIL
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(SMTP_USER, SMTP_PASSWORD)
    text = msg.as_string()
    server.sendmail(SMTP_USER, REC_EMAIL, text)
    server.quit()

# Створення 2-х типыв запитів згідно тасків
def get_dialogs(user_id, start_date=None):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    if start_date:
        query = '''SELECT * FROM dialogs WHERE user_id = ? AND last_message_date >= ?'''
        cursor.execute(query, (user_id, start_date))
    else:
        query = '''SELECT * FROM dialogs WHERE user_id = ?'''
        cursor.execute(query, (user_id,))

    rows = cursor.fetchall()
    conn.close()
    return rows

def main():
    user_id = 12345

    # Всі діалоги користувача з ID 12345
    dialogs = get_dialogs(user_id)
    dialogs_info = "\n".join([str(dialog) for dialog in dialogs])
    send_email('All Dialogs for User ID 12345', dialogs_info)

    # Всі діалоги користувача з ID 12345 за тиждень з новими повідомленнями
    last_week = datetime.now() - timedelta(days=7)
    dialogs_last_week = get_dialogs(user_id, last_week.strftime('%Y-%m-%d'))
    dialogs_last_week_info = "\n".join([str(dialog) for dialog in dialogs_last_week])
    send_email('Dialogs with New Messages for Last Week', dialogs_last_week_info)

if __name__ == '__main__':
    main()
