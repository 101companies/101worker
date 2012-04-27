package org.softlang.igraph;

import com.hp.hpl.jena.ontology.OntModel;
import com.hp.hpl.jena.rdf.model.ModelFactory;
import com.hp.hpl.jena.rdf.model.Property;

public final class Model {
	private static OntModel model = ModelFactory.createOntologyModel();
	
	public static OntModel Get(){
		return model;
	}
	
	final static Property IMPLEMENTATION_MEMBERS =  model.createProperty("http://data101companies.org/data//schema#implementationmembers");
}
