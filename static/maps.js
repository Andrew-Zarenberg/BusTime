markers = {}
polylines = []
selectedRoute = false;

var map;

var EXPRESS = ["X","BxM"]//,"QM","BM"]



function initialize() {
    var myLatlng = new google.maps.LatLng(40.761951,-73.979214);
    var mapOptions = {
	zoom: 14,
	center: myLatlng
    }
    map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);

    for(x in bus){
	temp = [];
	for(y=0;y<bus[x].length;y++){
	    col = "00FF00"   
	    if(bus[x][y]["route_prefix"].match("SBS")) col = "1969bc"
	    else if(bus[x][y]["destination"].match(/^LTD/i)) col = "97168f"
	    else col = "ed1c24"
	    for(z=0;z<EXPRESS.length;z++){
		if(bus[x][y]["route_prefix"] == EXPRESS[z]) col = "008837";
	    }
	    
	    marker = new google.maps.Marker({
		busStuff:bus[x][y],
		position: new google.maps.LatLng(bus[x][y]["lat"],bus[x][y]["lng"]),
		map: map,
		icon:"http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld="+bus[x][y]["route_num"]+"|"+col+"|FFFFFF",
		title: bus[x][y]["route"]+" to "+bus[x][y]["destination"]+" ("+bus[x][y]["id"]+")"
	    });
	    google.maps.event.addListener(marker,"click",function(){
		showOneRoute(this.busStuff);//.index)
	    });
	    google.maps.event.addListener(marker,"mouseover",function(){
		drawRoute(this.busStuff.index,true)
	    });
	    google.maps.event.addListener(marker,"mouseout",function(){
		if(!selectedRoute) clearPolylines();
	    });

	    temp.push(marker);
	}
	markers[x] = temp;
    }
}


function displayMarkers(n,t){
    for(x=0;x<markers[n].length;x++){
	markers[n][x].setVisible(t);
    }
}

function showOneRoute(b){

    console.log(b);
    showInfo(b);

    n = b.index;
    selectedRoute = true;
    clearPolylines();
    for(x in markers){
	if(x != n) displayMarkers(x,false);
    }
    drawRoute(n);
}

function showAllRoutes(){
    selectedRoute = false;
    clearPolylines();
    for(x in markers){
	displayMarkers(x,true);
    }
}

function clearPolylines(){
    for(x=0;x<polylines.length;x++){
	polylines[x].setMap(null);
    }
}







/*
 * DRAW BUS ROUTE
 */
function drawRoute(n){

    var poly = polyRoute[n];//.points;
    var polyPoints = []
    for(var x=0;x<poly.length;x++){
	var temp = []
	for(var y=0;y<poly[x].length;y++){
	    temp.push(new google.maps.LatLng(poly[x][y][0],poly[x][y][1]))
	}
	polyPoints.push(temp)
    }

    for(var x=0;x<polyPoints.length;x++){

	col = "#ff0000";
	for(var y=0;y<EXPRESS.length;y++){
	    if(n.substring(0,EXPRESS[y].length).toUpperCase() == EXPRESS[y].toUpperCase()) col = "#00dd00";
	}

	p = new google.maps.Polyline({
            path: polyPoints[x],
            geodesic: true,
            strokeColor: col,//polyRoute[n].color,
            strokeOpacity: 1.0,
            strokeWeight: 3
	});
	p.setMap(map);
	polylines.push(p);
    }
}



function showInfo(b){
    
    html = "<div style='font-size:25px;'>"+b.route+" ("+b.id+")</div><em>"+b.destination+"</em><br /><strong>Total "+b.route+" buses</strong>: "+bus[b.index].length+"</div>"
    document.getElementById("curRouteInfo").innerHTML = html;
}




google.maps.event.addDomListener(window, 'load', initialize);







