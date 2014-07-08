#!/usr/bin/python

import multitail2
import hpfeeds

import sys
import datetime
import json
import hpfeeds
import logging

root = logging.getLogger()
root.setLevel(logging.ERROR)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)
logger = logging.getLogger("hpfeeds-collector")

def parse(line):
    # TODO: extend this
    return {}

def hpfeeds_connect(host, port, ident, secret):
    try:
        connection = hpfeeds.new(host, port, ident, secret)
    except hpfeeds.FeedException, e:
        logger.error('feed exception: %s'%e)
        sys.exit(1)
    logger.info('connected to %s (%s:%s)'%(connection.brokername, host, port))
    return connection

def main():
    cfg = {
        'host' : '',
        'port' : 10000,
        'channel' : '',
        'ident ' : '',
        'secret' : '',
        'tail_file' : ''
    }

    if len(sys.argv) > 1:
        logger.info("Parsing config file: %s"%sys.argv[1])
        cfg.update(json.load(file(sys.argv[1])))

        for name,value in cfg.items():
            if isinstance(value, basestring):
                # hpfeeds protocol has trouble with unicode, hence the utf-8 encoding here
                cfg[name] = value.encode("utf-8")
    else:
        logger.warning("Warning: no config found, using default values for hpfeeds server")
    publisher  = hpfeeds_connect(cfg['host'], cfg['port'], cfg['ident'], cfg['secret'])

    tail = multitail2.MultiTail(cfg['tail_file'])
    for filemeta, line in tail:
        logger.debug(filemeta, line)
        record = parse(line)
        if record:
            publisher.publish(cfg['channel'], json.dumps(record))
    publisher.stop()
    return 0

if __name__ == '__main__':
    try: 
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(0)

