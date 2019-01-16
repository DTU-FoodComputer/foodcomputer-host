$("#button").click(function(event){
    $.get("http://localhost:8080/toggle");
});

function update_liveview(){
    $.get("http://localhost:8080/get_image", function(data){
        $("#liveview img").replaceWith(data);
    });
}

function loop(){
    update_liveview();
    setTimeout(function(){
        loop();
    }, 1000.0/15);
}

loop();