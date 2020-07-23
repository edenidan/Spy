
setInterval(function(){ ping() },1000);

function ping(){

    uid = document.getElementById("useridContainer").value;
    roomid = document.getElementById("roomidContainer").value;
    general = document.getElementById("generalinfoContainer").value;


    let http_request = new XMLHttpRequest();
    http_request.open('POST','/ping', false);
    http_request.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    http_request.send(JSON.stringify({"userid": uid, "roomid":roomid,"general":general}));
            
    handleResponse(http_request.responseText)
}