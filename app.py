

from flask import Flask, request
from operator import itemgetter
import json

import utils

app = Flask(__name__)


@app.route("/2")
def index():
    r = ""

    return r


@app.route("/")#map")
def map():

    routes = json.loads(open("routes_json.txt").read())


    r = """
<!DOCTYPE html>
<html>
  <head>
    <meta name="viewport" content="initial-scale=1.0, user-scalable=no">
    <meta charset="utf-8">
    <title>MTA Bus Locations</title>
    <style>
      html, body, #map-canvas {
        height: 100%;
        margin: 0px;
        padding: 0px
      }

body { font-family:Arial,Verdana; }

div.route { 
  border:1px solid black;
  padding:2px;
  padding-left:50px;
}
div.route_active { background:#A9F5A9; border-color:green; }
div.route_inactive { background:#F5A9A9; border-color:red; }
div.route_disabled { background:#A4A4A4; border-color:black; }
    </style>
    <script type="text/javascript" src="static/all_shapes.js"></script>
    <script src="https://maps.googleapis.com/maps/api/js?v=3.exp&sensor=false"></script>
    <script>

bus = {"""

    total_buses = 0
    pins = []
    routes_good = []
    route_count = {}
#    for zz in range(0,10):
#        z = routes[zz]

    roots = {}

    for z in routes:
        a = utils.get_bus_locations(z)

        if a != -1:
            if len(a) > 1:
                ind = a[0]["index"]
                routes_good.append(ind)


                """
                temp = '"%s":['%a[0]["index"]
                temp_ar = []
                for x in a:
                    temp_ar.append(json.dumps(x))
                    total_buses += 1
                temp += ",".join(temp_ar)
                temp += "]"
                pins.append(temp)
                route_count[z] = len(temp_ar)
"""


                if ind not in roots.keys():
                    roots[ind] = []
                
                for x in a:
                    roots[ind].append(json.dumps(x))
                    total_buses += 1
                route_count[ind] = len(roots[ind])

    tmp = []
    for x in roots.keys():
        tmp.append('"%s":[%s]'%(x,",".join(roots[x])))
    r += ",".join(tmp)

#    r += ",".join(pins)

    r += """
}
    </script>
    <script type="text/javascript" src="static/maps.js"></script>
  </head>
  <body>
    <div id="map-canvas" style="margin-left:350px;"></div>
    <div id="left" style="overflow:auto;width:350px;position:fixed;height:100%;border-right:5px solid black;top:0;"><div id="leftBox" style="padding:5px;">

<strong>Current Number of Buses</strong>: """+str(total_buses)+"""
<br /><br />
<div style="font-weight:bold;">Routes: <small><a href="javascript:void(0)" onclick="showAllRoutes()">[Show All Buses]</a></small></div>
"""

    for x in routes_good:
        if route_count[x] == 0:
            cn = "disabled"
        else:
            cn = "active"
        r += '<div id="route_%s" class="route route_%s">%s <em>(%d buses)</em></div>'%(x,cn,x,route_count[x])

    r += """</div>
  </body>
</html>
"""

    return r



@app.route("/route")
def route():
    r = ""


    if "route" in request.args:
        route = request.args.get("route")
    else:
        route = -1

        
    if route != -1:
        a = utils.get_bus_locations("M79")

        r += """
<table>
<tr><th>Bus ID</th><th>Longitude</th><th>Latitude</th></tr>"""
        for x in a:
            r += """
<tr>
<td>%(id)s</td>
<td>%(lng)f</td>
<td>%(lat)f</td>
</tr>"""%(x)

        r += '</table>'

    return r


if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0",port=5000)
