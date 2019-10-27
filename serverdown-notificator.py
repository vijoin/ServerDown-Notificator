import requests
from requests.exceptions import ConnectionError
import argparse

parser = argparse.ArgumentParser(description='Notify if a site is Down!')

### Receive sites and emails via CLI
parser.add_argument('-s', '--sites', nargs='+', help="i.e: -s http://127.0.0.1 http://domain.xyz")
parser.add_argument('-e', '--emails', nargs='+', help="i.e: -e myemail@domain.xyz myboss@domain.xyz")

### Receive sites and email from a file
parser.add_argument('-sf', '--sites-from-file', type=str, help='Pass the sites from a file')
parser.add_argument('-ef', '--emails-from-file', type=str, help='Pass the emails from a file')

args = parser.parse_args()


def send_notification(emails, site):
    for email in emails:
        print(f"""
        Hello {email.rstrip()}
        The Site {site} is down!""")


def _get_sites(f):
    return f.readlines()


def _get_emails(f):
    return f.readlines()


def main(**kwargs):
    if 'sites_from_file' in kwargs:
        print("OK")
        file_path = kwargs.get('sites_from_file')
        with open(file_path, 'r') as f:
            kwargs['sites'] = _get_sites(f)

    if 'emails_from_file' in kwargs:
        file_path = kwargs.get('emails_from_file')
        with open(file_path, 'r') as f:
            kwargs['emails'] = _get_emails(f)

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
