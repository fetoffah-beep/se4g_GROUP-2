document.getElementById("univ").onclick = function() {
	location.href = "https://www.polimi.it/";
}
document.getElementById("home").onclick = function() {
	location.href = "homeindex.html";
}
function myfunction(){
	alert("Hello\n\nArli\nPhesto\nFelix\nSahar");
}

// Base Map
var osm = new ol.layer.Tile({
	title: 'Open Streets Map',
	type: 'base',
	visible: true,
	source: new ol.source.OSM()
});

var stamenWatercolor = new ol.layer.Tile({
	title: 'Stamen Watercolor',
	type: 'base',
	visible: false,
	source: new ol.source.Stamen({
		layer: 'watercolor'
	})
});

var stamenToner = new ol.layer.Tile({
	title: 'Stamen Toner',
	type: 'base',
	visible: false,
	source: new ol.source.Stamen({
		layer: 'toner'
	})
});

var bingmap = new ol.layer.Tile({
	title: 'Bing Aerial Map',
	type: 'base',
	visible: false,
	source: new ol.source.BingMaps({
		key:
		'AtSmfEyzNVG77MNm5T7j56TO1K4qRO8BWXeYtfNLZ89HHXWOP0GOIGHYIBwAoIMV',
		imagerySet: 'AerialWithLabels'
	})
});

var bingroads = new ol.layer.Tile({
	title: 'Bing Roads Map',
	type: 'base',
	visible: false,
	source: new ol.source.BingMaps({
		key:
		'AtSmfEyzNVG77MNm5T7j56TO1K4qRO8BWXeYtfNLZ89HHXWOP0GOIGHYIBwAoIMV',
		imagerySet: 'Road'
	})
});

// Overlay Map
var road_block = new ol.layer.Image({
	title: 'Road Block',
	source: new ol.source.ImageWMS({
		url: 'http://localhost:8082/geoserver/wms',
		params: {'LAYERS': 'GIS_LabProject_2019:road_block'}
	})
});

var road_segments = new ol.layer.Image({
	title: 'Road Segments',
	source: new ol.source.ImageWMS({
		url: 'http://localhost:8082/geoserver/wms',
		params: {'LAYERS': 'GIS_LabProject_2019:road_segments'}
	})
});

var road_plos = new ol.layer.Image({
	title: 'Road Plos',
	source: new ol.source.ImageWMS({
		url: 'http://localhost:8082/geoserver/wms',
		params: {'LAYERS': 'GIS_LabProject_2019:road_plos'}
	})
});

var road_enplos = new ol.layer.Image({
	title: 'Enhanced Plos',
	source: new ol.source.ImageWMS({
		url: 'http://localhost:8082/geoserver/wms',
		params: {'LAYERS': 'GIS_LabProject_2019:Enhanced_PLOS'}
	})
});

var road_points = new ol.layer.Image({
	title: 'Road Points',
	source: new ol.source.ImageWMS({
		url: 'http://localhost:8082/geoserver/wms',
		params: {'LAYERS': 'GIS_LabProject_2019:road_points'}
	})
});

// Adding wfs layer
var vectorSource = new ol.source.Vector({
	loader: function(extent, resolution, projection) {
		var url = 'http://localhost:8082/geoserver/GIS_LabProject_2019/ows?service=WFS&' +
		'version=1.1.0&request=GetFeature&typeName=GIS_LabProject_2019:Enhanced_PLOS_wfs&' +
		'outputFormat=text/javascript&srsname=EPSG:3857&' +
		'format_options=callback:loadFeatures';
		$.ajax({url: url, dataType: 'jsonp'});
	}
});

var geojsonFormat = new ol.format.GeoJSON();
function loadFeatures(response) {
	vectorSource.addFeatures(geojsonFormat.readFeatures(response))
};

var road_plos_wfs = new ol.layer.Vector({
	title: 'Road Plos WFS',
	source: vectorSource
/*	style: new ol.style.Style({
		stroke: new ol.style.Stroke({
			color: 'rgb(58, 255, 81)',
			width: 4
		})
});*/
});


// Showing Map on Web

var map = new ol.Map({
	target: document.getElementById('map'),
	layers: [

	new ol.layer.Group({
		title: 'Base Map',
		layers: [osm, stamenToner, stamenWatercolor, bingmap, bingroads]
	}),

	new ol.layer.Group({
		title: 'Overlay Map',
		layers: [road_plos_wfs, road_enplos, road_plos, road_segments, road_points]
	})
	],

	view: new ol.View({
		center: ol.proj.fromLonLat([9.1760, 45.4995]),
		zoom: 16
	}),
	controls: ol.control.defaults().extend([
		new ol.control.ScaleLine(),
		new ol.control.FullScreen(),
		new ol.control.OverviewMap(),
		new ol.control.MousePosition({
			coordinateFormat: ol.coordinate.createStringXY(4),
			projection: 'EPSG:4326'
		})
		])
});

// Add Layer Switcher 
var layerSwitcher = new ol.control.LayerSwitcher({});
map.addControl(layerSwitcher);

// Adding Pop-up to Map

var elementPopup = document.getElementById('popup');

var popup = new ol.Overlay({
	element: elementPopup
});

map.addOverlay(popup);

//document.getElementById("map").addEventListener("mouseover", myFunction);
map.on('click', function(event) {
	var feature = map.forEachFeatureAtPixel(event.pixel, function(feature, layer) {
		return feature;
	});
	if (feature != null) {
		var pixel = event.pixel;
		var coord = map.getCoordinateFromPixel(pixel);
		popup.setPosition(coord);
		$(elementPopup).attr('title', '<b>Road Name : </b>' + feature.get('roadname'));
		$(elementPopup).attr('data-content', '<b>PLOS: </b>' + feature.get('PLOS') +
			'</br><b>Enhanced PLOS: </b>' + feature.get('Enhanced32'));
		$(elementPopup).popover({'placement': 'top', 'html': true});
		$(elementPopup).popover('show');
	}	
});

map.on('pointermove', function(event) {
	if (event.dragging) {
		$(elementPopup).popover('destroy');
		return;
	}
	var pixel = map.getEventPixel(event.originalEvent);
	var hit = map.hasFeatureAtPixel(pixel);
	map.getTarget().style.cursor = hit ? 'pointer' : '';
});


// Add Feature info option

map.on('click', function(event) {
	document.getElementById('get-feature-info').innerHTML = '';
	var viewResolution = (map.getView().getResolution());
	var url = road_points.getSource().getFeatureInfoUrl(event.coordinate,
		viewResolution, 'EPSG:3857', {'INFO_FORMAT': 'text/html'});
	if (url)
		document.getElementById('get-feature-info').innerHTML = '<iframe seamless src="' + url + '"></iframe>';
});


map.on('click', function(event) {
	document.getElementById('nodelist').innerHTML = '';
	var view = map.getView();
	var viewResolution = view.getResolution();
	var source = untiled.get('visible') ? untiled.getSource() : tiled.getSource();
	var url = source.getGetFeatureInfoUrl(
		evt.coordinate, viewResolution, view.getProjection(),
		{'INFO_FORMAT': 'text/html', 'FEATURE_COUNT': 50});
	if (url) {
		document.getElementById('nodelist').innerHTML = '<iframe seamless src="' + url + '"></iframe>';
	}
});







