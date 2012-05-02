package org.softlang.igraph;

import org.jgrapht.DirectedGraph;
import org.jgrapht.graph.DefaultEdge;

import ru.yandex.bolts.collection.Cf;
import ru.yandex.bolts.collection.ListF;
import ru.yandex.bolts.collection.Tuple3;

import com.hp.hpl.jena.ontology.OntModel;
import com.hp.hpl.jena.rdf.model.Property;
import com.hp.hpl.jena.rdf.model.RDFNode;
import com.hp.hpl.jena.rdf.model.Resource;
import com.hp.hpl.jena.rdf.model.SimpleSelector;
import com.hp.hpl.jena.rdf.model.Statement;
import com.hp.hpl.jena.rdf.model.StmtIterator;

public abstract class Query {
	
	protected OntModel _model;
	protected String _filter;
	protected Query(String filter){
		_filter = filter;
	    _model  = Model.Get();
	}
	
	public String getFileName(){
		return _filter.trim().replace(" ", "-") + ".dot";
	}
	
	abstract DirectedGraph<Vertex, DefaultEdge> Execute();
	
	protected ListF<Statement> GetImplementations(){
		//get all implementations
		StmtIterator implementations = _model.listStatements(
				new SimpleSelector(null, Model.TYPE, (RDFNode) null) {
					public boolean selects(Statement s) {
						return s.getObject().toString().contentEquals("Implementation");
					}
				});

		ListF<Statement> impls = Cf.list(implementations.toList());
		return impls;
	}

	protected Tuple3<String, String, String> Lookup(Resource resource, Property prop) {
		return new Tuple3<String, String, String>(resource.getProperty(prop).getSubject().toString(),
				resource.getProperty(prop).getPredicate().toString(),resource.getProperty(prop).getObject().toString());
	}
	
	protected void DumpResourceProperties(Resource resource){
		StmtIterator props = resource.listProperties();
		
		while (props.hasNext()) {
			Statement stmt      = props.nextStatement();  // get next statement
			Resource  subject   = stmt.getSubject();     // get the subject
			Property  predicate = stmt.getPredicate();   // get the predicate
			RDFNode   object    = stmt.getObject();      // get the object
			System.out.println(subject.toString() + " : " + predicate.toString() + " : " + object.toString());
		}
	}
}


