import time
from prometheus_client.core import GaugeMetricFamily, REGISTRY, CounterMetricFamily
from prometheus_client import start_http_server
import rivian_api as rivian
import os
import json
import random

class RivianExporter(object):
    def __init__(self):
        self.rivian = rivian.Rivian()
        response = self.rivian.login(
            os.environ['RIVIAN_USERNAME'],
            os.environ['RIVIAN_PASSWORD']
        )
        # owner info, grab rivian vehicleid
        owner = self.rivian.get_user_information()
        self.rivianid = owner['data']['currentUser']['vehicles'][0]['id']
        print(f'Rivian: {self.rivianid}')

    def collect(self):
        
        # status info
        whipstatus = self.rivian.get_vehicle_state(self.rivianid)

        # battery level - batteryLevel
        # distance to empty - distanceToEmpty
        # gear status - gearStatus

        batterylevel = whipstatus['data']['vehicleState']['batteryLevel']['value']
        distancetoempty = whipstatus['data']['vehicleState']['distanceToEmpty']['value']
        gearstatus = whipstatus['data']['vehicleState']['gearStatus']['value']
        
        # Metric Translations
        if gearstatus == 'park':
            gearstatus = 0
        else:
            gearstatus = 1


        a = GaugeMetricFamily("rivian_battery_level", "% of Battery left", labels=['whip'])
        a.add_metric([self.rivianid], batterylevel)
        yield a

        b = CounterMetricFamily("rivian_battery_distance_empty", 'Miles Left', labels=['whip'])
        b.add_metric([self.rivianid], distancetoempty)
        yield b

        c = CounterMetricFamily("rivian_gear_status", '0=park, otherwise rolling...', labels=['whip'])
        c.add_metric([self.rivianid], gearstatus)
        yield c


if __name__ == '__main__':
    start_http_server(8000)
    REGISTRY.register(RivianExporter())
    while True:
        REGISTRY.collect()
        # lets not piss off the Site Reliability Teams at Rivian
        time.sleep(90)