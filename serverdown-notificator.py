import requests
from requests.exceptions import ConnectionError


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
    sites = ('http://127.0.0.1',)
    emails = ('a@a.com',)
    main(sites=sites, emails=emails)
