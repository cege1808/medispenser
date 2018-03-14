$(function(){

  $("#drop-btn-cluster").show()
  $("#demo-notification").children().remove()
  $("#reset-btn-cluster").hide()

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
      $("#drop-btn-cluster").hide()
      $("#demo-notification").append($("<p>").text("Waiting..."))
      $("#demo-notification").append($("<div>", {"id": "progress"}))
      $("#progress").append($("<div>", {"id": "bar"}))
      move();
    }

    colour_ws.onmessage = function(message){
      var data = JSON.parse(message.data)["message"]
      console.log(data)
      if(data["success"]){
        console.log("Run Motor successfull")
        $("#bar").width("100%")
        setTimeout(function(){
          $("#demo-notification").append($("<p>").text("Please take your pill"))
          $("#reset-btn-cluster").show()
        }, 800);

      }
    }

    colour_ws.onclose = function(message){
      console.log(message);
    }

    colour_ws.onerror = function(message){
      console.log(message);
    }

  })

  $("#reset-btn-cluster").on('click', function(){
    $("#drop-btn-cluster").show()
    $("#demo-notification").children().remove()
    $("#reset-btn-cluster").hide()
  })

  function create_ws_address(path){
    var ws_scheme = window.location.protocol == 'https:' ? 'wss' : 'ws';
    return  ws_scheme + '://' + window.location.host  + window.location.pathname + path;
  }

  function move() {
      var elem = $("#bar");
      var width = 1;
      var id = setInterval(frame, 70);
      function frame() {
          if (width >= 95) {
              clearInterval(id);
          } else {
              width++;
              elem.width(width + "%");
          }
      }
  }


});


