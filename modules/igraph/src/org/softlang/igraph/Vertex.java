package org.softlang.igraph;

public class Vertex {
 private String _name;
 private String _resource;
 
 public Vertex(String name){
	 _name = name;
 }
 
 public Vertex(String name, String resource){
	 _name = name;
	 set_resource(resource);
 }
 
 public String getName(){
	 return _name;
 }
 
 public String toString(){
	return _name; 
 }

public String get_resource() {
	return _resource;
}

public void set_resource(String _resource) {
	this._resource = _resource;
}
}
