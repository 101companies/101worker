package org.softlang.igraph;

import java.io.IOException;
import java.io.InputStream;
import java.net.URL;
import java.net.URLConnection;

import com.hp.hpl.jena.ontology.OntModel;
import com.hp.hpl.jena.rdf.model.*;
import com.hp.hpl.jena.vocabulary.VCARD;


public class Main {

	/**
	 * @param args
	 * @throws IOException 
	 */
	public static void main(String[] args) throws IOException {
		// create an empty model
		OntModel model = Model.Get();
		
		String finalUrlString = "http://black42.uni-koblenz.de/production/101worker/dumps/Wiki101Full.rdf";
		
		URL url = new URL(finalUrlString);
        URLConnection connection = url.openConnection(); 
		InputStream in = connection.getInputStream();
		if (in == null) {
			throw new IllegalArgumentException(
					"URL: " + finalUrlString + " not found");
		}

		// read the RDF/XML file
		model.read(in, null);
		String HASKELL_THEME = "http://data101companies.org/data/Category/Haskell_theme";
		Resource r = model.getResource(HASKELL_THEME) ;
		System.out.print(r.toString());
		StmtIterator props = r.listProperties(Model.IMPLEMENTATION_MEMBERS);
		
		while (props.hasNext()) {
		    Statement stmt      = props.nextStatement();  // get next statement
		    Resource  subject   = stmt.getSubject();     // get the subject
		    Property  predicate = stmt.getPredicate();   // get the predicate
		    RDFNode   object    = stmt.getObject();      // get the object

		    	   System.out.print(subject.toString());
				    System.out.print(" " + predicate.toString() + " ");
				    if (object instanceof Resource) {
				       System.out.print(object.toString());
				    } else {
				        // object is a literal
				        System.out.print(" \"" + object.toString() + "\"");
				    }

				    System.out.println(" .");
		}

		// write it to standard out
		//model.write(System.out);
	}

}
