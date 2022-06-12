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
const dir = ["S", "W"]
function CenterMap(long, lat){
  map.getView().setCenter(ol.proj.fromLonLat([long, lat]));
  map.getView().setZoom(14);
}
function process(){
  c = document.getElementsByName("coordinates")[0].value;
  var cArr = [];
  String(c);
  var count = 0;
  var isValid = /^[0-9,.\s\-]*$/.test(c);
  if(isValid){
    cArr = c.split(',');
  }
  else{
    for (var i=0; i<c.length; i++){
      if(c[i] == "°" && count == 0){
        cArr.push(c.slice(0, i));
        count=i;
      }
      else if(c[i] == "°"){
        cArr.push(c.slice(count+4, i));
      }
      else if(dir.includes(c[i])){
        var neg = "-"
        cArr[cArr.length-1] = neg.concat(cArr[cArr.length-1]);
      }
    }
  }
  //var cArr = c.split(',');
  CenterMap(parseFloat(cArr[1]), parseFloat(cArr[0]));
  return false;
}
