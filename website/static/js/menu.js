// import {export_js} from './parser.js';




// PARSING & EXPORTING /////////////////////////////////////////////////////////////////////////////////////////////////////////////////

function post_data(json_str){ // Posts the string to the server

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
        //console.log(i + " " +nodes.length);
        str += json_str + ",";

      }
    }
    str = str.slice(0,-1) + "}";
    //console.log(str);
    post_data(str)
    return str;
  }


  function export_json(){
       var str = export_js_gen() + "||" + export_js_db()
       post_data(str)
       //console.log(str)
      return str
  }
  function get_json_db(node){
    var id = node.id;
    var type = node.getAttribute("type");
    var neighbours = node.getAttribute("neighbours");
  // console.log(str);
     return "\"" + id + "\" :{" + "\"type\":\"" + type + "\", \"neighbours\" : " + neighbours + "}"
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
   return "\"" + id + "\" :{" + "\"type\":\"" + type + "\", \"neighbours\" : " + neighbours + ",\"coords\" : " + coords + "}"
  }

  // ARROWS ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

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

  // CONNECTIONS //////////////////////////////////////////////////////////////////////////////////////////////////////////////////

  
  function connect_via_x(Node1, Node2, d, boxWidth){ // left to right
    var node1;
    var node2;
    if(get_coords(Node1.getAttribute("coords"))[0] > get_coords(Node2.getAttribute("coords"))[0]){
      node1 = Node2;
      node2 = Node1;
//    var arrow = document.createElement("div")
//    arrow.appendChild(create_arrow("left"))
////    arrow.className = "arrow-down";
//    arrow.style.left = String(Number(10 + Number(node2.style.left.slice(0,-2))) - 4)+"px"
////    console.log(end);
//    arrow.style.top = String(Number(6 + Number(node1.style.top.slice(0,-2))) - 6)+"px";
//    arrow.style.visibility = "visible";
//    arrow.style.position = "absolute";
  
    }else{
      node1 = Node1;
      node2 = Node2;
//                var arrow = document.createElement("div")
//    arrow.appendChild(create_arrow("right"))
////    arrow.className = "arrow-down";
//    arrow.style.left = String(Number(10 + Number(node1.style.left.slice(0,-2))) - 4)+"px"
////    console.log(end);
//    arrow.style.top = String(Number(6 + Number(node1.style.top.slice(0,-2))) - 6)+"px";
//    arrow.style.visibility = "visible";
//    arrow.style.position = "absolute";
    }
    var distance = Math.sqrt((get_coords(node2.getAttribute("coords"))[0] - get_coords(node1.getAttribute("coords"))[0])**2);
    var offset = boxWidth * distance;
    //console.log(String(distance));
  
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
    //console.log(line.style.top);
    line.style.width = offset + "px";
    line.style.height = "0px";
    line.style.visibility = "visible";
    hide_Nodes(Node1.id, Node2.id, "Horizontal");
    line.style.position = "absolute";

    console.log(mid);
    console.log(dist.style.left);
    document.getElementsByClassName("connections")[0].appendChild(line);
    document.getElementsByClassName("connections")[0].appendChild(dist);
    //    document.getElementsByClassName("connections")[0].appendChild(arrow);

  }
  
  function connect_via_y(Node1, Node2, d,boxHeight){ //top to bottm
    var node1;
    var node2;

    var mid = end + (offset/2);

    if(get_coords(Node1.getAttribute("coords"))[1] > get_coords(Node2.getAttribute("coords"))[1]){
      node1 = Node2;
      node2 = Node1;

//          var arrow = document.createElement("div")
//    arrow.appendChild(create_arrow("up"))
////    arrow.className = "arrow-down";
//    arrow.style.left = String(Number(10 + Number(node1.style.left.slice(0,-2))) - 4)+"px"
////    console.log(end);
//    arrow.style.top = String(Number(6 + Number(node1.style.top.slice(0,-2))) - 6)+"px";
//    arrow.style.visibility = "visible";
//    arrow.style.position = "absolute";
  
    }else{
      node1 = Node1;
      node2 = Node2;

//                var arrow = document.createElement("div")
//    arrow.appendChild(create_arrow("down"))
////    arrow.className = "arrow-down";
//    arrow.style.left = String(Number(10 + Number(node1.style.left.slice(0,-2))) - 4)+"px"
////    console.log(end);
//    arrow.style.top = String(Number(6 + Number(node2.style.top.slice(0,-2))) - 6)+"px";
//    arrow.style.visibility = "visible";
//    arrow.style.position = "absolute";
    }
    var distance = Math.sqrt((get_coords(node2.getAttribute("coords"))[1] - get_coords(node1.getAttribute("coords"))[1])**2);
//    console.log(distance);
    var offset = boxHeight * distance;

    var start = Number(10 + Number(node1.style.left.slice(0,-2)));
    var end = Number(6 + Number(node1.style.top.slice(0,-2)));

    var line = document.createElement("div");
    var dist = document.createElement("div");
    dist.appendChild(document.createTextNode(d));



    console.log("Drawing Now!!")
    // Draw Distance
    dist.className = "dist-label";
    dist.style.left = String(start - 25)+"px";
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
    directions = ["up", "right", "down", "left"];
    var second = directions.indexOf(direction_n1_n2);
    if(second <= 1){
      second = directions[second + 2];
    }else{
      second = directions[second - 2];
    }
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
  }
  
  function getAttributes() { // presents a prompt to define node attributes
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

  function get_node_by_coords(x,y){ // gets node by xy coords
    nodes = document.getElementsByClassName("node");
    for(var i = 0; i < nodes.length; i++){
        if(nodes[i].getAttribute("coords") == "[" + x + "," + y + "]"){
            return nodes[i];
        }
    };
  }

  function hide_Nodes(start, end, direction){ // hides all nodes between 2 nodes
    var start = document.getElementsByClassName("node")[start];
    var end = document.getElementsByClassName("node")[end];

    if(direction == "Vertical"){
        x = parseInt(start.getAttribute("coords").replace("]","").replace("[","").split(",")[0]);
        start_y = parseInt(start.getAttribute("coords").replace("]","").replace("[","").split(",")[1]);
        end_y = parseInt(end.getAttribute("coords").replace("]","").replace("[","").split(",")[1]);
        difference = start_y - end_y;
        for(var i = 1; i < ((difference)**2)**0.5;i++){
            if(Math.sign(difference) == -1){
              var node = get_node_by_coords(x, start_y + i);
              node.style.visibility = "hidden";
            }else if(Math.sign(difference) == 1){
              var node = get_node_by_coords(x, start_y - i);
              node.style.visibility = "hidden";
            }
        }
    }else if(direction == "Horizontal"){
        y = parseInt(start.getAttribute("coords").replace("]","").replace("[","").split(",")[1]);
        start_x = parseInt(start.getAttribute("coords").replace("]","").replace("[","").split(",")[0]);
        end_x = parseInt(end.getAttribute("coords").replace("]","").replace("[","").split(",")[0]);
        difference = start_x - end_x;
        for(var i = 1; i < ((difference)**2)**0.5;i++){
            if(Math.sign(difference) == -1){
              var node = get_node_by_coords(start_x + i, y);
              node.style.visibility = "hidden";
            }else if(Math.sign(difference) == 1){
              var node = get_node_by_coords(start_x - i,y);
              node.style.visibility = "hidden";
            }
        }
    }
  }

  function connect(Node1,Node2){
    var n1 = document.getElementById(Node1);
    var n2 = document.getElementById(Node2);
    var attributes = getAttributes().split(",");
    var Distance = attributes[0];
    var direction = attributes[1];
    var priority = attributes[2];

    if(get_coords(n1.getAttribute("coords"))[0] == get_coords(n2.getAttribute("coords"))[0]){
      connect_via_y(n1, n2, Distance, 50);
      if(get_coords(n1.getAttribute("coords"))[1] > get_coords(n2.getAttribute("coords"))[1]){
        add_neighbour(n1,n2,"up", Distance, direction, priority);
      }else{
        add_neighbour(n1,n2,"down", Distance, direction, priority);
      }
    }else if(get_coords(n1.getAttribute("coords"))[1] == get_coords(n2.getAttribute("coords"))[1]){
      connect_via_x(n1, n2, Distance, 50);
      if(get_coords(n1.getAttribute("coords"))[0] > get_coords(n2.getAttribute("coords"))[0]){
        add_neighbour(n1,n2,"left", Distance, direction, priority);
      }else{
        add_neighbour(n1,n2,"right", Distance, direction, priority);
      }
    }
   }

  // NODE CREATION & GRID MANAGEMENT ///////////////////////////////////////////////////////////////////////////////////////

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
    return unbracket;

  }

  var connecting = false;
  var pair = [];

   function add_connect_node(id){
      if(pair.length < 2){
      pair.push(id);
      //console.log(pair);
        }

    if(pair.length >= 2){
      connect(pair[0],pair[1]);
      connecting = false;
      pair = [];
    }
   }

  
  function node_options(id,menu){
    var selector = document.querySelector('input[name="group2"]:checked').value;
    var grid = document.getElementsByClassName("grid")[0];
    if(selector == "connect"){
        connecting = true;
        add_connect_node(id);
    }
    if(selector == "delete"){
      document.getElementById(id).style.background = "White";
      document.getElementsByClassName("node")[id].type = "undefined";
    }
    menu.style.visibility = "hidden";
    menu.remove();
    grid.style.visibility = "visible";
  }

    function set_type_radio(id){
    var selected = document.querySelector('input[name="group1"]:checked').value;
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
  }
  
  function add_node(id, coords, left, top){ // where modifier is last row, last colunm, bottom right or else
    var div = document.createElement("button");
    div.className = "node";
    div.id = id;
    div.type = "undefined";
    div.setAttribute("coords",coords);
    div.style.left = String(500 + Number(left))+"px";
    div.style.top = String(200 + Number(top))+"px";
    document.getElementsByClassName("grid")[0].appendChild(div);
    document.getElementById(id).onclick = function() {
      if(div.getAttribute("type") == "undefined" || document.querySelector('input[name="group1"]:checked').value == "undefined" ){
            set_type_radio(id);
      }else if(connecting == true){
            add_connect_node(div.id);
      }else{
      if(!connecting){

        var menu = document.getElementsByClassName("item-selector")[0].cloneNode(true);
        menu.id = "temp";
        document.getElementsByClassName("temp-select")[0].appendChild(menu);
        var grid = document.getElementsByClassName("grid")[0];
        menu.style.visibility = "visible";
        grid.style.visibility = "hidden";
        menu.childNodes[5].addEventListener("click", function(){
                node_options(id,menu);
        });
      }};
     }}

  var rows;
  var columns;
  var spacing;
  
  function createGrid(){
    document.getElementsByClassName("grid")[0].innerHTML = "";
     rows = document.getElementById("dims").value.split(",")[0];
     colunms = document.getElementById("dims").value.split(",")[1];;
     spacing = 50;
    var nodes = 0;
    for(var i = 0; i < colunms; i++){
      for(var x = 0; x < rows; x++){
        var row = String(x);
        var colunm = String(i);
        var id = "[" + row + "," + colunm + "]";
        var left = 50 * x + spacing;
        var top = 50 * i + spacing;
        if(x == rows - 1|| i == colunms - 1){
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
      }
    }
  }
