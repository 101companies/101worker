package org.softlang.igraph;

import java.io.IOException;
import java.io.PrintWriter;
import java.io.FileWriter;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;

import org.jgrapht.DirectedGraph;
import org.jgrapht.ext.DOTExporter;
import org.jgrapht.ext.StringNameProvider;
import org.jgrapht.graph.DefaultDirectedGraph;
import org.jgrapht.graph.DefaultEdge;
import org.softlang.igraph.queries.ImplementationsUseLanguageQuery;
import org.softlang.igraph.queries.ThemeMembersQuery;

import ru.yandex.bolts.collection.Cf;
import ru.yandex.bolts.collection.ListF;
import ru.yandex.bolts.collection.Tuple3;
import ru.yandex.bolts.function.Function;
import ru.yandex.bolts.function.Function1B;
import ru.yandex.bolts.function.Function1V;

import com.hp.hpl.jena.enhanced.Implementation;
import com.hp.hpl.jena.ontology.OntModel;
import com.hp.hpl.jena.rdf.model.*;

// We use the following library which adds some functional programming primitives to Java: https://bitbucket.org/stepancheg/bolts/wiki/Home

public class Main {

	public static Function<Statement, String> getSubjName() {
	    return new Function<Statement, String>() {
	      public String apply(Statement s) { 
	        return s.getSubject().toString();
	      }
	    };
	  }
	
	/**
	 * @param args
	 * @throws IOException 
	 */
	public static void main(String[] args) throws IOException {
		System.out.println("hi there");
		
		List<Query> queries = new ArrayList<Query>();
		
		queries.add(new ThemeMembersQuery("Haskell_theme"));
		queries.add(new ImplementationsUseLanguageQuery("Haskell"));
		
		Cf.list(queries).forEach(new Function1V<Query>() {
			public void apply(Query q) {
				DOTExporter dot = new DOTExporter(
		        		new NameProvider101(), 
		        		new StringNameProvider<Vertex>(), 
		        		//new StringEdgeNameProvider<String>());
		        		null);
				
				// PrintWriter out = new java.io.PrintWriter(System.out);
				PrintWriter out;
				try {
					out = new PrintWriter(new FileWriter(q.getFileName()));
				    dot.export(out, q.Execute());
				} catch (IOException e) {
					e.printStackTrace();
					System.exit(-1);
				}   
			}
		});
		
		final OntModel model = Model.Get();
		final DirectedGraph<Vertex, DefaultEdge> g1 = new ImplementationsUseLanguageQuery("Haskell").Execute();
		
		Cf.set(g1.vertexSet()).forEach(new Function1V<Vertex>(){
			public void apply(final Vertex v) {
				if(v instanceof ImplementationVertex){
					Resource r = model.getResource(v.get_resource());
					Cf.list(r.listProperties(Model.TECHNOLOGY).toList()).forEach(new Function1V<Statement>(){
						@Override
						public void apply(Statement st) {
							String t = st.getObject().toString();
							Resource techRes = model.getResource(t);
							String  val = techRes.getProperty(Model.NAME).getObject().toString(); 
							System.out.println(val);
							
							Vertex technology = new TechnologyVertex(val);
							g1.addVertex(technology);
							g1.addEdge(v,  technology);
						}});	
				}
			}});
		
		Cf.set(g1.vertexSet()).forEach(new Function1V<Vertex>(){
			public void apply(final Vertex v) {
				if(v instanceof ImplementationVertex){
					Resource r = model.getResource(v.get_resource());
					Cf.list(r.listProperties(Model.MOTIVATION_LINK).toList()).forEach(new Function1V<Statement>(){
						@Override
						public void apply(Statement st) {
							String t = st.getObject().toString();
							Resource res = model.getResource(t);
							
							if(res.getProperty(Model.TYPE).getObject().toString().contentEquals("Concept")){
								String val = res.getProperty(Model.NAME).getObject().toString();
								System.out.println(val);
								
								Vertex concept = new ConceptVertex(val);
								g1.addVertex(concept);
								g1.addEdge(v,  concept);
							}

						}});	
				}
			}});
		
		DOTExporter dot = new DOTExporter(
        		new NameProvider101(), 
        		new StringNameProvider<Vertex>(), 
        		//new StringEdgeNameProvider<String>());
        		null,
        		new VertexAttributeProvider101(),
        		null);
		PrintWriter out;
		try {
			out = new PrintWriter(new FileWriter("Full_Haskel.dot"));
		    dot.export(out, g1);
		} catch (IOException e) {
			e.printStackTrace();
			System.exit(-1);
		}   

		//Resource r = model.getResource("http://data101companies.org/data/Implementation/haskell");
		//DumpResourceProperties(r);
		
		//GetAllImplementationsUseLanguage(model, "Haskell");
	}

	private static List<String> GetAllImplementationsUseLanguage(final OntModel model, final String languageName){
		// http://data101companies.org/data/Implementation/haskell : http://data101companies.org/data//schema#type : Implementation
		//http://data101companies.org/data/Implementation/haskell : http://data101companies.org/data//schema#languages : http://data101companies.org/data/Language/Haskell_98
		
		//get all implementations
		StmtIterator implementations = model.listStatements(
		    new SimpleSelector(null, Model.TYPE, (RDFNode) null) {
		        public boolean selects(Statement s) {
		        	 return s.getObject().toString().contentEquals("Implementation");
		        }
		    });
		
		ListF<Statement> impls = Cf.list(implementations.toList());
		
		//filter them by haskell/haskell_98 usage
		ListF<Statement> haskellImpls = impls.filter(new Function1B<Statement>() {
			public boolean apply(Statement stm) {
				String name = stm.getSubject().toString();
				Resource r = model.getResource(name);
				
				if(r.hasProperty(Model.LANGUAGE)){
					String lang = r.getPropertyResourceValue(Model.LANGUAGE).toString();
					if(lang.contentEquals("http://data101companies.org/data/Language/" + languageName)){
						return true;
					}
					else return false;
				}
				else return false;
			}
		});
		
		List<String> res = haskellImpls.map(getSubjName());
		
		DumpResourceProperties(model.getResource(res.get(0)));
		return res;
	}
	
	private static ListF<String> GetThemeMembers(OntModel model, String themeName){
		//All implementations being members of a theme.
		String theme = "http://data101companies.org/data/Category/" + themeName;
		Resource r = model.getResource(theme) ;
		Iterator<Statement> implIter = r.listProperties(Model.IMPLEMENTATION_MEMBERS).toList().iterator();
		
		final List<String> result = new ArrayList<String>();
		
		while (implIter.hasNext()) {
			Statement impl      = implIter.next();  // get next statement
			RDFNode   object    = impl.getObject(); // get the object
			
			if (object instanceof Resource) {
				String name = Lookup((Resource)object, Model.NAME).get3();
				//ystem.out.println(name);
				result.add(name);
			} else {
				// object is a literal
				System.out.print(" \"" + object.toString() + "\"");
			}
		}
		
		return Cf.list(result);
	}
	
	private static Tuple3<String, String, String> Lookup(Resource resource, Property prop) {
		return new Tuple3<String, String, String>(resource.getProperty(prop).getSubject().toString(),
				resource.getProperty(prop).getPredicate().toString(),resource.getProperty(prop).getObject().toString());
	}
	
	private static void DumpResourceProperties(Resource resource){
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
