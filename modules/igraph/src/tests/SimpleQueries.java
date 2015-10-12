package tests;

import static org.junit.Assert.*;

import org.junit.Test;
import org.softlang.igraph.WikiRepository;

import com.hp.hpl.jena.rdf.model.Model;
import com.hp.hpl.jena.rdf.model.Property;
import com.hp.hpl.jena.rdf.model.RDFNode;
import com.hp.hpl.jena.rdf.model.Resource;
import com.hp.hpl.jena.rdf.model.SimpleSelector;
import com.hp.hpl.jena.rdf.model.Statement;
import com.hp.hpl.jena.rdf.model.StmtIterator;

public class SimpleQueries {

	@Test
	public void getAllLanguages() {
			Model model = WikiRepository.getModel();

			// select all the resources with a VCARD.FN property
			// whose value ends with "Smith"
			StmtIterator iter = model.listStatements(
					new SimpleSelector(null, null, (RDFNode) null) {
						public boolean selects(Statement s) {
							System.out.println(s.getString());
							return s.getString().endsWith("Smith");
						}
					});

			while(iter.hasNext()){
				Statement stmt = iter.nextStatement();
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
				iter.next();
			}
			fail("failed to get model");
	}

}
