package tests;

import java.io.PrintWriter;

import org.junit.Test;

import org.jgrapht.*;
import org.jgrapht.ext.DOTExporter;
import org.jgrapht.ext.StringNameProvider;
import org.jgrapht.graph.*;
import org.softlang.igraph.NameProvider101;
import org.softlang.igraph.Vertex;

public class SimpleGraph {

	@SuppressWarnings("unchecked")
	@Test
	public void CreateDummyGraph(){
		DirectedGraph<Vertex, DefaultEdge> g =
	            new DefaultDirectedGraph<Vertex, DefaultEdge>(DefaultEdge.class);
		
		// add the vertices
		Vertex haskell = new Vertex("Haskell");
        g.addVertex(haskell);
        
        Vertex language = new Vertex("Language");
        g.addVertex(language);
        
        Vertex fpl = new Vertex("Functional Programming Language");
        g.addVertex(fpl);
        
        g.addEdge(fpl, language);
        g.addEdge(haskell, fpl);
        
		@SuppressWarnings("unchecked")
		DOTExporter dot = new DOTExporter(
        		new NameProvider101(), 
        		new StringNameProvider<Vertex>(), 
        		//new StringEdgeNameProvider<String>());
        		null);
       
        PrintWriter out = new java.io.PrintWriter(System.out);
        dot.export(out, g);
	}
}
