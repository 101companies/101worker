package org.softlang.igraph;

import java.util.HashMap;
import java.util.Map;

import org.jgraph.graph.Edge;
import org.jgrapht.ext.ComponentAttributeProvider;

public class EdgeAttributeProvider101<DefaultEdge> implements ComponentAttributeProvider<DefaultEdge> {

	@Override
	public Map<String, String> getComponentAttributes(DefaultEdge e) {
		
		Map<String,String> attr = new HashMap<String, String>();
		attr.put("color", "blue");
		return attr;
	}
}


