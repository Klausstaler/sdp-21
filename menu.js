
function connect_via_x(Node1, Node2, boxWidth){ // left to right
  var start = Node1.left;
  var node1_x = Node1.coords[0];
  var node2_x = Node1.coords[0];
  var distance = node2_x - node1_x;
  var offset = boxWidth * distance;

  var div = document.createElement("div");
  div.className = "line";
  div.left = start+"px";
  div.width = offset + "px";
  div.height = "1px";
}

function connect_via_ys(Node1, Node2, boxHeight){ //top to bottm
  var start = Node1.top;
  var node1_y = Node1.coords[0];
  var node2_y = Node1.coords[0];
  var distance = node1_y - node2_y;
  var offset = boxHeight * distance;

  var div = document.createElement("div");
  div.className = "line";
  div.top = start+"px";
  div.height = offset + "px";
  div.width = "1px";
}



function addBox(id, left,top) {
  var div = document.createElement("div");
  div.className = "box";
  // div.id = id;
  div.style.left = String(150 + Number(left))+"px";
  div.style.top = String(50 + Number(top))+"px";
  document.getElementsByClassName("grid")[0].appendChild(div);
}


function copyNodeStyle(sourceNode, targetNode) {
    const computedStyle = window.getComputedStyle(sourceNode);
    Array.from(computedStyle).forEach(key => targetNode.style.setProperty(key, computedStyle.getPropertyValue(key), computedStyle.getPropertyPriority(key)))
  }

function set_type(id,menu){
  console.log("here");
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
  if(selector.value == "QR Code"){
    document.getElementById(id).style.background = "Black";
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
  // div.style.position = "absolute";
  div.style.left = String(140 + Number(left))+"px";
  // div.style.right = "0px";
  div.style.top = String(42.5 + Number(top))+"px";
  document.getElementsByClassName("grid")[0].appendChild(div);
  document.getElementById(id).onclick = function() {
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
};
}


function createGrid(){
  // clearDoc();
  var rows = 15;
  var colunms = 10;
  var spacing = 50;
  var nodes = 0;

  for(var i = 0; i < colunms; i++){
    for(var x = 0; x < rows; x++){
      var row = String(x);
      var colunm = String(i);
      var id = "(" + row + "," + colunm + ")";

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
// document.body.onload = addElement;
