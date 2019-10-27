import requests
from requests.exceptions import ConnectionError
import argparse

parser = argparse.ArgumentParser(description='Notify if a site is Down!')
parser.add_argument('-s', '--sites', nargs='+', help="i.e: -s http://127.0.0.1 http://domain.xyz", required=True)
parser.add_argument('-e', '--emails', nargs='+', help="i.e: -e myemail@domain.xyz myboss@domain.xyz", required=True)
args = parser.parse_args()


def send_notification(emails, site):
    for email in emails:
        print(f"""
        Hello {email}
        The Site {site} is down!""")


def main(sites, emails):
    for site in sites:
        try:
            r = requests.get(f'{site}', timeout=5)
            if r.status_code != 200:
                send_notification(emails, site)
        except ConnectionError:
            print("\nConnection Error\n")
            send_notification(emails, site)


if __name__ == '__main__':
    main(**vars(args))
