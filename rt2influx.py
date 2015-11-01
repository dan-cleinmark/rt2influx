#!/usr/bin/env python

import numbers
import radiotherm
from influxdb import InfluxDBClient

INFLUX_HOST = '192.168.0.105'
INFLUX_PORT = 8086
INFLUX_USER = 'root'
INFLUX_PASS = 'root'
INFLUX_DB = 'thermostat_history'


def main():
    influx = InfluxDBClient(INFLUX_HOST, INFLUX_PORT,
                            INFLUX_USER, INFLUX_PASS,
                            INFLUX_DB)
    #influx.create_database(INFLUX_DB)
    tstats = list(get_thermostats())
    write_influx(influx, tstats)


def get_thermostats():
    return radiotherm.get_thermostats()


def tstat_point(tstat):
    body = []
    print tstat.tstat['raw']
    for k, v in tstat.tstat['raw'].iteritems():
        if isinstance(v, numbers.Number):
            body.append({
                "measurement": k,
                "tags": {
                  "name": tstat.name['raw']},
                "fields": {
                  "value": v}})
    print body
    return body


def dump_temps(tstats):
    for t in tstats:
        print "%s - %s" % (t.name['raw'], t.temp['raw'])
       

def write_influx(influx, tstats):
    for t in tstats:
        print influx.write_points(tstat_point(t))    


if __name__ == "__main__":
    main()
