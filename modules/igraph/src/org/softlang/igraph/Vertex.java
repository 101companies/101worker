package org.softlang.igraph;

public class Vertex {
 private String _name;
 
 public Vertex(String name){
	 _name = name;
 }
 
 public String getName(){
	 return _name;
 }
 
 public String toString(){
	return _name; 
 }
}
