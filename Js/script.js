setInterval(function() {
    getData("lireLuminosite", "valeurLuminosite");
}, 2000);

setInterval(function() {
    getData("lireTemperature", "temperature");
}, 2000);

setInterval(function() {
    getData("lireHumidite", "humidite");
}, 2000);

function sendRequest(url) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);
    xhr.send();
}

document.getElementById('led-on').addEventListener('click', function() {
    sendRequest('/led/on');
});

document.getElementById('led-off').addEventListener('click', function() {
    sendRequest('/led/off');
});
document.getElementById('servo-on').addEventListener('click', function() {
    sendRequest('/servo/on');
});

document.getElementById('servo-off').addEventListener('click', function() {
    sendRequest('/servo/off');
});
