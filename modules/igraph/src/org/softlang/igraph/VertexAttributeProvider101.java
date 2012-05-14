package org.softlang.igraph;

import java.util.HashMap;
import java.util.Map;

import org.jgrapht.ext.ComponentAttributeProvider;

public class VertexAttributeProvider101 implements ComponentAttributeProvider<Vertex> {

	@Override
	public Map getComponentAttributes(Vertex v) {
		Map<String,String> attr = new HashMap<String, String>();
		
		if(v instanceof ConceptVertex){
			//attr.put("color", "blue");
			attr.put("style", "filled");
			attr.put("shape", "ellipse");
			return attr;
		}
		else if(v instanceof ImplementationVertex){
			attr.put("shape", "box");
			return attr;
		}
		return null;
	}

}
