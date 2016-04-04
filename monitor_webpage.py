import requests  
import time  # time.sleep
import sys # sys.stdout.flush

import getpass

import smtplib
from email.mime.text import MIMEText

email = 'EMAIL@ADDRESS'


def loop_watcher(url):
    not_updated = True
    req = requests.head(url)
    req_mod_date = req.headers["Last-Modified"]
    print("Last updated: ", req_mod_date)

    print('Need email credentials... \n')
    login = input('Login: ')
    psswd = getpass.getpass()
    
    print("Watching: ", url, "\n")

    while not_updated:
        print('.', end='')

        new_req = requests.head(url)
        new_req_mod_date = req.headers["Last-Modified"]

        if req_mod_date != new_req_mod_date:
            not_updated = False

            notice = 'Site updated: '
            notice += new_req_mod_date
            print(notice)
            
            email_notice(notice, login, psswd)
        else:
            sys.stdout.flush()
            time.sleep(600) # 600 seconds == 10 minutes

    print("Terminating watch.")

def email_notice(notice, login, psswd):
    msg = MIMEText(notice)

    msg['Subject'] = notice
    msg['From'] = email
    msg['To'] = email

    s = smtplib.SMTP('localhost')
    s.login(login, psswd)
    s.send_message(msg)
    s.quit()


if __name__ == '__main__':
    url = 'http://url/page.html'
    loop_watcher(url)
