package org.softlang.igraph;

import java.util.HashMap;
import java.util.Map;

import org.jgrapht.ext.ComponentAttributeProvider;

public class EdgeAttributeProvider101 implements ComponentAttributeProvider<Object> {

	@Override
	public Map<String, String> getComponentAttributes(Object arg0) {
		Map<String,String> attr = new HashMap<String, String>();
		attr.put("color", "blue");
		return attr;
	}
}


