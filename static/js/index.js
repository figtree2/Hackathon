var map = new ol.Map({
  target: 'map',
  layers: [
    new ol.layer.Tile({
      source: new ol.source.OSM()
    })
  ],
  view: new ol.View({
    //LONGITUDE FIRST IDK WHY IT DOES THAT (-98.57, 39.82)
    center: ol.proj.fromLonLat([-98.57, 39.82]),
    zoom: 4
  })
});