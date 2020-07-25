
setInterval(function(){ ping() },1000);

function onResponse(http_request){
    console.log('got response')
    handleResponse(http_request.responseText)
}

function ping(){

    

    uid = document.getElementById("useridContainer").value;
    roomid = document.getElementById("roomidContainer").value;
    general = document.getElementById("generalinfoContainer").value;

    var d = new Date();
    var n = d.getTime();
    console.log('ping ' + n)

    let http_request = new XMLHttpRequest();
    http_request.open('POST','/ping',true);
    http_request.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    http_request.onload= ()=> { onResponse(http_request); }
    http_request.send(JSON.stringify({"userid": uid, "roomid":roomid,"general":general}));
            
}