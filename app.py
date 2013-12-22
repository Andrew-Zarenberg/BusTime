

from flask import Flask, request, render_template
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

#    routes = json.loads(open("routes_json.txt").read())

    return render_template("index.html")




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


@app.route("/js")
def js():
    a = int(request.args.get("type"))
    
    # get shape
    if a == 1:
        return utils.get_bus_shape(request.args.get("route"))



if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0",port=5000)
