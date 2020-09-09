import argparse
import os
import tempfile
import logging
import json

from TM1py.Services import TM1Service
from base64 import urlsafe_b64decode, urlsafe_b64encode
from taptools import configure_logging
from taptools import send_alert

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--server', help='Server Name', required=False, default='localhost')
    parser.add_argument('--port', help='Server Port', required=False, default='20000')
    parser.add_argument('--user', help='Username', required=True)
    parser.add_argument('--ssl', help='SSL', required=False, default=True, type=bool)
    parser.add_argument('--password', help='Password', required=True)
    parser.add_argument('--namespace', help='CAMNamespace', required=True)
    parser.add_argument('--process', help='Process', required=True)
    parser.add_argument('--pLogPath', help='', required=True)
    parser.add_argument('--parameter_dict', help='Dictionary', required=True, type=str)
    args = parser.parse_args()
    try:
        tm1_service = TM1Service(address=args.server, port=args.port, user=args.user, password=args.password, namespace=args.namespace, ssl=args.ssl)
        data=json.loads(args.parameter_dict)
        process_dictionary = {'Parameters': data}
        tm1_service.processes.execute(args.process, parameters=process_dictionary)
    except Exception as err:
        log_name= args.process + '.tap'
        message = "An exception has occured while calling process :" + args.process
        logging.exception(message, app=args.server, file_name=log_name)
        send_alert(message, pd=False, email=True)
    finally:
        tm1_service.logout()
        
if __name__ == '__main__':
    main()
