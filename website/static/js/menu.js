console.log("This is the new JS!");
// Setup node menu
var modal = document.getElementById("node_menu")
var node_menu = M.Modal.getInstance(modal)
node_menu.options.dismissible = false;

function post_data(json_str){

    var http = new XMLHttpRequest();
    var url = 'get_data.php';
    var params = 'orem=ipsum&name=binny';
    http.open('POST', "/generator/", true);
    console.log(json_str)
    
    http.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    
    http.send("data=" + json_str);
    }
  //  //Send the proper header information along with the request
  //  http.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
  //
  //  http.onreadystatechange = function() {//Call a function when the state changes.
  //      if(http.readyState == 4 && http.status == 200) {
  //  //        alert(http.responseText);
  //      }
  //  }
  //  http.send("data=" + json_str);
    
    
    function connect_via_x(Node1, Node2, boxWidth){ // left to right
      // var start =
      var node1;
      var node2;
      if(get_coords(Node1.getAttribute("coords"))[0] > get_coords(Node2.getAttribute("coords"))[0]){
        node1 = Node2;
        node2 = Node1;
    
      }else{
        node1 = Node1;
        node2 = Node2;
      }
      var distance = Math.sqrt((get_coords(node2.getAttribute("coords"))[0] - get_coords(node1.getAttribute("coords"))[0])**2);
      var offset = boxWidth * distance;
      console.log(String(distance));
    
      var div = document.createElement("div");
      div.className = "line";
      div.style.left = String(10 + Number(node1.style.left.slice(0,-2)))+"px";
      div.style.top = String(6 + Number(node1.style.top.slice(0,-2)))+"px";
      console.log(div.style.top);
      div.style.width = offset + "px";
      div.style.height = "0px";
      div.style.visibility = "visible";
      hide_Nodes(Node1.id, Node2.id, "Horizontal");
  
      document.getElementsByClassName("connections")[0].appendChild(div);
    }
    
    function connect_via_y(Node1, Node2, boxHeight){ //top to bottm
      // var start = Node1.top;
      var node1;
      var node2;
      if(get_coords(Node1.getAttribute("coords"))[1] > get_coords(Node2.getAttribute("coords"))[1]){
        node1 = Node2;
        node2 = Node1;
    
      }else{
        node1 = Node1;
        node2 = Node2;
      }
      var distance = Math.sqrt((get_coords(node2.getAttribute("coords"))[1] - get_coords(node1.getAttribute("coords"))[1])**2);
      var offset = boxHeight * distance;
      // console.log(node1_y + "," + node2_y);
    
      var div = document.createElement("div");
      div.className = "line";
      div.style.left = String(10 + Number(node1.style.left.slice(0,-2)))+"px";
      div.style.top = String(6 + Number(node1.style.top.slice(0,-2)))+"px";
      console.log(div.style.top);
      div.style.width = "0px";
      div.style.height = offset + "px";
      div.style.visibility = "visible";
      hide_Nodes(Node1.id, Node2.id, "Vertical");
      document.getElementsByClassName("connections")[0].appendChild(div);
    }
    
    // div.setAttribute("neighbours", "{'0' : {'0':'', '1':'', '2':'', '3':''}," +
    //                                 "'1' : {'0':'', '1':'', '2':'', '3':''},"+
    //                                 "'2' : {'0':'', '1':'', '2':'', '3':''},"+
    //                                 "'3' : {'0':'', '1':'', '2':'', '3':''}}");
    
    function add_neighbour(n1, n2, direction_n1_n2, Distance, direction, priority){
      Node1 = n1.getAttribute("id");
      Node2 = n2.getAttribute("id");
      directions = ["up", "right", "down", "left"];
      var second = directions.indexOf(direction_n1_n2);
      console.log("direction "+direction_n1_n2);
      console.log(second);
      if(second <= 1){
        second = directions[second + 2];
      }else{
        second = directions[second - 2];
      }
      console.log(second);
  
      var n_dir = "bi";
      if(direction == "to"){
          n_dir = "from";
      }else if(direction == "from"){
          n_dir = "to";
      }/*else if(direction == "bi"){
          n_dir == "bi";
      }*/
  
  
  
  
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
    
      console.log(n1.neighbours);
    
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
        console.log(weight)
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
              console.log("Found node id! " + nodes[i].getAttribute("id"));
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
          console.log(start_y - end_y);
          for(var i = 1; i < ((difference)**2)**0.5;i++){
              if(Math.sign(difference) == -1){
                console.log("hi");
                var node = get_node_by_coords(x, start_y + i);
                node.style.visibility = "hidden";
              }else if(Math.sign(difference) == 1){
                console.log("hi");
                var node = get_node_by_coords(x, start_y - i);
                node.style.visibility = "hidden";
              }
          }
      }else if(direction == "Horizontal"){
          y = parseInt(start.getAttribute("coords").replace("]","").replace("[","").split(",")[1]);
          start_x = parseInt(start.getAttribute("coords").replace("]","").replace("[","").split(",")[0]);
          end_x = parseInt(end.getAttribute("coords").replace("]","").replace("[","").split(",")[0]);
          difference = start_x - end_x;
          console.log(start_x - end_x);
          for(var i = 1; i < ((difference)**2)**0.5;i++){
              if(Math.sign(difference) == -1){
                console.log("hi");
                var node = get_node_by_coords(start_x + i, y);
                node.style.visibility = "hidden";
              }else if(Math.sign(difference) == 1){
                console.log("hi");
                var node = get_node_by_coords(start_x - i,y);
                node.style.visibility = "hidden";
              }
          }
      }
  
  
    }
  
    function connect(Node1,Node2,attr){
      var n1 = document.getElementById(Node1);
      var n2 = document.getElementById(Node2);
      console.log(get_coords(n1.getAttribute("coords")), get_coords(n2.getAttribute("coords")));
  
      var attributes = attr.split(",");
      var Distance = attributes[0];
      var direction = attributes[1];
      var priority = attributes[2];
  
      console.log(Distance);
      console.log(direction);
      console.log(priority);
  
      if(get_coords(n1.getAttribute("coords"))[0] == get_coords(n2.getAttribute("coords"))[0]){
        connect_via_y(n1, n2, 50);
        if(get_coords(n1.getAttribute("coords"))[1] > get_coords(n2.getAttribute("coords"))[1]){
          add_neighbour(n1,n2,"up", Distance, direction, priority);
        }else{
          add_neighbour(n1,n2,"down", Distance, direction, priority);
        }
      }else if(get_coords(n1.getAttribute("coords"))[1] == get_coords(n2.getAttribute("coords"))[1]){
        connect_via_x(n1, n2, 50);
        if(get_coords(n1.getAttribute("coords"))[0] > get_coords(n2.getAttribute("coords"))[0]){
          add_neighbour(n1,n2,"left", Distance, direction, priority);
        }else{
          add_neighbour(n1,n2,"right", Distance, direction, priority);
        }
      }else{
        console.log("sorry cannot link");
      }
    
    
      console.log("Connected.");
      connecting = false;
      console.log("WIPING PAIR");
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
        console.log(node[i].getAttribute("type"));
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
      // console.log(x,y);
      return unbracket;
  
    }
  
    var connecting = false;
    var pair = [];
    function connect_button(){
      connecting = true;
      console.log(connecting);
    }
  
      function add_connect_node(id){
        if(pair.length < 2){
        pair.push(id);
        console.log("I'm here");
      }
  
      if(pair.length >= 2){
          // Wipe the buttons
          document.getElementById("node_buttons").style.display = "none";
          // Show the form
          document.getElementById("lane_info").style.display = "block";
          // Set up submission
          console.log("Opened connection menu");
          // Setup the submission button
          console.log(pair);
          const getLaneData = () => {
            // Parse the form data
                const dir = document.querySelector('input[name="direction"]:checked').value;
                const priority = document.getElementById("priority").value;
                const dist = document.getElementById("distance").value;
                var parsedStr = `${dist},${dir},${priority},`;
                console.log(parsedStr);
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
       console.log("here");
      // var menu = document.getElementsByClassName("item-selector")[0];
      // var selector = document.getElementById("selector");
      // menu.style.visibility = "visible";
      var selector = document.querySelector('input[name="group2"]:checked').value;
      var grid = document.getElementsByClassName("grid")[0];
      // var val = selector.value.valueOf();
  //    document.getElementsByClassName("node")[id].type = selector.value;
    
      if(selector == "connect"){
  //      document.getElementById(id).style.background = "Blue";
          console.log("Connecting...");
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
      // console.log("here");
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
  
      console.log(String(document.getElementById(id).style.background));
      console.log(String(selected));
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
         console.log(connecting);
  
        if(div.getAttribute("type") == "undefined" || document.getElementById("node_type").value == "" ){
            console.log("Indeterminate state");
              set_type_radio(id);
        }else if(connecting == true){
              console.log("Connecting");
              add_connect_node(div.id);
        }else{
        console.log(div.getAttribute("type"));
        if(!connecting){
            console.log("CLICK - not connecting");
            console.log(pair);
            // Display the menu (modal)
            node_menu.open();
        //   var menu = document.getElementsByClassName("item-selector")[0].cloneNode(true);
        //   menu.id = "temp";
        //   document.getElementsByClassName("temp-select")[0].appendChild(menu);
        //   var grid = document.getElementsByClassName("grid")[0];
        //   menu.style.visibility = "visible";
        //   grid.style.visibility = "hidden";
        //   console.log(menu.childNodes);
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
        console.log("Connecting...");
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
        console.log("Cancelling");
        node_menu.close();
        console.log(pair);
    }
  
  
    
    var rows;
    var columns;
    var spacing;
    
    function createGrid(){
        document.getElementById("dim-form").style.display = "none";
        document.getElementById("grid-builder").style.display = "block";
      // clearDoc();
      // Clear the grid
      document.getElementsByClassName("grid")[0].innerHTML = "";
    
       var rows = document.getElementById("length").value;
       var columns = document.getElementById("width").value;
       var spacing = 50;
    
      var nodes = 0;
    
      for(var i = 0; i < columns; i++){
        for(var x = 0; x < rows; x++){
          var row = String(x);
          var colunm = String(i);
          var id = "[" + row + "," + colunm + "]";
          // var x = row;
          // var y = column;
          var left = 50 * x + spacing;
          var top = 50 * i + spacing;
    //        addBox(id, left, top);
    
    
          if(x == rows - 1|| i == columns - 1){
    
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
    
     function export_js_db(){
      str = "{";
      var nodes = document.getElementsByClassName("node");
      for(var i = 0; i < nodes.length; i++){
        if(nodes[i].getAttribute("type") != "undefined"){
          var json_str = get_json_db(nodes[i]);
          console.log(i + " " +nodes.length);
          str += json_str + ",";
    
        }
      }
      str = str.slice(0,-1) + "}";
      console.log(str);
      post_data(str)
      return str;
    }
    
    
    function export_json(){
         var str = export_js_gen() + "||" + export_js_db();
         post_data(str);
         console.log(str);
        return str;
    }
    function get_json_db(node){
      var id = node.id;
      var type = node.getAttribute("type");
      var neighbours = node.getAttribute("neighbours");
    // console.log(str);
       return "\"" + id + "\" :{" + "\"type\":\"" + type + "\", \"neighbours\" : " + neighbours + "}";
    }
    
    function export_js_gen(){
     str = "{ \"dimensions\" : " + "[" + rows + "," + colunms + "], \"nodes\" : {" ;
     var nodes = document.getElementsByClassName("node");
     for(var i = 0; i < nodes.length; i++){
       if(nodes[i].getAttribute("type") != "undefined"){
         var json_str = get_json_gen(nodes[i]);
    //     console.log(i + " " +nodes.length);
         str += json_str + ",";
    
       }
     }
     str = str.slice(0,-1) + "}}";
    // console.log(str);
     return str;
    }
    
    function get_json_gen(node){
     var id = node.id;
     var type = node.getAttribute("type");
     var neighbours = node.getAttribute("neighbours");
     var coords = node.getAttribute("coords");
     return "\"" + id + "\" :{" + "\"type\":\"" + type + "\", \"neighbours\" : " + neighbours + ",\"coords\" : " + coords + "}";
    }
    
    
    // document.body.onload = addElement;