// import {export_js} from './parser.js';

function post_data(json_str){

var http = new XMLHttpRequest();
var url = 'get_data.php';
var params = 'orem=ipsum&name=binny';
http.open('POST', "/generator/", true);
console.log(json_str)
//Send the proper header information along with the request
http.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');

http.onreadystatechange = function() {//Call a function when the state changes.
    if(http.readyState == 4 && http.status == 200) {
//        alert(http.responseText);
    }
}
http.send("data=" + json_str);
}

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
  document.getElementsByClassName("connections")[0].appendChild(div);
}

// div.setAttribute("neighbours", "{'0' : {'0':'', '1':'', '2':'', '3':''}," +
//                                 "'1' : {'0':'', '1':'', '2':'', '3':''},"+
//                                 "'2' : {'0':'', '1':'', '2':'', '3':''},"+
//                                 "'3' : {'0':'', '1':'', '2':'', '3':''}}");

function add_neighbour(n1, n2, direction_n1_n2 ,Distance){
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

  if(n1.hasAttribute("neighbours")){
    n1.setAttribute("neighbours", n1.getAttribute("neighbours").slice(0, -1) + ",\"" + direction_n1_n2 + "\":[" + Node2 + "," + Distance + "]}");
  }else{
    n1.setAttribute("neighbours", "{\"" + direction_n1_n2 + "\":[" + Node2 + "," + Distance + "]}");
  }

  if(n2.hasAttribute("neighbours")){
    n2.setAttribute("neighbours", n2.getAttribute("neighbours").slice(0, -1) + ",\"" + second + "\":[" + Node1 + "," + Distance + "]}");
  }else{
    n2.setAttribute("neighbours", "{\"" + second + "\":[" + Node1 + "," + Distance + "]}");
  }

  console.log(n1.neighbours);

}

function getDistance() {
  var distance = prompt("Please enter the distance between these two nodes", "");
  if (distance != null) {
    return distance;
  }
}

function connect(Node1,Node2){
  var n1 = document.getElementById(Node1);
  var n2 = document.getElementById(Node2);
  console.log(get_coords(n1.getAttribute("coords")), get_coords(n2.getAttribute("coords")));
  var Distance = getDistance();
  if(get_coords(n1.getAttribute("coords"))[0] == get_coords(n2.getAttribute("coords"))[0]){
    // if(){
    // }
    connect_via_y(n1, n2, 50);

    if(get_coords(n1.getAttribute("coords"))[1] > get_coords(n2.getAttribute("coords"))[1]){
      add_neighbour(n1,n2,"up", Distance);
    }else{
      add_neighbour(n1,n2,"down", Distance);
    }
  }else if(get_coords(n1.getAttribute("coords"))[1] == get_coords(n2.getAttribute("coords"))[1]){
    connect_via_x(n1, n2, 50);
    if(get_coords(n1.getAttribute("coords"))[0] > get_coords(n2.getAttribute("coords"))[0]){
      add_neighbour(n1,n2,"left", Distance);
    }else{
      add_neighbour(n1,n2,"right", Distance);
    }
  }else{
    console.log("sorry cannot link");
  }


  console.log("Connected.");


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

function set_type(id,menu){
  // console.log("here");
  // var menu = document.getElementsByClassName("item-selector")[0];
  // var selector = document.getElementById("selector");
  // menu.style.visibility = "visible";
  var selector = menu.childNodes[3];
  var grid = document.getElementsByClassName("grid")[0];
  // var val = selector.value.valueOf();
  document.getElementsByClassName("node")[id].type = selector.value;

  if(selector.value == "Robot"){
    document.getElementById(id).style.background = "Blue";
  }
  if(selector.value == "RFID"){
    document.getElementById(id).style.background = "Red";
  }
  if(selector.value == "Shelf"){
    document.getElementById(id).style.background = "Yellow";
  }

  menu.style.visibility = "hidden";
  menu.remove();
  grid.style.visibility = "visible";

}

function add_node(id, coords, left, top){ // where modifier is last row, last colunm, bottom right or else
  var div = document.createElement("button");
  div.className = "node";
  div.id = id;
  div.type = "undefined";
  div.setAttribute("coords",coords);

// /  // div.style.position = "absolute";
  div.style.left = String(192 + Number(left))+"px";
  // div.style.right = "0px";
  div.style.top = String(143 + Number(top))+"px";
  document.getElementsByClassName("grid")[0].appendChild(div);
  document.getElementById(id).onclick = function() {

    if(!connecting){

      var menu = document.getElementsByClassName("item-selector")[0].cloneNode(true);
      menu.id = "temp";
      document.getElementsByClassName("temp-select")[0].appendChild(menu);
      var grid = document.getElementsByClassName("grid")[0];
      menu.style.visibility = "visible";
      grid.style.visibility = "hidden";
      console.log(menu.childNodes);
      menu.childNodes[5].addEventListener("click", function(){

        set_type(id,menu);

      });


    }else{
      if(pair.length < 2){
        pair.push(div.id);
        console.log(pair);

      }

      if(pair.length >= 2){
        connect(pair[0],pair[1]);
        connecting = false;
        pair = [];
      }

    }

};
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


var rows = 9;
var colunms = 9;
var spacing = 50;

function createGrid(){
  // clearDoc();

  var nodes = 0;

  for(var i = 0; i < colunms; i++){
    for(var x = 0; x < rows; x++){
      var row = String(x);
      var colunm = String(i);
      var id = "[" + row + "," + colunm + "]";
      // var x = row;
      // var y = column;
      var left = 50 * x + spacing;
      var top = 50 * i + spacing;
      addBox(id, left, top);


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
     var str = export_js_gen() + "||" + export_js_db()
     post_data(str)
     console.log(str)
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


// document.body.onload = addElement;
