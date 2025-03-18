
import argparse
import logging
from taptools import configure_logging
from taptools import send_alert
from TM1py.Services import TM1Service
from taptools import getsecret
import sys
import json


app = sys.argv[0].split('/')[3]
CONFIG_PATH = f'/var/tm1/{app}/config/deploy/node.json'
ENVIRONMENT_CONFIG = '/opt/uber/environment.json'

def get_environment():
    with open(ENVIRONMENT_CONFIG, 'r') as f:
        return json.load(f)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--server', help='Server Name', required=False, default='ops.findev.uberinternal.com')
    parser.add_argument('--port', help='Server Port', required=False, default='443')
    parser.add_argument('--ssl', help='SSL', required=False, default=True, type=bool)
    parser.add_argument('--namespace', help='CAMNamespace', required=False, default='uberAD')
    parser.add_argument('--pCube', help='', required=False, default='OPS Monthly')
    parser.add_argument('--pView', help='', required=False, default='')
    parser.add_argument('--pFilter', help='', required=False, default='Version:Actual')
    parser.add_argument('--pDimensionDelim', help='', required=False, default='&')
    parser.add_argument('--pElementStartDelim', help='', required=False, default=':')
    parser.add_argument('--pElementDelim', help='', required=False, default='+')
    parser.add_argument('--pSkipRules', help='', required=False, default=1)
    parser.add_argument('--pSkipCons', help='', required=False, default=1)
    parser.add_argument('--pZeroSource', help='', required=False, default=0)
    parser.add_argument('--pFilePath', help='', required=False, default='var/tm1/ops/files/shared/ops/')
    parser.add_argument('--pFileName', help='', required=False, default='filter.txt')
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

        parameter = {'Parameters': [
            {'Name': 'pCube', 'Value': args.pCube},
            {'Name': 'pView', 'Value': args.pView},
            {'Name': 'pFilter', 'Value': args.pFilter},
            {'Name': 'pDimensionDelim', 'Value': args.pDimensionDelim},
            {'Name': 'pElementStartDelim', 'Value': args.pElementStartDelim},
            {'Name': 'pElementDelim', 'Value': args.pElementDelim},
            {'Name': 'pSkipRules', 'Value': args.pSkipRules},
            {'Name': 'pSkipCons', 'Value': args.pSkipCons},
            {'Name': 'pZeroSource', 'Value': args.pZeroSource},
            {'Name': 'pFilePath', 'Value': args.pFilePath},
            {'Name': 'pFileName', 'Value': args.pFileName},
            {'Name': 'pDebug', 'Value': args.pDebug}
        ]}

        tm1_service.processes.execute('tap.cube.export data to file', parameters=parameter)
    except Exception:
        message = 'Exception while calling TI process: tap.cube.export data to file'
        send_alert(message, alert_high=False)
        logging.exception(message)
    finally:
        tm1_service.logout()


if __name__ == "__main__":
    main()