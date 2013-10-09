

w3c = """<?xml version="1.0"?>
<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
  xmlns:dc="http://purl.org/dc/elements/1.1/">
  <rdf:Description rdf:about="http://www.w3.org/">
    <dc:title>World Wide Web Consortium</dc:title> 
  </rdf:Description>
</rdf:RDF>"""

w3cRemoved = '''<?xml version="1.0" encoding="UTF-8"?>
<rdf:RDF
	xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">

</rdf:RDF>'''

w3cResult = '''<?xml version="1.0" encoding="UTF-8"?>
<rdf:RDF
	xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
	xmlns:dc="http://purl.org/dc/elements/1.1/">

<rdf:Description rdf:about="http://www.w3.org/">
	<dc:title>World Wide Web Consortium</dc:title>
</rdf:Description>

</rdf:RDF>'''

# Using Shelley Powers examples from _Practical_RDF_.  Should be
# pretty stable.

postURL = "http://burningbird.net/articles/monsters1.rdf"

serqlSQuery = """
	select date
		from   {Resource} rdf:type {pstcn:Movement};
			pstcn:movementType {"Add"};
			dc:date {date}
		using namespace 
			pstcn = <http://burningbird.net/postcon/elements/1.0/>,
			dc = <http://purl.org/dc/elements/1.1/>
"""

serqlCQuery = """
	construct 
		{Resource} dc:date {date}
	from   
		{Resource} rdf:type {pstcn:Movement};
			pstcn:movementType {"Add"};
			dc:date {date}
	using namespace 
		pstcn = <http://burningbird.net/postcon/elements/1.0/>,
		dc = <http://purl.org/dc/elements/1.1/>
"""

rdqlQuery = """SELECT ?date
WHERE
(?resource, <rdf:type>, <pstcn:Movement>),
(?resource, <pstcn:movementType>,?value),
(?resource, <dc:date>, ?date)
AND (?value eq "Add")
USING pstcn FOR <http://burningbird.net/postcon/elements/1.0/>,
      rdf for <http://www.w3.org/1999/02/22-rdf-syntax-ns#>,
      dc for <http://purl.org/dc/elements/1.1/>"""

rdqlQueryResult = {'header':[u'date'], 'tuples': [[{'type':u'literal','value': '1998-01-01T00:00:00-05:00'}]]}


rdqlQueryRDF = """<?xml version='1.0' encoding='UTF-8'?>
<tableQueryResult>
	<header>
		<columnName>date</columnName>
	</header>
	<tuple>
		<literal>1998-01-01T00:00:00-05:00</literal>
	</tuple>
</tableQueryResult>"""



serqlCQueryRDF = """<?xml version="1.0" encoding="UTF-8"?>
<rdf:RDF
        xmlns:dcterms="http://purl.org/dc/terms/"
        xmlns:pstcn="http://burningbird.net/postcon/elements/1.0/"
        xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
        xmlns:dc="http://purl.org/dc/elements/1.1/">

<rdf:Description rdf:about="http://www.yasd.com/dynaearth/monsters1.htm">
        <dc:date>1998-01-01T00:00:00-05:00</dc:date>
</rdf:Description>

</rdf:RDF>"""

