package org.softlang.igraph;

import org.jgrapht.ext.VertexNameProvider;

public class NameProvider101 implements VertexNameProvider<Vertex> {

	@Override
	public String getVertexName(Vertex v) {
		return String.valueOf(v.getName().hashCode());
	}

}
