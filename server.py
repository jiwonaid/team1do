property AppEUI 0240771000000194
property LTID 00000194d02544fffef0149a
property X-M2M-NM test_sub
property X-M2M-Origin 00000194d02544fffef0149a
property X-M2M-RI 00000194d02544fffef0149A_00012
property abc (xml.xpath $system.xml_data */headerCd)
property accept application/xml
property connect_body "<?xml version=\"1.0\" encoding=\"UTF-8\"?><m2m:sub xmlns:m2m=\"http://www.onem2m.org/xml/protocols\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"><enc><rss>1</rss></enc><nu>HTTP|http://211.253.9.191:80</nu><nct>2</nct></m2m:sub>"
property content_type_connect application/vnd.onem2m-res+xml;ty=23
property content_type_send application/xml
property send_body "<?xml version=\"1.0\" encoding=\"UTF-8\"?><m2m:mgc xmlns:m2m=\"http://www.onem2m.org/xml/protocols\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"><exe>true</exe><exra>280101</exra></m2m:mgc>"
property send_body_off "<?xml version=\"1.0\" encoding=\"UTF-8\"?><m2m:mgc xmlns:m2m=\"http://www.onem2m.org/xml/protocols\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"><exe>true</exe><exra>280100</exra></m2m:mgc>"
property uKey VS9zQkEyK3FVWlpwcHNYNXp4V2xYREVXbUdwY3dnQnhNL1dGV2FnT01scElReldhejJNRzJJclFSZ3I1bjN5UA==
property dir /root/Desktop/team1do/website

service id connect
  on start https.send thingplugpf.sktiot.com 9443 /$system.AppEUI$/v1_0/remoteCSE-$system.LTID$/container-LoRa POST $system.connect_body$ {"X-M2M-RI":"$system.X-M2M-RI$","X-M2M-Origin":"$system.X-M2M-Origin$","X-M2M-NM":"$system.X-M2M-NM$","uKey":"$system.uKey$","Content-Type":"$system.content_type_connect$"}
exit
service id get_bus_data
  on start
    http.send ws.bus.go.kr 80 /api/rest/buspos/getBusPosByRtid GET "" {} {"serviceKey":"/lGKaos/Ylfttaf7fO9+7SwZ9UjlA8x0FUyXfnTut8I2T8pP6g/xNbcUuU591ilyIPa851EvrPZ8kQ9PvecrXQ==","busRouteId":"110900008"}
    system.property.write xml_data $last.body
  exit
exit
service id get_bus_info
  on start
    http.send ws.bus.go.kr 80 /api/rest/arrive/getLowArrInfoByRoute GET "" {} {"serviceKey":"/lGKaos/Ylfttaf7fO9+7SwZ9UjlA8x0FUyXfnTut8I2T8pP6g/xNbcUuU591ilyIPa851EvrPZ8kQ9PvecrXQ==","stId":"113000202","busRouteId":"100100332","ord":"36"}
    system.property.write station_data $last.body
  exit
exit
service id send_data
  on start https.send thingplugpf.sktiot.com 9443 /$system.AppEUI$/v1_0/mgmtCmd-$system.LTID$_extDevMgmt PUT $system.send_body$ {"Accpet":"$system.accept$","X-M2M-RI":"$system.X-M2M-RI$","X-M2M-Origin":"$system.X-M2M-Origin$","uKey":"$system.uKey$","Content-Type":"$system.content_type_send$"}
exit
service id send_data_off
  on start https.send thingplugpf.sktiot.com 9443 /$system.AppEUI$/v1_0/mgmtCmd-$system.LTID$_extDevMgmt PUT $system.send_body_off$ {"Accpet":"$system.accept$","X-M2M-RI":"$system.X-M2M-RI$","X-M2M-Origin":"$system.X-M2M-Origin$","uKey":"$system.uKey$","Content-Type":"$system.content_type_send$"}
exit
service id test
  on start
    map.new
    map.put $last X-M2M-RI 00000194d02544fffef0149A_00012
    map.put $last X-M2M-Origin 00000194d02544fffef0149a
    map.put $last uKey VS9zQkEyK3FVWlpwcHNYNXp4V2xYREVXbUdwY3dnQnhNL1dGV2FnT01scElReldhejJNRzJJclFSZ3I1bjN5UA==
    map.put $last X-M2M-NM test_sub
    map.put $last content-type application/vnd.onem2m-res+xml;ty=23
    https.send thingplugpf.sktiot.com 9443 /$system.AppEUI$/v1_0/remoteCSE-$system.LTID$/container-LoRa POST $system.connect_body$ $last
  exit
exit
service id init
  on start
    # service connection_device $system.device3_mac$ $system.POST$ $system.cassia_mac$
    # service configure_device $system.device3_mac$ $system.en_sensor$ $system.cassia_mac$
  exit
exit
service id send_data_to_ws
  on start
    system.property.write station_data (text.replace $system.station_data$ "version=\"1.0\""  "version=\\"1.0\\"")
    system.property.write station_data (text.replace $system.station_data$ "encoding=\"UTF-8\"" "encoding=\\"UTF-8\\"")
    system.property.write station_data (text.replace $system.station_data$ "standalone=\"yes\"" "standalone=\\"yes\\"")
    # content = "{\"xml_data\":\"$system.station_data$\"}"
    content = $system.station_data
    interface.send websocket_server "$content$"
    debug content $content
  exit
exit

interface id webserver
  on #
    if (text.starts_with $data.path /api) (return (event $data.path))
    if (text.equals $data.path /) (return (file.read "$system.dir$/index.html"))
    file.read (text.join $system.dir $data.path)
  exit
  on /api/send_data
    service send_data
  exit
  on /api/send_data_off
    service send_data_off
  exit
  on /api/get_xml_data
    return $system.station_data
  exit
  type http server
  port 80
exit

interface id websocket_server
  port 8081
  type ws server
  on connect respond (service init)
exit

timer id update_10sec
  interval 10000
  on start
    service send_data_to_ws
  exit
  active
exit
