package org.softlang.igraph.queries;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

import org.jgrapht.DirectedGraph;
import org.jgrapht.graph.DefaultDirectedGraph;
import org.jgrapht.graph.DefaultEdge;
import org.softlang.igraph.ImplementationVertex;
import org.softlang.igraph.Model;
import org.softlang.igraph.Query;
import org.softlang.igraph.ThemeVertex;
import org.softlang.igraph.Vertex;

import ru.yandex.bolts.collection.Cf;
import ru.yandex.bolts.collection.ListF;
import ru.yandex.bolts.function.Function1V;

import com.hp.hpl.jena.rdf.model.RDFNode;
import com.hp.hpl.jena.rdf.model.Resource;
import com.hp.hpl.jena.rdf.model.Statement;

public class ThemeMembersQuery extends Query {

	public ThemeMembersQuery(String filter) {
		super(filter);	//filter -- name of the theme
	}

	@Override
	public DirectedGraph<Vertex, DefaultEdge> Execute() {
		//All implementations being members of a theme.
		String theme = "http://data101companies.org/data/Category/" + _filter;
		Resource r = _model.getResource(theme) ;
		Iterator<Statement> implIter = r.listProperties(Model.IMPLEMENTATION_MEMBERS).toList().iterator();

		final List<Resource> result = new ArrayList<Resource>();

		while (implIter.hasNext()) {
			Statement impl      = implIter.next();  // get next statement
			RDFNode   object    = impl.getObject(); // get the object

			if (object instanceof Resource) {
				Resource name = _model.getResource(impl.getObject().toString());
				//System.out.println(name);
				result.add(name);
			} else {
				// object is a literal
				System.out.print(" \"" + object.toString() + "\"");
			}
		}
		
		final DirectedGraph<Vertex, DefaultEdge> g = new DefaultDirectedGraph<Vertex, DefaultEdge> (DefaultEdge.class);
		final Vertex t = new ThemeVertex(_filter);
		g.addVertex(t);
		
		ListF<Resource> res = Cf.list(result);
		
		res.forEach(new Function1V<Resource>(){
			@Override
			public void apply(Resource arg) {
				String name = Lookup((Resource)arg, Model.NAME).get3();
				String res = Lookup((Resource)arg, Model.NAME).get1();
				Vertex v = new ImplementationVertex(name);
				v.set_resource(res);
				g.addVertex(v);
				g.addEdge(t, v);
			}});
		
		
		return g;
	}
}