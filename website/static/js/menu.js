//console.log("This is the new JS!");
// Setup node menu
var modal = document.getElementById("node_menu")
var node_menu = M.Modal.getInstance(modal)
node_menu.options.dismissible = false;
var rows;
var columns;
var spacing;

function post_data(json_str){

    var http = new XMLHttpRequest();
    var url = 'get_data.php';
    var params = 'orem=ipsum&name=binny';
    http.open('POST', "/generator/", true);
    //console.log(json_str)
    
    http.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    
    http.send("data=" + json_str);
    }

    function export_js_db(){
      str = "{";
      var nodes = document.getElementsByClassName("node");
      for(var i = 0; i < nodes.length; i++){
        if(nodes[i].getAttribute("type") != "undefined"){
          var json_str = get_json_db(nodes[i]);
          ////console.log(i + " " +nodes.length);
          str += json_str + ",";
        }
      }
      str = str.slice(0,-1) + "}";
      ////console.log(str);
      post_data(str)
      return str;
    }
  
  
    function export_json(){
         var str = export_js_gen() + "||" + export_js_db()
         post_data(str)
         ////console.log(str)
        return str
    }
    function get_json_db(node){
      var id = node.id;
      var type = node.getAttribute("type");
      var neighbours = node.getAttribute("neighbours");
    // //console.log(str);
       return "\"" + id + "\" :{" + "\"type\":\"" + type + "\", \"neighbours\" : " + neighbours + "}"
    }

    function export_js_gen(){
      str = "{ \"dimensions\" : " + "[" + rows + "," + columns + "], \"nodes\" : {" ;
      var nodes = document.getElementsByClassName("node");
      for(var i = 0; i < nodes.length; i++){
        if(nodes[i].getAttribute("type") != "undefined"){
          var json_str = get_json_gen(nodes[i]);
     //     //console.log(i + " " +nodes.length);
          str += json_str + ",";
   
        }
      }
      str = str.slice(0,-1) + "}}";
     // //console.log(str);
      return str;
     }
   
     function get_json_gen(node){
      var id = node.id;
      var type = node.getAttribute("type");
      var neighbours = node.getAttribute("neighbours");
      var coords = node.getAttribute("coords");
      return "\"" + id + "\" :{" + "\"type\":\"" + type + "\", \"neighbours\" : " + neighbours + ",\"coords\" : " + coords + "}"
     }

     function create_arrow(direction){
      var div = document.createElement("div");
      div.style.width = "10px";
      div.style.height = "10px";
  
      if(direction == "up"){
          div.style.borderLeft = "5px solid transparent";
          div.style.borderRight = "5px solid transparent";
          div.style.borderBottom = "5px solid black";
      }else if(direction == "down"){
          div.style.borderLeft = "5px solid transparent";
          div.style.borderRight = "5px solid transparent";
          div.style.borderTop = "5px solid black";
      }else if(direction == "left"){
          div.style.borderBottom = "5px solid transparent";
          div.style.borderRight = "5px solid transparent";
          div.style.borderTop = "5px solid black";
      }else if(direction == "right"){
          div.style.borderBottom = "5px solid transparent";
          div.style.borderLeft = "5px solid transparent";
          div.style.borderTop = "5px solid black";
      }
  
      return div;
    }
  
    
    
    function connect_via_x(Node1, Node2, d, boxWidth){ // left to right
      var node1;
      var node2;
      if(Number(get_coords(Node1.getAttribute("coords"))[0]) > Number(get_coords(Node2.getAttribute("coords"))[0])){
        node1 = Node2;
        node2 = Node1;
      }else{
        node1 = Node1;
        node2 = Node2;
      }
      var distance = Math.sqrt((get_coords(node2.getAttribute("coords"))[0] - get_coords(node1.getAttribute("coords"))[0])**2);
      var offset = boxWidth * distance;
      ////console.log(String(distance));
    
      var line = document.createElement("div");
      var dist = document.createElement("div");
      dist.appendChild(document.createTextNode(d));
  
      var start = 10 + Number(node1.style.left.slice(0,-2));
      var end = 6 + Number(node1.style.top.slice(0,-2));
      var mid = start + ((offset) / 2);
  
      // Draw Distance
      dist.className = "dist-label";
      dist.style.left = String(mid)+"px";
      dist.style.top = String(end - 25)+"px";
  //    dist.style.width = offset + "px";
      dist.style.visibility = "visible";
      dist.style.position = "absolute";
  
  
      // Draw Line
      line.className = "line";
  
      line.style.left = String(start)+"px";
      line.style.top = String(end)+"px";
      ////console.log(line.style.top);
      line.style.width = offset + "px";
      line.style.height = "0px";
      line.style.visibility = "visible";
      line.style.position = "absolute";
      //console.log(mid);
      //console.log(dist.style.left);
      hide_Nodes(Node1.id, Node2.id, "Horizontal");
      document.getElementsByClassName("connections")[0].appendChild(line);
      document.getElementsByClassName("connections")[0].appendChild(dist);

    }
    
    function connect_via_y(Node1, Node2, d,boxHeight){ //top to bottom
      var node1;
      var node2;
  
      var mid = end + (offset/2);
  
      if(Number(get_coords(Node1.getAttribute("coords"))[1]) > Number(get_coords(Node2.getAttribute("coords"))[1])){
        node1 = Node2;
        node2 = Node1;
    
      }else{
        node1 = Node1;
        node2 = Node2;

      }
      var distance = Math.sqrt((get_coords(node2.getAttribute("coords"))[1] - get_coords(node1.getAttribute("coords"))[1])**2);
      var offset = boxHeight * distance;
      var start = Number(10 + Number(node1.style.left.slice(0,-2)));
      var end = Number(6 + Number(node1.style.top.slice(0,-2)));
      var line = document.createElement("div");
      var dist = document.createElement("div");
      dist.appendChild(document.createTextNode(d));
      //console.log("Drawing Now!!")
      // Draw Distance
      dist.className = "dist-label";
      dist.style.left = String(start - 20)+"px";
      dist.style.top = String(mid)+"px";
  //    dist.style.width = offset + "px";
      dist.style.visibility = "visible";
      dist.style.position = "absolute";
  
      // line
      line.className = "line";
      line.style.left = String(start)+"px";
      line.style.top = String(end)+"px";
      line.style.width = "0px";
      line.style.height = offset + "px";
      line.style.visibility = "visible";
      line.style.position = "absolute";
  
      // arrow
  
  
      hide_Nodes(Node1.id, Node2.id, "Vertical");
      document.getElementsByClassName("connections")[0].appendChild(line);
      document.getElementsByClassName("connections")[0].appendChild(dist);
  //    document.getElementsByClassName("connections")[0].appendChild(arrow);
  
    }
    
    function add_neighbour(n1, n2, direction_n1_n2, Distance, direction, priority){
      Node1 = n1.getAttribute("id");
      Node2 = n2.getAttribute("id");
      //console.log("Node1 ID: " + Node1);
      //console.log("Node2 ID: " + Node2);
      //console.log(direction_n1_n2)

      directions = ["up", "right", "down", "left"];
      var second = directions.indexOf(direction_n1_n2);
      //console.log("direction "+direction_n1_n2);
      //console.log(second);
      if(second <= 1){
        second = directions[second + 2];
      }else{
        second = directions[second - 2];
      }
      //console.log(second);
  
      var n_dir = "bi";
      if(direction == "to"){
          n_dir = "from";
      }else if(direction == "from"){
          n_dir = "to";
      }


      if(n1.hasAttribute("neighbours")){
        n1.setAttribute("neighbours", n1.getAttribute("neighbours").slice(0, -1) + ",\"" + direction_n1_n2 + "\":[" + Node2 + "," + Distance + ",\"" + direction + "\"," + priority + "]}");
      }else{
        n1.setAttribute("neighbours", "{\"" + direction_n1_n2 + "\":[" + Node2 + "," + Distance + ",\"" + direction +"\"," + priority + "]}");
      }
    
      if(n2.hasAttribute("neighbours")){
        n2.setAttribute("neighbours", n2.getAttribute("neighbours").slice(0, -1) + ",\"" + second + "\":[" + Node1 + "," + Distance + ",\"" + n_dir + "\"," + priority + "]}");
      }else{
        n2.setAttribute("neighbours", "{\"" + second + "\":[" + Node1 + "," + Distance + ",\"" + n_dir + "\"," + priority + "]}");
      }
    
      //console.log(n1.neighbours);
    
    }
    
    function getAttributes() {
      var ret = "";
      var dist = "";
      var w = "";
      var typo = "";
  
      var distance = prompt("Please enter the distance between these two nodes", "");
      if (distance != null) {
        dist = distance;
      }
  
      var weight = prompt("Please Enter The Priority of this lane(0-100)", "");
      if (weight != null) {
        //console.log(weight)
        w = weight;
      }
  
      var tp = prompt("Please Enter The Connection Type(bi, to, from)", "");
      if (tp != null) {
        typo = tp;
      }
  
  
  
      return dist + "," + typo + "," + w + ",";
    }
  
    function get_node_by_coords(x,y){
      nodes = document.getElementsByClassName("node");
      for(var i = 0; i < nodes.length; i++){
          if(nodes[i].getAttribute("coords") == "[" + x + "," + y + "]"){
              //console.log("Found node id! " + nodes[i].getAttribute("id"));
              return nodes[i];
          }
      };
    }
  
    function hide_Nodes(start, end, direction){
      var start = document.getElementsByClassName("node")[start];
      var end = document.getElementsByClassName("node")[end];
  
      if(direction == "Vertical"){
          x = parseInt(start.getAttribute("coords").replace("]","").replace("[","").split(",")[0]);
          start_y = parseInt(start.getAttribute("coords").replace("]","").replace("[","").split(",")[1]);
          end_y = parseInt(end.getAttribute("coords").replace("]","").replace("[","").split(",")[1]);
          difference = start_y - end_y;
          //console.log(start_y - end_y);
          for(var i = 1; i < ((difference)**2)**0.5;i++){
              if(Math.sign(difference) == -1){
                //console.log("hi");
                var node = get_node_by_coords(x, start_y + i);
                node.style.visibility = "hidden";
              }else if(Math.sign(difference) == 1){
                //console.log("hi");
                var node = get_node_by_coords(x, start_y - i);
                node.style.visibility = "hidden";
              }
          }
      }else if(direction == "Horizontal"){
          y = parseInt(start.getAttribute("coords").replace("]","").replace("[","").split(",")[1]);
          start_x = parseInt(start.getAttribute("coords").replace("]","").replace("[","").split(",")[0]);
          end_x = parseInt(end.getAttribute("coords").replace("]","").replace("[","").split(",")[0]);
          difference = start_x - end_x;
          //console.log(start_x - end_x);
          for(var i = 1; i < ((difference)**2)**0.5;i++){
              if(Math.sign(difference) == -1){
                //console.log("hi");
                var node = get_node_by_coords(start_x + i, y);
                node.style.visibility = "hidden";
              }else if(Math.sign(difference) == 1){
                //console.log("hi");
                var node = get_node_by_coords(start_x - i,y);
                node.style.visibility = "hidden";
              }
          }
      }
  
  
    }
  
    function connect(Node1,Node2,attr){
      var n1 = document.getElementById(Node1);
      var n2 = document.getElementById(Node2);
      //console.log(get_coords(n1.getAttribute("coords")), get_coords(n2.getAttribute("coords")));
  
      var attributes = attr.split(",");
      var Distance = attributes[0];
      var connection_direction = attributes[1]; // bi
      var priority = attributes[2];
  
      //console.log(Distance);
      //console.log(connection_direction);
      //console.log(priority);
  
      if(Number(get_coords(n1.getAttribute("coords"))[0]) == Number(get_coords(n2.getAttribute("coords"))[0])){
        connect_via_y(n1, n2, Distance, 50);
        if(Number(get_coords(n1.getAttribute("coords"))[1]) > Number(get_coords(n2.getAttribute("coords"))[1])){
          add_neighbour(n1,n2,"up", Distance, connection_direction, priority);
        }else{
          add_neighbour(n1,n2,"down", Distance, connection_direction, priority);
        }
      }else if(Number(get_coords(n1.getAttribute("coords"))[1]) == Number(get_coords(n2.getAttribute("coords"))[1])){
        connect_via_x(n1, n2, Distance, 50);
        console.log("FOR GOD DANM")
        console.log(get_coords(n1.getAttribute("coords"))[0])
        console.log(get_coords(n2.getAttribute("coords"))[0])
        if(Number(get_coords(n1.getAttribute("coords"))[0]) > Number(get_coords(n2.getAttribute("coords"))[0])){
          console.log("Selecting Left")
          add_neighbour(n1,n2,"left", Distance, connection_direction, priority);
        }else{
          console.log("Selecting Right")
          add_neighbour(n1,n2,"right", Distance, connection_direction, priority);
        }
      }else{
        //console.log("sorry cannot link");
      }
    
    
      //console.log("Connected.");
      connecting = false;
      //console.log("WIPING PAIR");
      pair = [];
      // document.getElementsByClassName("grid")[0].appendChild(div);
    
    }
    
    function toggle_grid(){
      var box = document.getElementsByClassName("box");
      var node = document.getElementsByClassName("node");
    
      for(var i=0; i < box.length; i++){
        if(box[i].style.visibility == "visible"){
          box[i].style.visibility = "hidden";
        }else{
          box[i].style.visibility = "visible";
    
        }
      }
    
      for(var i=0; i < node.length; i++){
        //console.log(node[i].getAttribute("type"));
        if(node[i].getAttribute("type") == "undefined" && node[i].style.visibility == "visible"){
          node[i].style.visibility = "hidden";
        }else if (node[i].getAttribute("type") == "undefined"){
          node[i].style.visibility = "visible";
        }
      }
    }
    
    
    
    function addBox(id, left,top) {
      var div = document.createElement("div");
      div.className = "box";
      // div.id = id;
      div.style.left = String(200 + Number(left))+"px";
      div.style.top = String(150 + Number(top))+"px";
      document.getElementsByClassName("grid")[0].appendChild(div);
    }
    
    
    function copyNodeStyle(sourceNode, targetNode) {
        const computedStyle = window.getComputedStyle(sourceNode);
        Array.from(computedStyle).forEach(key => targetNode.style.setProperty(key, computedStyle.getPropertyValue(key), computedStyle.getPropertyPriority(key)))
      }
  
  
  
    function get_coords(str){
  
      const unbracket = String(str).replace(']','').replace('[','').split(",");
      var x = unbracket[0];
      var y = unbracket[1];
      // //console.log(x,y);
      return unbracket;
  
    }
  
    var connecting = false;
    var pair = [];
    function connect_button(){
      connecting = true;
      //console.log(connecting);
    }
  
      function add_connect_node(id){
        if(pair.length < 2){
        pair.push(id);
        //console.log("I'm here");
      }
  
      if(pair.length >= 2){
          // Wipe the buttons
          document.getElementById("node_buttons").style.display = "none";
          // Show the form
          document.getElementById("lane_info").style.display = "block";
          // Set up submission
          //console.log("Opened connection menu");
          // Setup the submission button
          //console.log(pair);
          const getLaneData = () => {
            // Parse the form data
                const dir = document.querySelector('input[name="direction"]:checked').value;
                const priority = document.getElementById("priority").value;
                const dist = document.getElementById("distance").value;
                var parsedStr = `${dist},${dir},${priority},`;
                //console.log("HERE!!!!!" + parsedStr);
                connect(pair[0],pair[1],parsedStr);
                node_menu.close();
                // Show the buttons
                document.getElementById("node_buttons").style.display = "block";
                // Wipe the form
                document.getElementById("lane_info").style.display = "none";
                document.getElementById("create_lane").removeEventListener("click", getLaneData);
                };
          document.getElementById("create_lane").addEventListener("click", getLaneData);
          node_menu.open();
      }}
  
    
    function node_options(id,menu){
       //console.log("here");
      // var menu = document.getElementsByClassName("item-selector")[0];
      // var selector = document.getElementById("selector");
      // menu.style.visibility = "visible";
      var selector = document.querySelector('input[name="group2"]:checked').value;
      var grid = document.getElementsByClassName("grid")[0];
      // var val = selector.value.valueOf();
  //    document.getElementsByClassName("node")[id].type = selector.value;
    
      if(selector == "connect"){
  //      document.getElementById(id).style.background = "Blue";
          //console.log("Connecting...");
          connecting = true;
          add_connect_node(id);
      }
      if(selector == "delete"){
        document.getElementById(id).style.background = "White";
        document.getElementsByClassName("node")[id].type = "undefined";
      }
  //    if(selector.value == "exit"){
  //      document.getElementById(id).style.background = "Yellow";
  //    }
    
      menu.style.visibility = "hidden";
      menu.remove();
      grid.style.visibility = "visible";
    
    }
  
      function set_type_radio(id){
      // //console.log("here");
      // var menu = document.getElementsByClassName("item-selector")[0];
      // var selector = document.getElementById("selector");
      // menu.style.visibility = "visible";
  //    var selector = menu.childNodes[3];
  //    var selected = document.getElementById("group1").getAttribute("value");
      // var val = selector.value.valueOf();
      var selected = document.getElementById("node_type").value;
      document.getElementsByClassName("node")[id].type = selected;
  
      if(selected == "robot"){
        document.getElementById(id).style.background = "Blue";
      }
      if(selected == "rfid"){
        document.getElementById(id).style.background = "Red";
      }
      if(selected == "shelf"){
        document.getElementById(id).style.background = "Yellow";
      }
      if(selected == "undefined"){
            document.getElementById(id).style.background = "White";
      }
  
      //console.log(String(document.getElementById(id).style.background));
      //console.log(String(selected));
  //    menu.style.visibility = "hidden";
  //    menu.remove();
  //    grid.style.visibility = "visible";
  
    }
    
    function add_node(id, coords, left, top){ // where modifier is last row, last colunm, bottom right or else
      var div = document.createElement("button");
      div.className = "node";
      div.id = id;
      div.type = "undefined";
      div.setAttribute("coords",coords);
    
    // /  // div.style.position = "absolute";
      div.style.left = String(500 + Number(left))+"px";
      // div.style.right = "0px";
      div.style.top = String(200 + Number(top))+"px";
      document.getElementsByClassName("grid")[0].appendChild(div);
      // What happens when you click a node
      document.getElementById(id).onclick = function() {
         //console.log(connecting);
  
        if(div.getAttribute("type") == "undefined" || document.getElementById("node_type").value == "" ){
            //console.log("Indeterminate state");
              set_type_radio(id);
        }else if(connecting == true){
              //console.log("Connecting");
              add_connect_node(div.id);
        }else{
        //console.log(div.getAttribute("type"));
        if(!connecting){
            //console.log("CLICK - not connecting");
            //console.log(pair);
            // Display the menu (modal)
            node_menu.open();
        //   var menu = document.getElementsByClassName("item-selector")[0].cloneNode(true);
        //   menu.id = "temp";
        //   document.getElementsByClassName("temp-select")[0].appendChild(menu);
        //   var grid = document.getElementsByClassName("grid")[0];
        //   menu.style.visibility = "visible";
        //   grid.style.visibility = "hidden";
        //   //console.log(menu.childNodes);
        //   menu.childNodes[5].addEventListener("click", function(){
        //           node_options(id,menu);
        //   });

        var connect_button = document.getElementById("connect");
        var cancel_button = document.getElementById("cancel");
        var delete_button = document.getElementById("delete");

        const connect_action = () => {
            connect_option(id);
            cancel_button.removeEventListener("click",cancel_action);
            connect_button.removeEventListener("click",connect_action);
            delete_button.removeEventListener("click",delete_action);
        };

        const cancel_action = () => {
            cancel_option(id);
            cancel_button.removeEventListener("click",cancel_action);
            connect_button.removeEventListener("click",connect_action);
            delete_button.removeEventListener("click",delete_action);
        };

        const delete_action = () => {
            delete_option(id);
            cancel_button.removeEventListener("click",cancel_action);
            connect_button.removeEventListener("click",connect_action);
            delete_button.removeEventListener("click",delete_action);
        };

        connect_button.addEventListener("click", connect_action);

        cancel_button.addEventListener("click", cancel_action);

        delete_button.addEventListener("click", delete_action);
    
    
        }else{
  
    
        }
    
    }
    };
}

    function connect_option(id){
        //console.log("Connecting...");
        connecting = true;
        add_connect_node(id);
        node_menu.close();
    }

    function delete_option(id){
        document.getElementById(id).style.background = "White";
        document.getElementsByClassName("node")[id].type = "undefined";
        node_menu.close();
    }

    function cancel_option(id){
        //console.log("Cancelling");
        node_menu.close();
        //console.log(pair);
    }

    function createGrid(){
        document.getElementById("dim-form").style.display = "none";
        document.getElementById("grid-builder").style.display = "block";
      // clearDoc();
      // Clear the grid
      document.getElementsByClassName("grid")[0].innerHTML = "";
    
      rows = document.getElementById("length").value;
      columns = document.getElementById("width").value;
      spacing = 50;
    
      var nodes = 0;
    
      for(var i = 0; i < columns; i++){
        for(var x = 0; x < rows; x++){
          var row = String(x + 1);
          var colunm = String(i + 1);
          var id = "[" + row + "," + colunm + "]";
          // var x = row;
          // var y = column;
          var left = 50 * x + spacing;
          var top = 50 * i + spacing;
    //        addBox(id, left, top);
    
    
          if(x == rows || i == columns){
    
            add_node(nodes, id, left + spacing, top);
            nodes += 1;
            add_node(nodes, id, left + spacing, top + spacing);
            nodes += 1;
            add_node(nodes, id, left, top);
            nodes += 1;
            add_node(nodes, id, left, top + spacing);
            nodes += 1;
    
          }else{
            add_node(nodes, id, left, top);
            nodes += 1;
          }
          // var box = document.getElementById(id);
        }
      }
    }