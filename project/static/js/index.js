const BASECOORDS = [-7.2575, 112.7521];
const accessToken = 'pk.eyJ1IjoicmFzeWFkaCIsImEiOiJjampibXNxYXUwaW9uM2txazhkdWpoZGZqIn0.IgA6jETECG2wKFy3O6tW6A';
let mymap = L.map('llmap').setView(BASECOORDS, 12);
let defaultActiveLayer = {};

const makeMap = (() => {
    let TILE_URL = "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png";
    let MB_ATTR = 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors';
    L.tileLayer(TILE_URL, {
        attribution: MB_ATTR,
        accessToken: accessToken
    }).addTo(mymap);
});

const onEachFeature = ((feature, layer) => {
    if (feature.properties && feature.properties.KABKOT && feature.properties.PROVINSI) {
        layer.bindPopup(`${feature.properties.KABKOT}<br>${feature.properties.PROVINSI}`);
    }
    else if (feature.properties && feature.properties.KECAMATAN) {
        layer.bindPopup(`${feature.properties.KECAMATAN}<br>${feature.properties.KABKOT}<br>Area: ${feature.properties.SHAPE_Area}, Leng: ${feature.properties.SHAPE_Leng}`);
    }
    else {
        layer.bindPopup(`${feature.properties.Nama}<br>Lat: ${feature.properties.Latitude}, Long: ${feature.properties.Longitude}`);
    }
});

const renderGeoData = ((geo) => {
    if (defaultActiveLayer.hasOwnProperty(geo)) {
        mymap.removeLayer(defaultActiveLayer[geo]);
        delete defaultActiveLayer[geo];

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
                case "KecamatanSurabaya":
                    style = { "color": "#ff6868" };
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
            defaultActiveLayer[geo] = layer;
        });

        document.getElementById(geo).classList.remove("is-light");
        document.getElementById(geo).classList.add("is-info");
    }
});

$(() => {
    makeMap();
});