postcon = """<?xml version="1.0" encoding="UTF-8"?>
<rdf:RDF
  xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
  xmlns:pstcn="http://burningbird.net/postcon/elements/1.0/"
  xmlns:dcterms="http://purl.org/dc/terms/"
  xmlns:dc="http://purl.org/dc/elements/1.1/"
  xml:base="http://burningbird.net/articles/">

  <pstcn:Resource rdf:about="monsters1.htm">

<!-- Resource Biographical Information -->
     <pstcn:bio rdf:parseType="Resource">
        <dc:title>Tale of Two Monsters: Legends</dc:title>
     	  <dcterms:abstract>
            When I think of "monsters" I think of the creatures of 
            legends and tales, from the books and movies, and 
            I think of the creatures that have entertained me for years.
     	  </dcterms:abstract>
        <dc:description>
            Part 1 of four-part series on cryptozoology, legends, 
            Nessie the Loch Ness Monster and the giant squid.
        </dc:description>
     	  <dc:created>1999-08-01T00:00:00-06:00</dc:created>
     	  <dc:creator>Shelley Powers</dc:creator>
     	  <dc:publisher>Burningbird Network</dc:publisher>
      </pstcn:bio>

<!-- Resource's relevancy at time RDF/XML document was built -->
      <pstcn:relevancy rdf:parseType="Resource">
     	   <pstcn:currentStatus>Active</pstcn:currentStatus>
     	   <dcterms:valid>2003-12-01T00:00:00-06:00</dcterms:valid>
     	   <dc:subject>legends</dc:subject>
     	   <dc:subject>giant squid</dc:subject>
     	   <dc:subject>loch ness monster</dc:subject>
     	   <dc:subject>Architeuthis Dux</dc:subject>
     	   <dc:subject>Nessie</dc:subject>
	   <dcterms:isReferencedBy>http://www.pibburns.com/cryptozo.htm</dcterms:isReferencedBy>
	   <dcterms:references>http://www.nrcc.utmb.edu/</dcterms:references>
      </pstcn:relevancy>

<!-- Presentation/consumption information about resource -->
      <pstcn:presentation rdf:parseType="Resource">
         <dc:format>text/html</dc:format>
         <dcterms:conformsTo>XHTML 1.0 Strict</dcterms:conformsTo>
         <dcterms:conformsTo>CSS Validation</dcterms:conformsTo>
         <dcterms:requires>HTML User agent</dcterms:requires>
	   <pstcn:requires rdf:parseType="Resource">
            <pstcn:type>stylesheet</pstcn:type>
            <rdf:value>http://burningbird.net/de.css</rdf:value>
         </pstcn:requires>
         <pstcn:requires rdf:parseType="Resource">
            <pstcn:type>logo</pstcn:type>
            <rdf:value>http://burningbird.net/mm/dynamicearth.jpg</rdf:value>
         </pstcn:requires>
      </pstcn:presentation>

<!-- History of events of resource -->
     <pstcn:history>
       <rdf:Seq>
        <rdf:_1 rdf:resource="http://www.yasd.com/dynaearth/monsters1.htm" />
        <rdf:_2 rdf:resource="http://www.dynamicearth.com/articles/monsters1.htm" />
        <rdf:_3 rdf:resource="http://burningbird.net/articles/monsters1.htm" />
      </rdf:Seq>    
     </pstcn:history>

<!-- Resource internal to PostCon that are related to resource -->
     <pstcn:related rdf:resource="monsters2.htm" />
     <pstcn:related rdf:resource="monsters3.htm" />
     <pstcn:related rdf:resource="monsters4.htm" />
  </pstcn:Resource>

<!-- Related resources -->
  <pstcn:Resource rdf:about="monsters2.htm">
     <dc:title>Cryptozooloy</dc:title>
     <pstcn:reason>First in the Tale of Two Monsters series.</pstcn:reason>
  </pstcn:Resource>
  <pstcn:Resource rdf:about="monsters3.htm">
     <dc:title>A Tale of Two Monsters: Architeuthis Dux (Giant Squid)</dc:title>
     <pstcn:reason>Second in the Tale of Two Monsters series.</pstcn:reason>
  </pstcn:Resource>
  <pstcn:Resource rdf:about="monsters4.htm">
     <dc:title>Nessie, the Loch Ness Monster </dc:title>
     <pstcn:reason>Fourth in the Tale of Two Monsters series.</pstcn:reason>
  </pstcn:Resource>

<!-- Resource events -->
  <pstcn:Movement rdf:about="http://www.yasd.com/dynaearth/monsters1.htm">
      <pstcn:movementType>Add</pstcn:movementType>
      <pstcn:reason>New Article</pstcn:reason>
      <dc:date>1998-01-01T00:00:00-05:00</dc:date>
  </pstcn:Movement>
  <pstcn:Movement rdf:about="http://www.dynamicearth.com/articles/monsters1.htm">
      <pstcn:movementType>Move</pstcn:movementType>
      <pstcn:reason>Moved to separate dynamicearth.com domain</pstcn:reason>
      <dc:date>1999-10-31:T00:00:00-05:00</dc:date>
  </pstcn:Movement>
  <pstcn:Movement rdf:about="http:/burningbird.net/articles/monsters1.htm">
     <pstcn:movementType>Move</pstcn:movementType>
     <pstcn:reason>Collapsed into Burningbird</pstcn:reason>
     <dc:date>2002-11-01</dc:date> 
  </pstcn:Movement>

</rdf:RDF>"""
