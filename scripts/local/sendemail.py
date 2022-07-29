import os
import logging
import argparse

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from taptools import configure_logging
from taptools import send_alert


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--from_email', help='Source email address', required=True)
    parser.add_argument('--to_emails', help='Target email addresses separated by a space', required=True, nargs='+')
    parser.add_argument('--subject', help='Email subject', required=True)
    parser.add_argument('--html_content', help='HTML content for email', required=True)
    parser.add_argument('--logs_path', help='Path to logs', required=True)
    parser.add_argument('--triggering_app', help='pTriggeringApp', required=True)

    args = parser.parse_args()

    configure_logging(app=args.triggering_app)

    sg = SendGridAPIClient(os.environ['SENDGRID_API_KEY'])

    message = Mail(
        from_email=args.from_email,
        to_emails=args.to_emails,
        subject=args.subject,
        html_content=args.html_content)
    try:
        response = sg.send(message)
        logging.info(response.status_code)
        logging.info(response.body)
        logging.info(response.headers)
    except Exception:
        message = 'Unable to send email'
        send_alert(message, alert_high=False)
        logging.exception(message)


if __name__ == '__main__':
    main()
