import unittest
from unittest.mock import patch, MagicMock
from scripts.local.generic_process_call import main

class TestMainFunction(unittest.TestCase):

    def setUp(self):
        # Mocking the arguments for the main function
        self.args = MagicMock()
        self.args.server = 'localhost'
        self.args.port = '20000'
        self.args.user = 'admin'
        self.args.ssl = True
        self.args.password = 'test_password'
        self.args.namespace = 'test_CAMNamespace'
        self.args.process = 'process'
        self.args.pLogPath = 'log_path'
        self.args.parameter_dict = '{"param1":"value1"}'

    @patch('scripts.local.generic_process_call.json')
    @patch('argparse.ArgumentParser')
    @patch('scripts.local.generic_process_call.TM1Service')
    def test_generic_process_call_success(self, mock_tm1_service, mock_arg_parser, mock_json):
        # Arrange
        # Mocking the JSON data and process dictionary
        mock_json.loads.return_value = MagicMock()
        process_dictionary = {'Parameters': mock_json.loads.return_value}
        # Mocking argparse to return our predefined arguments
        mock_arg_parser.return_value.parse_args.return_value = self.args
        # Mocking TM1Service and its execute method
        mock_tm1_service.return_value = MagicMock()
        mock_tm1_service.processes.execute.return_value = MagicMock()
        mock_tm1_service.processes.execute.return_value.status_code = 200
        mock_tm1_service.return_value.logout.return_value = MagicMock()

        # Act
        main()

        # Assert
        # Checking if TM1Service is called with the expected arguments
        mock_tm1_service.assert_called_with(address=self.args.server, port=self.args.port, user=self.args.user,
                                            password=self.args.password, namespace=self.args.namespace, ssl=self.args.ssl)
        # Checking if json.loads is called with the expected argument
        mock_json.loads.assert_called_with(self.args.parameter_dict)
        # Checking if TM1Service's execute method is called with the expected arguments
        mock_tm1_service.return_value.processes.execute.assert_called_with(
            self.args.process, parameters=process_dictionary)
        # Checking if TM1Service's logout method is called
        mock_tm1_service.return_value.logout.assert_called_with()

    @patch('scripts.local.generic_process_call.send_alert')
    @patch('scripts.local.generic_process_call.logging.exception')
    @patch('scripts.local.generic_process_call.json')
    @patch('argparse.ArgumentParser')
    @patch('scripts.local.generic_process_call.TM1Service')
    def test_generic_process_call_failure(self, mock_tm1_service, mock_arg_parser, mock_json, mock_logging_exception, mock_send_alert):
        # Arrange
        # Setting up an exception scenario
        message = 'An exception has occurred while calling process : process'
        mock_json.loads.return_value = MagicMock()
        process_dictionary = {'Parameters': mock_json.loads.return_value}
        mock_arg_parser.return_value.parse_args.return_value = self.args
        mock_tm1_service.return_value = MagicMock()
        mock_tm1_service.return_value.processes.execute.side_effect = Exception(
            'Test Exception')
        mock_logging_exception.return_value = MagicMock()
        mock_send_alert.return_value = MagicMock()

        # Act
        main()

        # Assert
        # Checking if TM1Service is called with the expected arguments
        mock_tm1_service.assert_called_with(address=self.args.server, port=self.args.port, user=self.args.user,
                                            password=self.args.password, namespace=self.args.namespace, ssl=self.args.ssl)
        # Checking if json.loads is called with the expected argument
        mock_json.loads.assert_called_with(self.args.parameter_dict)
        # Checking if TM1Service's execute method is called with the expected arguments
        mock_tm1_service.return_value.processes.execute.assert_called_with(self.args.process, parameters=process_dictionary)
        # Checking if TM1Service's logout method is called
        mock_tm1_service.return_value.logout.assert_called_with()