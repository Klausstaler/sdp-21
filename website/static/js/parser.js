export function export_js(){
  str = "{";
  var nodes = document.getElementsByClassName("node");
  for(int i = 0; i < nodes.length; i++){
    if(node[i].getAttribute("type") != "undefined"){
      var json_str = get_json(node[i]);
      str += json_str;
    }
  }
  str += "}";
  //console.log(str);
  return str;
}

function get_json(node){
  var id = node.id;
  var type = node.getAttribute("type");
  var neighbours = node.getAttribute("neighbours");
  return id + ":{" + "'type':'" + type + "', 'neighbours' : {" + neighbours + "}}"
}


// export {export};
