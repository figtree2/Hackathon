var map = new ol.Map({
  target: 'map',
  layers: [
    new ol.layer.Tile({
      source: new ol.source.OSM()
    })
  ],
  view: new ol.View({
    //LONGITUDE FIRST IDK WHY IT DOES THAT (39.82, -98.57)
    center: ol.proj.fromLonLat([-98.57, 39.82]),
    zoom: 4
  })
});
var c;
function CenterMap(long, lat){
  map.getView().setCenter(ol.proj.fromLonLat([long, lat]));
  map.getView().setZoom(4);
}
function process(){
  c = document.getElementsByName("coordinates")[0].value;
  String(c);
  var cArr = c.split(',');
  CenterMap(parseInt(cArr[1]), parseInt(cArr[0]));
  return false;
}
