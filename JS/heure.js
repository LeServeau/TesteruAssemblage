setInterval(function() {
    var heure = new Date();
    var uminute = heure.getMinutes();
    var useconde = heure.getSeconds();
    var uheure = heure.getHours();
    if (uheure < 10) { uheure = '0' + uheure; }
    if (uminute < 10) { uminute = '0' + uminute; }
    if (useconde < 10) { useconde = '0' + useconde; }
    var time = uheure + ':' + uminute + ':' + useconde
    document.getElementById('heure').innerHTML = time;
}, 1);