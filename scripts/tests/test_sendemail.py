import os
import logging
import argparse
import unittest
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from taptools import configure_logging
from taptools import send_alert
from unittest.mock import patch, MagicMock
from io import StringIO
from scripts.local import sendemail
from scripts.local.sendemail import *

class TestSendEmailScript(unittest.TestCase):

    triggering_app = 'ops'

    @patch('scripts.local.sendemail.SendGridAPIClient')
    @patch('scripts.local.sendemail.send_alert')
    @patch('scripts.local.sendemail.logging')
    @patch('scripts.local.sendemail.configure_logging')
    @patch('argparse.ArgumentParser')
    def test_send_email_success(self, mock_arg_parser, mock_configure_logging, mock_logging, mock_send_alert, mock_sendgrid):
        # Arrange
        args = MagicMock()
        args.from_email = 'gurudamodharan@uber.com'
        args.to_emails = ['gurudamodharan@uber.com']
        args.subject = 'Code Coverage Sendemail.py'
        args.html_content = '<p>Code Coverage Sendemail.py</p>'
        args.logs_path = '/var/tm1/ops/logs'
        args.triggering_app = 'ops'
        sg_instance = MagicMock()
        mock_sendgrid.return_value = sg_instance
        mock_response = MagicMock()

        mock_arg_parser.return_value.parse_args.return_value = args
        mock_sendgrid.return_value.send.return_value.status_code = 200
        mock_logging.info.side_effect = print  # Redirect logging output to stdout

        with patch.dict(os.environ, {'SENDGRID_API_KEY': str(mock_sendgrid.return_value)}):
            # Act
            sendemail.main()

        # Assert
        mock_configure_logging.assert_called_once_with(app='ops')
        mock_sendgrid.assert_called_once_with(str(mock_sendgrid.return_value))
        #mock_sendgrid.return_value.send.assert_called_once()
        #mock_logging.info.assert_called_with()

    @patch('scripts.local.sendemail.SendGridAPIClient')
    @patch('scripts.local.sendemail.send_alert')
    @patch('scripts.local.sendemail.logging')
    @patch('scripts.local.sendemail.configure_logging')
    @patch('argparse.ArgumentParser')
    def test_send_email_failure(self, mock_arg_parser, mock_configure_logging, mock_logging, mock_send_alert, mock_sendgrid):
        # Arrange
        args = MagicMock()
        args.from_email = 'gurudamodharan@uber.com'
        args.to_emails = ['gurudamodharan@uber.com']
        args.subject = 'Code Coverage Sendemail.py'
        args.html_content = '<p>Code Coverage Sendemail.py</p>'
        args.logs_path = '/var/tm1/ops/logs'
        args.triggering_app = 'ops'
        sg_instance = MagicMock()
        mock_sendgrid.return_value = sg_instance
        mock_response = MagicMock()

        mock_arg_parser.return_value.parse_args.return_value = args
        mock_sendgrid.return_value.send.side_effect = Exception('Test Exception')
        mock_logging.exception.side_effect = print  # Redirect logging output to stdout

        with patch.dict(os.environ, {'SENDGRID_API_KEY': str(mock_sendgrid.return_value)}):
            # Act
            sendemail.main()

        # Assert
        mock_configure_logging.assert_called_once_with(app='ops')
        mock_sendgrid.assert_called_once_with(str(mock_sendgrid.return_value))
        mock_sendgrid.return_value.send.assert_called_once()
        mock_send_alert.assert_called_once_with('Unable to send email', alert_high=False)
        mock_logging.exception.assert_called_once_with('Unable to send email')

if __name__ == '__main__':
    unittest.main()