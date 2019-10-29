import smtplib
import os
import requests
from requests.exceptions import ConnectionError
import argparse

EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
SENDER = EMAIL_ADDRESS

parser = argparse.ArgumentParser(description='Notify if a site is Down!')

group_site = parser.add_mutually_exclusive_group()
group_site.add_argument('-s', '--sites', nargs='+', help="i.e: -s http://127.0.0.1 http://domain.xyz")
group_site.add_argument('-sf', '--sites-from-file', type=argparse.FileType('r'), help='Pass the sites from a file')

group_email = parser.add_mutually_exclusive_group()
group_email.add_argument('-e', '--emails', nargs='+', help="i.e: -e myemail@domain.xyz myboss@domain.xyz")
group_email.add_argument('-ef', '--emails-from-file', type=argparse.FileType('r'), help='Pass the emails from a file')

args = parser.parse_args()


def send_notification(emails, site):
    with smtplib.SMTP('smtp.gmail.com', 25) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()

        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        subject = f'YOUR SITE {site} IS DOWN!'
        body = 'Make sure the server restarted and it is backed up'
        msg = f'Subject: {subject} \n\n{body}'

        smtp.sendmail(from_addr=SENDER, to_addrs=emails, msg=msg)
        print("### EMAIL SENT to  {} ###".format(', '.join(emails).replace('\n', '')))


def main(**kwargs):
    if kwargs.get('sites_from_file', None):
        kwargs['sites'] = kwargs['sites_from_file'].readlines()

    if kwargs.get('emails_from_file', None):
        kwargs['emails'] = kwargs['emails_from_file'].readlines()

    for site in kwargs['sites']:
        try:
            r = requests.get(f'{site.rstrip()}', timeout=5)
            if r.status_code != 200:
                send_notification(kwargs['emails'], site)
        except ConnectionError:
            print("\nConnection Error\n")
            send_notification(kwargs['emails'], site)


if __name__ == '__main__':
    main(**vars(args))
