package org.softlang.igraph;

import com.hp.hpl.jena.ontology.OntModel;
import com.hp.hpl.jena.rdf.model.ModelFactory;
import com.hp.hpl.jena.rdf.model.Property;

public final class Model {
	private static OntModel model = WikiRepository.getModel();
	
	public static OntModel Get(){
		return model;
	}
	
	final private static String SCHEMA = "http://data101companies.org/data//schema#";
	
	final static Property IMPLEMENTATION_MEMBERS =  model.createProperty(SCHEMA + "implementationmembers");
	final static Property NAME = model.createProperty(SCHEMA + "name");
	
	// http://data101companies.org/data//schema#implementation
	final static Property IMPLEMENTATION = model.createProperty(SCHEMA + "implementation");
	
	// http://data101companies.org/data//schema#type
	final static Property TYPE = model.createProperty(SCHEMA + "type");
	
	// http://data101companies.org/data//schema#languages
	final static Property LANGUAGE = model.createProperty(SCHEMA + "languages");
	
	// http://data101companies.org/data//schema#technologies
	final static Property TECHNOLOGY = model.createProperty(SCHEMA + "technologies");
	
	// http://data101companies.org/data//schema#features
	final static Property FEATURE = model.createProperty(SCHEMA + "features");
}
