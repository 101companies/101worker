package org.softlang.igraph;

import java.util.HashMap;
import java.util.Map;

import org.jgrapht.ext.ComponentAttributeProvider;

public class VertexAttributeProvider101 implements ComponentAttributeProvider<Vertex> {

	@Override
	public Map getComponentAttributes(Vertex v) {
		if(v instanceof ConceptVertex){
			Map<String,String> attr = new HashMap<String, String>();
			attr.put("color", "blue");
			return attr;
			
		}
		return null;
	}

}
