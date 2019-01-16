//描画
function plot() {
    document.getElementById("waittxt").textContent = "描画中...";
    var param = {};
    param["year"] = document.getElementById("year").value;
    param["level"] = document.getElementById("level").value;
    param["area"] = document.getElementById("area").value;
    var query = jQuery.param(param);
    
    $.get("/plot/map" + "?" + query, function(data) {
        document.getElementById("plotimg").src = data;
        document.getElementById("waittxt").textContent = ""; 
    });
};

//挙動設定
document.getElementById("plot").addEventListener("click", function(){
    plot()
}, false);

//初回の描画
plot();