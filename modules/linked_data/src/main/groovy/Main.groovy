import com.tinkerpop.blueprints.Direction
import com.tinkerpop.blueprints.impls.sail.SailGraph
import com.tinkerpop.blueprints.impls.sail.SailVertex
import com.tinkerpop.blueprints.impls.sail.impls.LinkedDataSailGraph
import com.tinkerpop.blueprints.oupls.sail.*
import com.tinkerpop.gremlin.groovy.Gremlin
import groovy.json.JsonBuilder
import groovy.json.JsonOutput
import groovy.json.JsonDelegate
import net.fortytwo.sesametools.reposail.RepositorySail
import org.openrdf.query.resultio.TupleQueryResultFormat
import org.openrdf.repository.Repository
import org.openrdf.repository.http.HTTPRepository
import org.openrdf.model.URI
import org.openrdf.model.impl.URIImpl

import static Repo101.Properties.*

class Repo101 {
    private static final String repoURI = 'http://triples.101companies.org/openrdf-sesame/repositories/wiki2/';
    static Repository repo;
    static SailGraph graph;

    public static class Properties {
        public static DEPENDS_ON = 'http://101companies.org/property/dependsOn'
        public static IDENTIFIES = 'http://101companies.org/property/identifies'
        public static LINKS_TO = 'http://101companies.org/property/linksTo'
        public static CITES = 'http://101companies.org/property/cites'
        public static USES = 'http://101companies.org/property/uses'
        public static IMPLEMENTS = 'http://101companies.org/property/implements'
        public static INSTANCE_OF = 'http://101companies.org/property/instanceOf'
        public static IS_A = 'http://101companies.org/property/isA'
        public static DEVELOPED_BY = 'http://101companies.org/property/developedBy'
        public static REVIEWED_BY = 'http://101companies.org/property/reviewedBy'
        public static RELATES_TO = 'http://101companies.org/property/relatesTo'
        public static MENTIONS = 'http://101companies.org/property/mentions'
        public static LABEL = 'http://www.w3.org/2000/01/rdf-schema#label'
        public static PAGE = 'http://semantic-mediawiki.org/swivt/1.0#page'
        public static TYPE = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type'

        private static createProperty(ns, name){
            if (ns == 'wiki'){
                return Repo101.graph.uri('wiki', 'Property-3A:' + name)
            }
            def prop =  Repo101.graph.uri(ns + ':' + name)
            return prop
        }
    }

    static {
        Gremlin.load()
        repo = new HTTPRepository(repoURI);
        repo.setPreferredTupleQueryResultFormat(TupleQueryResultFormat.JSON)

        repo.initialize();

        graph = new LinkedDataSailGraph(new SailGraph(new RepositorySail(repo)))
        graph.addDefaultNamespaces()
        graph.addNamespace('v101','http://101companies.org/properties/')
        graph.addNamespace('wiki', 'http://101companies.org/resource/')
        graph.addNamespace('swivt', 'http://semantic-mediawiki.org/swivt/1.0')
        graph.addNamespace('rdf', 'http://www.w3.org/1999/02/22-rdf-syntax-ns#')

    }

    public void statistics(){
        def edges =  graph.getEdges().toList()
        println "dependsOn:" + edges.findAll {it.label == Properties.DEPENDS_ON}.size()
        println "identifies:" + edges.findAll {it.label == Properties.IDENTIFIES}.size()
        println "linksTo:" + edges.findAll {it.label == Properties.LINKS_TO}.size()
        println "cites:" + edges.findAll {it.label == Properties.CITES}.size()
        println "uses:" +  edges.findAll {it.label == Properties.USES}.size()
        println "implements:" + edges.findAll {it.label == Properties.IMPLEMENTS}.size()
        println "instanceOf:" + edges.findAll {it.label == Properties.INSTANCE_OF}.size()
        println "isA:" + edges.findAll {it.label == Properties.IS_A}.size()
        println "developedBy:" + edges.findAll {it.label == Properties.DEVELOPED_BY}.size()
        println "reviewedBy:" + edges.findAll {it.label == Properties.REVIEWED_BY}.size()
        println "relatesTo:" + edges.findAll {it.label == Properties.RELATES_TO}.size()
        println "mentions:" + edges.findAll {it.label == Properties.MENTIONS}.size()
    }

    public examineConcepts(ns) {

        def nsLanguage = getResource(ns)
        println(nsLanguage)
        //println nsLanguage.inE('http://101companies.org/property/instanceOf').outV.toList()
        def concept = getResource("http://101companies.org/resources/namespaces/Concept")
        def concepts = nsLanguage.inE('http://101companies.org/property/instanceOf').outV. //languages
                   inE('http://101companies.org/property/uses').outV.       // contributions
                   outE('http://101companies.org/property/mentions').inV.toList().findAll{
                    it.outE('http://101companies.org/property/instanceOf').inV.filter{it == concept}.toList().size() > 0
                   }
        //println "# concepts: " + concepts.size()
        println "concepts: " + concepts
        //println "# unique concepts: " + concepts.unique().size()
        //println "unique concepts: " + concepts.unique()
        return concepts 
      }

    //'http://101companies.org/resource/Namespace-3ANamespace'
    public SailVertex getResource(url){
        return graph.v(url)
    }
}
