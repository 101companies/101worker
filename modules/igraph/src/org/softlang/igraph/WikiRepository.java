package org.softlang.igraph;

import java.io.IOException;
import java.io.InputStream;
import java.net.URL;
import java.net.URLConnection;

import com.hp.hpl.jena.rdf.model.Model;
import com.hp.hpl.jena.rdf.model.ModelFactory;

public class WikiRepository {
	public static Model getModel() throws IOException{
		// create an empty model
		Model model = ModelFactory.createDefaultModel();

		String finalUrlString = "http://black42.uni-koblenz.de/production/101worker/Wiki101Full.rdf";

		URL url = new URL(finalUrlString);
		URLConnection connection = url.openConnection(); 
		InputStream in = connection.getInputStream();
		if (in == null) {
			throw new IllegalArgumentException(
					"URL: " + finalUrlString + " not found");
		}

		// read the RDF/XML file
		model.read(in, null);
		
		return model;
	}
}
