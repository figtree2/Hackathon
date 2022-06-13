

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
const mongoose = require('mongoose');
const form = require('./form');
var c;
const dir = ["S", "W"]

function CenterMap(long, lat){
  map.getView().setCenter(ol.proj.fromLonLat([long, lat]));
  map.getView().setZoom(4);
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

function address(){
  c = document.getElementsByName("address")[0].value;
  String(c)
  let url = "https://api.myptv.com/geocoding/v1/locations/by-address?street="
  words = c.split(" ")
  url += words.pop(0)
  for(word in words){
    url += "%20" + word
  }
  fetch(url, {
        method: "GET",
        headers: { apiKey: "NjgyOWM2MjA4NGRiNGRhOTgxODQ1NjgxNGVkMGJkMmQ6NmM4ZDY5NjAtYjVmNS00M2VlLWIxZGUtZGYwZGNmNTgyZjk1", "Content-Type": "application/json" },
    })
    .then(response => response.json())
    .then(result => console.log(result));

  // CenterMap(longitude, latitude);
}

function createMarker(long, lat) {

  var marker = new ol.Feature({
    geometry: new ol.geom.Point(
      ol.proj.fromLonLat([long, lat])
    ),
  });
  marker.set('style', createStyle('marker.png', undefined)); //someone upload icon to git
  var vectorSource = new ol.source.Vector({
    features: [marker]
  });
  var markerVectorLayer = new ol.layer.Vector({
    source: vectorSource,
  });
  map.addLayer(markerVectorLayer);
}
async function putMarker(){
  await mongoose.connect('mongodb+srv://timotea:1234@cluster0.qfjdm.mongodb.net/?retryWrites=true&w=majority',{
    keepAlive: true,
  })
  let posts = await form.findMany({}).toArray();
  for(let i = 0; i < posts.length; i ++){
    long = posts[i].longitude
    lat = posts[i].latitude
    createMarker(long, lat);
  }
}