import unittest
from unittest.mock import patch, Mock
import importlib

# Dynamic import of the main function from the module
module_name = 'data-move'  
main_function = importlib.import_module(f'scripts.local.{module_name}').main

class TestMainFunction(unittest.TestCase):

    @patch(f'scripts.local.{module_name}.TM1Service', autospec=True)
    @patch(f'scripts.local.{module_name}.send_alert', autospec=True)
    @patch(f'scripts.local.{module_name}.configure_logging', autospec=True)
    @patch(f'scripts.local.{module_name}.logging', autospec=True)
    def test_main_success(self, mock_logging, mock_configure_logging, mock_send_alert, mock_TM1Service):
        args = Mock(
            server='test_server',
            port='test_port',
            user='test_user',
            ssl=True,
            password='test_password',
            namespace='test_namespace',
            pCube='test_pCube',
            pView='test_pView',
            pFilter='test_pFilter',
            pDimensionDelim='test_pDimensionDelim',
            pElementStartDelim='test_pElementStartDelim',
            pElementDelim='test_pElementDelim',
            pSkipRules=1,
            pSkipCons=1,
            pZeroSource=0,
            pFilePath='test_pFilePath',
            pFileName='test_pFileName',
            pDebug=0
        )

        with patch(f'scripts.local.{module_name}.argparse.ArgumentParser.parse_args', return_value=args):
            main_function()

    @patch(f'scripts.local.{module_name}.TM1Service', side_effect=Exception('Test exception'), autospec=True)
    @patch(f'scripts.local.{module_name}.send_alert', autospec=True)
    @patch(f'scripts.local.{module_name}.configure_logging', autospec=True)
    @patch(f'scripts.local.{module_name}.logging', autospec=True)
    def test_main_exception(self, mock_logging, mock_configure_logging, mock_send_alert, mock_TM1Service):
        args = Mock(
            server='test_server',
            port='test_port',
            user='test_user',
            ssl=True,
            password='test_password',
            namespace='test_namespace',
            pCube='test_pCube',
            pView='test_pView',
            pFilter='test_pFilter',
            pDimensionDelim='test_pDimensionDelim',
            pElementStartDelim='test_pElementStartDelim',
            pElementDelim='test_pElementDelim',
            pSkipRules=1,
            pSkipCons=1,
            pZeroSource=0,
            pFilePath='test_pFilePath',
            pFileName='test_pFileName',
            pDebug=0
        )

        with patch(f'scripts.local.{module_name}.argparse.ArgumentParser.parse_args', return_value=args):
            with self.assertRaises(Exception):
                main_function()

if __name__ == '__main__':
    unittest.main()
