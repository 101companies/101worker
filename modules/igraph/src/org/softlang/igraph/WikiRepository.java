package org.softlang.igraph;

import java.io.IOException;
import java.io.InputStream;
import java.net.URL;
import java.net.URLConnection;

import com.hp.hpl.jena.ontology.OntModel;
import com.hp.hpl.jena.rdf.model.Model;
import com.hp.hpl.jena.rdf.model.ModelFactory;

public class WikiRepository {
	public static OntModel getModel() {
		// create an empty model
		OntModel model = ModelFactory.createOntologyModel();

		String finalUrlString = "http://black42.uni-koblenz.de/production/101worker/dumps/Wiki101Full.rdf";

		try{
			URL url = new URL(finalUrlString);
			URLConnection connection = url.openConnection(); 
			InputStream in = connection.getInputStream();
			if (in == null) {
				throw new IllegalArgumentException(
						"URL: " + finalUrlString + " not found");
			}
			
			// read the RDF/XML file
			model.read(in, null);
		}
		catch(IOException ex){
			return null;
		}

		return model;
	}
}
