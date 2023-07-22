// price ranger
function getCommaSeparatedNumber(input) {
    var x = input.value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    return x;
}
  
var minSlider = document.getElementById('min');
var maxSlider = document.getElementById('max');

var outputMin = document.getElementById('min-value');
var outputMax = document.getElementById('max-value');

var min = getCommaSeparatedNumber(minSlider);
var max = getCommaSeparatedNumber(maxSlider);

outputMin.innerHTML = min;
outputMax.innerHTML = max;

minSlider.oninput = function(){
    var mi = getCommaSeparatedNumber(this);
    outputMin.innerHTML=mi;
}

maxSlider.oninput = function(){
    var ma = getCommaSeparatedNumber(this);
    outputMax.innerHTML=ma;    
}