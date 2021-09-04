#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import yaml
from flask import Flask, Response, request
import netsnmp

app = Flask(__name__)

parser = argparse.ArgumentParser(description='Web server that proxies SNMP extracts for Prometheus')

metric_format = '\n'.join(['# HELP {metric} {metric_help}',
                           '# TYPE {metric} {metric_type}',
                           '{metric} {metric_value}'])

parser.add_argument('--config_file',
                    type=str,
                    required=True,
                    help="config file in yaml format")

parser.add_argument('--port',
                    type=int,
                    help = "listen port for this server",
                    default = '9550')

def start_server(port):
    app.run(host='0.0.0.0', port=port, debug=False)

    
def main():
    args = parser.parse_args()

    config = yaml.load(open(args.config_file))
    
    app.config['targets'] = config['targets']

    print("starting server at port: %d" % args.port)
    start_server(args.port)
        

@app.route("/")
def hello_world():
    return "<p><a href='/metrics'>Prometheus Metrics</a></p>"


def get_snmp(snmp_session, oid):
    walk = snmp_session.walk(netsnmp.VarList(netsnmp.Varbind(oid, '')))
    if len(walk) > 0:
        return walk[0] # only supports single valued fields
    else:
        return None

@app.route("/metrics")
def metrics():

    responses = []
    target_host = request.args.get('target')
    
    for target in app.config['targets']:
        if target['address'] != target_host:
            continue

        session = netsnmp.Session(Version=2, DestHost=target['address'], Community='public')
        for metric in target['metrics']:
            metric_value = get_snmp(session, metric['oid'])
            if metric_value != None:
                responses.append(metric_format.format(metric=metric['label'],
                                                      metric_help=metric['help'],
                                                      metric_type=metric.get('type', 'gauge'),
                                                      metric_value=metric_value.decode('utf-8')))

    return Response('\n'.join(responses), mimetype='text/plain')

if __name__ == '__main__':
    main()
