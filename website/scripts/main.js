var xmlParser = new DOMParser();
var xml_data = "";
var xml_data_websocket = "";
var xmlDoc="";
var xmlDoc_websocket="";
var arrmsg1 ="";
var arrmsg2 ="";
var plainNo1 = "";
var plainNo2 = "";
var ws = new WebSocket("ws://211.253.9.191:8081");
ws.onmessage = function(message) {
  // data = JSON.parse(message.data);
  console.log(message);
  xml_data = message.data;
  xmlDoc = xmlParser.parseFromString(xml_data, "text/xml");

         // Expected arriving time 1
         arrmsg1 = xmlDoc.getElementsByTagName("arrmsg1")[0].innerHTML;
         // Expected arriving time 2
         arrmsg2 = xmlDoc.getElementsByTagName("arrmsg2")[0].innerHTML;
         // vehicle No which is planned to arrive first
         plainNo1 = xmlDoc.getElementsByTagName("plainNo1")[0].innerHTML;
         // vehicle No which is planned to arrive first
         plainNo2 = xmlDoc.getElementsByTagName("plainNo2")[0].innerHTML;
         console.log("Hello World");
  // document.getElementById("bri_data").innerHTML = data.bri_data;
  // document.getElementById("di_data").innerHTML = data.di_data;
  // document.getElementById("Amb_temp_data").innerHTML = calAmb(data.Amb_temp_data);
  // document.getElementById("IR_temp_data").innerHTML = data.IR_temp_data;
  // document.getElementById("baro_data").innerHTML = calBaro(data.baro_data);
  // document.getElementById("humi_data").innerHTML = calHumi(data.humi_data);
  // document.getElementById("earth_data").innerHTML = data.earth_data;
  // document.getElementById("li1_status").innerHTML = data.li1_status;
  // document.getElementById("li2_status").innerHTML = data.li2_status;
  // document.getElementById("li3_status").innerHTML = data.li3_status;
  // document.getElementById("li4_status").innerHTML = data.li4_status;
  // document.getElementById("li5_status").innerHTML = data.li5_status;
  // document.getElementById("li6_status").innerHTML = data.li6_status;
};
$(document).ready(function(){
xmlParser = new DOMParser();


    $(".button_send_data").click(function(){
      console.log("success to send data:before");
        $.get("/api/send_data",function(data,status){
          alert("Data: " + data + "\nStatus: " + status);
        });
        console.log("success to send data");
    });
    $(".button_send_data_off").click(function(){
      console.log("success to send data to off:before");
        $.get("/api/send_data_off");
        console.log("success to send data to off");
    });
    $(".button_test").click(function(){
      console.log("success to send data:before");
        $.get("/api/get_xml_data",function(data,status){
          // alert("Data: " + data + "\nStatus: " + status);
          if(status!="success"){
            alert("error!");
          }else{
            xml_data = data;
            xmlDoc = xmlParser.parseFromString(xml_data, "text/xml");

            // Expected arriving time 1
            arrmsg1 = xmlDoc.getElementsByTagName("arrmsg1")[0].innerHTML;
            // Expected arriving time 2
            arrmsg2 = xmlDoc.getElementsByTagName("arrmsg2")[0].innerHTML;
            // vehicle No which is planned to arrive first
            plainNo1 = xmlDoc.getElementsByTagName("plainNo1")[0].innerHTML;
            // vehicle No which is planned to arrive first
            plainNo2 = xmlDoc.getElementsByTagName("plainNo2")[0].innerHTML;
            console.log("Hello World");
            alert("Expected time to arrive Bus1: " + arrmsg1
            + "   Bus1 Number: " + plainNo1
            + "\nExpected time to arrive Bus2: " + arrmsg2
            + "   Bus2 Number: " + plainNo2);
          }
        });
        console.log("success to send data");
    });

});
