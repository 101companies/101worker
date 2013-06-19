import groovy.json.JsonBuilder

class Run{
    void run(){
        def m = new Repo101()
        def fpConcepts = m.examineConcepts('http://101companies.org/resources/concepts/Functional_programming_language')
        
        def uniqueFpConcepts = fpConcepts.unique()
        def ooConcepts = m.examineConcepts('http://101companies.org/resources/concepts/OO_programming_language')
        
        def sortedOOConcepts = ooConcepts.countBy{it}.sort {a, b -> b.value <=> a.value}
        def sortedFpConcepts = fpConcepts.countBy{it}.sort {a, b -> b.value <=> a.value}

        println "OO Programming Language"
        def table = ""
        sortedOOConcepts.each{ k, v -> def r = "<tr><td>${k.getRawVertex().toString()}</td><td>${v}</td><td>${!sortedFpConcepts.containsKey(k)}</td></tr>"; println r; table += r }
        new File("oo.html").withWriter {it << toHtml(table) }

        println "FP Programming Language"
        sortedFpConcepts.each{ k, v -> def r = "<tr><td>${k.getRawVertex().toString()}</td><td>${v}</td><td>${!sortedOOConcepts.containsKey(k)}</td></tr>"; println r; table += r  }
        new File("fp.html").withWriter {it << toHtml(table) }

        //def uniqueOOConcepts = ooConcepts.unique()
        
        //def overlappingConcepts = fpConcepts.intersect(ooConcepts)
        //println "overlapping concepts: "
        //println overlappingConcepts
        //println "# overlapping concepts: " + overlappingConcepts.size()
  
        //m.statistics()
    }

    def toHtml(table){
        def html = "<html><head></head><body><table style=\"border:1px solid black;border-collapse:collapse;\"><tr><th>Concept</th><th>#Occs</th><th>Unique</th></tr>${table}</table></body></html>"
        return html 
    }
}



