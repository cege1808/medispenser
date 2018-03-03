$(function(){

  $(".demo-btn").on('click', function(){
    var colour = $(this).data('colour');
    var module = $(this).data('module');
    var address = create_ws_address(colour);
    console.log(address);
    var colour_ws = new WebSocket(address);

    colour_ws.onopen =  function(message){
      console.log(message);
      colour_ws.send(JSON.stringify({
        'path': window.location.pathname,
        'message': 'run module -client-',
        'colour': colour,
        'module': module
      }));
    }

    colour_ws.onmessage = function(message){
      console.log(message);
      console.log(message.data);
    }

    colour_ws.onclose = function(message){
      console.log(message);
    }

    colour_ws.onerror = function(message){
      console.log(message);
    }

  })

});

function create_ws_address(path){
  var ws_scheme = window.location.protocol == 'https:' ? 'wss' : 'ws';
  return  ws_scheme + '://' + window.location.host  + window.location.pathname + path;
}
