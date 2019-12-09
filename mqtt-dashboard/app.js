var util = require('util');
var net = require('net');
var mqtt = require('mqtt');
var http = require("http"),
    url = require("url"),
    path = require("path"),
    fs = require("fs")
    port = process.argv[2] || 8888;

var io  = require('socket.io').listen(3000);
//var client = mqtt.connect('mqtt://iot.eclipse.org');
var client  = mqtt.connect('mqtt://broker.hivemq.com');

client.on('connect', function () {
    // Solar Panel
    // client.subscribe('anthonyho-solar/veris/#');
    client.subscribe('ioThinx_4510/read/#');
    console.log("\nConnected to broker... \n");
});

io.sockets.on('connection', function (socket) {
  socket.on('subscribe', function (data) {
    console.log('Subscribing to '+data.topic);
    socket.join(data.topic);
    client.subscribe(data.topic);
  });
});

client.on('message', function(topic, message) {
    console.log(topic+' = '+message.toString());
    io.sockets.emit('mqtt', {
        'topic': String(topic), 
        'payload': JSON.parse(message.toString())
    }); 
});

http.createServer(function(request, response) {

  var uri = url.parse(request.url).pathname
    , filename = path.join(process.cwd(), uri);

  fs.exists(filename, function(exists) {
    if(!exists) {
      response.writeHead(404, {"Content-Type": "text/plain"});
      response.write("404 Not Found\n");
      response.end();
      return;
    }

    if (fs.statSync(filename).isDirectory()) filename += '/index.html';

    fs.readFile(filename, "binary", function(err, file) {
      if(err) {
        response.writeHead(500, {"Content-Type": "text/plain"});
        response.write(err + "\n");
        response.end();
        return;
      }
      response.writeHead(200);
      response.write(file, "binary");
      response.end();
    });
  });
}).listen(parseInt(port, 10));

console.log("Dashboard is running at\n  => http://localhost:" + port + "/\nCTRL + C to shutdown");
