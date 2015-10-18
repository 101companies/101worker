package org.softlang.igraph.queries;

import org.jgrapht.DirectedGraph;
import org.jgrapht.graph.DefaultDirectedGraph;
import org.jgrapht.graph.DefaultEdge;
import org.softlang.igraph.ImplementationVertex;
import org.softlang.igraph.LanguageVertex;
import org.softlang.igraph.Model;
import org.softlang.igraph.Query;
import org.softlang.igraph.Vertex;

import ru.yandex.bolts.collection.ListF;
import ru.yandex.bolts.function.Function1B;
import ru.yandex.bolts.function.Function1V;

import com.hp.hpl.jena.rdf.model.Resource;
import com.hp.hpl.jena.rdf.model.Statement;

public class ImplementationsUseLanguageQuery extends Query {

	public ImplementationsUseLanguageQuery(String filter) {
		super(filter);
	}

	@Override
	public DirectedGraph<Vertex, DefaultEdge> Execute() {
		final DirectedGraph<Vertex, DefaultEdge> g = new DefaultDirectedGraph<Vertex, DefaultEdge> (DefaultEdge.class);
		final Vertex l = new LanguageVertex(_filter);
		g.addVertex(l);
		
		ListF<Statement> impls = GetImplementations();

		ListF<Statement> filteredImpls = impls.filter(new Function1B<Statement>() {
			public boolean apply(Statement stm) {
				String name = stm.getSubject().toString();
				Resource r = _model.getResource(name);

				if(r.hasProperty(Model.LANGUAGE)){
					String lang = r.getPropertyResourceValue(Model.LANGUAGE).toString();
					if(lang.contentEquals("http://data101companies.org/data/Language/" + _filter)){
						return true;
					}
					else return false;
				}
				else return false;
			}
		});
		
		filteredImpls.forEach(new Function1V<Statement>(){
			@Override
			public void apply(Statement impl) {
				Resource r = impl.getSubject();
				Statement name = r.getProperty(Model.NAME);
				
				Vertex vImpl = new ImplementationVertex(name.getObject().toString());
				vImpl.set_resource(name.getSubject().toString());
				g.addVertex(vImpl);
				g.addEdge(l, vImpl);	
			}
		});
		
		return g;
	}

}
