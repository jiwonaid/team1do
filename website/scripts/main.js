//
// var xhr = new XMLHttpRequest();
//
// function send_data(){
// xhr.open('GET', "http://211.253.9.191:80/api/send_data", true);
// xhr.send(null);
// console.log("success to send data ");
// }


$(document).ready(function(){
    $(".button_send_data").click(function(){
      console.log("success to send data:before");
        $.get("/api/send_data");
        console.log("success to send data");
    });
    $(".button_send_data_off").click(function(){
      console.log("success to send data to off:before");
        $.get("/api/send_data_off");
        console.log("success to send data to off");
    });

});
