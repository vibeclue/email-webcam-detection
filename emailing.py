import smtplib
import filetype
from email.message import EmailMessage

SENDER = 'asdf@gmail.com'
PASSWORD = 'password'

def send_email(image_path):
    email_msg = EmailMessage()
    email_msg["Subject"] = "New person showed up!"
    email_msg.set_content("Hey, there is a new person showed up!")

    with open(image_path, 'rb') as image:
        content = image.read()
    email_msg.add_attachment(content, maintype='image', subtype=filetype.guess(content))

    gmail = smtplib.SMTP('smtp.gmail.com', 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(SENDER, PASSWORD)
    gmail.sendmail(SENDER, SENDER, email_msg.as_string())
    gmail.quit()

if __name__ == '__main__':
    send_email('images/test.png')