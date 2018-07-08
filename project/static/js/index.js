const BASECOORDS = [-7.2575, 112.7521];
const accessToken = 'pk.eyJ1IjoicmFzeWFkaCIsImEiOiJjampibXNxYXUwaW9uM2txazhkdWpoZGZqIn0.IgA6jETECG2wKFy3O6tW6A';
let mymap = L.map('llmap').setView(BASECOORDS, 12);
let activeLayer = {};

const makeMap = (() => {
    let TILE_URL = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";
    let MB_ATTR = 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors';
    L.tileLayer(TILE_URL, {
        attribution: MB_ATTR,
        accessToken: accessToken
    }).addTo(mymap);
});

const onEachFeature = ((feature, layer) => {
    if (feature.properties && feature.properties.Shape_Area) {
        layer.bindPopup(`${feature.properties.Nama_Kanto}<br>Area: ${feature.properties.Shape_Area}<br>Leng: ${feature.properties.Shape_Leng}`);
    }
    else if (feature.properties && feature.properties.KABKOT && feature.properties.PROVINSI) {
        layer.bindPopup(`${feature.properties.KABKOT}<br>${feature.properties.PROVINSI}`);
    }
    else if (feature.properties && feature.properties.KECAMATAN) {
        layer.bindPopup(`${feature.properties.KECAMATAN}<br>${feature.properties.KABKOT}<br>Area: ${feature.properties.SHAPE_Area}, Leng: ${feature.properties.SHAPE_Leng}`);
    }
    else {
        layer.bindPopup(`${feature.properties.Nama_Kanto}<br>${feature.properties.Alamat}<br>Lat: ${feature.properties.Latitude}, Long: ${feature.properties.Longtitude}`);
    }
});

const renderGeoData = ((geo) => {
    if (activeLayer.hasOwnProperty(geo)) {
        mymap.removeLayer(activeLayer[geo]);
        delete activeLayer[geo];

        document.getElementById(geo).classList.remove("is-info");
        document.getElementById(geo).classList.add("is-light");
    }
    else {
        $.getJSON("/geodata/" + geo, (obj) => {
            let style;

            switch (geo.split(".json")[0]) {
                case "Surabaya":
                    style = { "color": "#58ff2e" };
                    break;
                case "KantorPosBuff":
                    style = { "color": "#ff6868" };
                    break;
                case "KecamatanSurabaya":
                    style = { "color": "#0a8602"};
                    break;
                default:
                    style = {};
                    break;
            }

            let layer = new L.GeoJSON(obj, {
                onEachFeature: onEachFeature,
                style: style
            });

            mymap.addLayer(layer);
            activeLayer[geo] = layer;
        });

        document.getElementById(geo).classList.remove("is-light");
        document.getElementById(geo).classList.add("is-info");
    }
});

$(() => {
    makeMap();
});