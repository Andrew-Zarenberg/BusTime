

import urllib2
import json
from operator import itemgetter

def get_bus_locations(n):
    if "+" in n:
        n = n.replace("+","%2B")
    url = "http://bustime.mta.info/api/siri/vehicle-monitoring.json?key=OBANYC&LineRef=%s"%n

    result = json.loads(urllib2.urlopen(url).read())

    bus = []

    if "ErrorCondition" in result["Siri"]["ServiceDelivery"]["VehicleMonitoringDelivery"][0].keys():
        return -1

    for x in result["Siri"]["ServiceDelivery"]["VehicleMonitoringDelivery"][0]["VehicleActivity"]:
        x = x["MonitoredVehicleJourney"]
        temp = {
            "id":int("".join(c for c in x["VehicleRef"] if c.isdigit())),
            "route":x["PublishedLineName"],
            "route_num":int("".join(c for c in x["PublishedLineName"] if c.isdigit())),
            "route_prefix":"".join(c for c in x["PublishedLineName"] if not c.isdigit()),
            "lat":x["VehicleLocation"]["Latitude"],
            "lng":x["VehicleLocation"]["Longitude"],
            "destination":x["DestinationName"],
            "index":x["PublishedLineName"].split("-")[0].upper()
            }


        
        bus.append(temp)

    return bus


def bus_routes():
    a = open("routes.txt").read().split("\n")

    r = []

    for x in range(1,len(a)-1):
        k = a[x].split(",")[0]
        if len(k) <= 5:
            r.append([k,int("".join(c for c in k if c.isdigit())),"".join(c for c in k if not c.isdigit())])
        
    r = sorted(r,key=itemgetter(2,1))

    ret = []
    for x in range(0,len(r)):
        ret.append(r[x][0])
    return ret


def test_routes():
    good = []

    k = open("routes_json.txt",'r').read()

    for x in json.loads(k):
        if get_bus_locations(x) != -1:
            good.append(x)

    return good




if __name__ == "__main__":
#    print(str(get_bus_locations("M31")))
#    print(json.dumps(bus_routes()))
    print(json.dumps(test_routes()))
