import argparse
import os
import tempfile
import logging
import json
import logging

from TM1py.Services import TM1Service
from base64 import urlsafe_b64decode, urlsafe_b64encode
from taptools import configure_logging
from taptools import send_alert
from taptools import getsecret
import sys

app = sys.argv[0].split('/')[3]
CONFIG_PATH = f'/var/tm1/{app}/config/deploy/node.json'
ENVIRONMENT_CONFIG = '/opt/uber/environment.json'

def get_environment():
    with open(ENVIRONMENT_CONFIG, 'r') as f:
        return json.load(f)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--server', help='Server Name', required=False, default='localhost')
    parser.add_argument('--port', help='Server Port', required=False, default='20000')
    parser.add_argument('--ssl', help='SSL', required=False, default=True, type=bool)
    parser.add_argument('--namespace', help='CAMNamespace', required=True)
    parser.add_argument('--process', help='Process', required=True)
    parser.add_argument('--pLogPath', help='', required=True)
    parser.add_argument('--parameter_dict', help='Dictionary', required=True, type=str)
    parser.add_argument('--pDebug', help='', required=False, default=0)
    args = parser.parse_args()

    node = json.load(open(CONFIG_PATH))
    env = get_environment()
    user = node['normal']['tm1']['user']
    password = getsecret.get_password('tm1_password', env)
    #Adding derived arguments from Cellar
    args.user=user
    args.password=password
    configure_logging(app='ops', debug=bool(args.pDebug))

    logging.info('Called with parameters {}'.format(vars(args)))

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
