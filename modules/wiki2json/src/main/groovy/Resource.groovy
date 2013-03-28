import groovy.json.JsonBuilder
import groovy.json.JsonOutput
import groovy.json.JsonSlurper
import groovy.transform.TypeChecked

import static Repo101.Properties.*

class Resource {

    def Resource(resource){
        this.resource = resource;
    }

    private resource

    /*
              println('properties: ')
          // all properties of the resource
          r.outE.each{
            println(it.getId())

           // TODO: extract metadata, by searching for properties http://101companies.org/property/XXX
          }
          println()
          //def rOut = r.outE.toList()
          //def rIn = r.inE.toList()
     */


    private handleObject(props, name, object){
        if (props.containsKey(name))
            props[name] += object.getLocalName()
        else
            props[name] = [object.getLocalName()]

        return props
    }

    private handlePage(props, name, object)  {
        if (props.containsKey(name))
            props[name] += handlePageLabel(object.getLocalName(), "-3A")
        else
            props[name] = [handlePageLabel(object.getLocalName(), "-3A")]

        return props
    }

    private handleUrlObject(props, name, object){
        if (props.containsKey(name))
            props[name] += object.toString()
        else
            props[name] = [object.toString()]

        return props
    }

    private handlePageLabel(label, separator = ":"){
       def page =  label.split(separator)
       def props = [:]
       if (page.size() == 1)   {
           props["p"] = null
           props["n"] = page[0].replaceAll('-C3-A', 'ä')
       }
      else{
           props["p"] = page[0]
           props["n"] = page[1].replaceAll('-C3-A', 'ä')
       }
     return props
    }

    def getJSON(url, attemps = 0){
        try{
            def links = null;
            URLConnection connection = new URL(url).openConnection();
            int responseCode = connection.getResponseCode();
            if (responseCode == HttpURLConnection.HTTP_OK) {
                InputStream response = connection.getInputStream();
                String txt = new Scanner(response, "UTF-8").useDelimiter("\\A").next();
                links = new JsonSlurper().parseText(txt)
                if (attemps > 0){
                    println('successfully got data from ' + url)
                }
            }
            else if (responseCode == HttpURLConnection.HTTP_SERVER_ERROR){
                println(' HTTP 500 server error. Retrying...' + url)
                attemps++
                if (attemps < 3){
                    getJSON(url, attemps)
                }
            }
            else {
                return null;
            }
            return links
        }
        catch(java.io.FileNotFoundException e){
            print('not found: ')
            println(e)
        }
        catch (java.io.IOException e) {
            println(e)
        }
    }

    public getProperties(){
        def props = [:]
        resource.outE.each{
            //println(it.getId())
            def edge = it.getRawEdge()
            def predicate = edge.getPredicate().toString()
            switch (predicate){
                case LABEL :
                    def obj = edge.getObject()
                    props['page'] = handlePageLabel(obj.label)
                    try {
                        def url = 'http://beta.101companies.org/api/pages/' + java.net.URLEncoder.encode(obj.label.replaceAll(' ', '_')) + '/internal_links'
                        props['internal_links'] = getJSON(url)
                    }
                    catch(e){
                      println('weird exception')
                      println(e)
                    }

                    try {
                        //Thread.currentThread().sleep(2 * 1000)
                        def url = 'http://beta.101companies.org/api/pages/' + java.net.URLEncoder.encode(obj.label.replaceAll(' ', '_')) + '/sections'
                        def sections = getJSON(url)
                        if ((sections != null) && (sections.size() > 0) && (sections[0].title == "Headline")){
                            props['headline'] = sections[0].content.replaceAll("== Headline ==", "").replaceAll("==Headline==","")
                        }
                    }
                    catch(e){
                        println('weird exception')
                        println(e)
                    }
                    break
                /*case PAGE :
                    props['page'] = edge.getObject().getLocalName()
                    break     */
                case REVIEWED_BY :
                    props = handlePage(props, 'reviewedBy', edge.getObject())
                    break
                case DEVELOPED_BY :
                    props = handlePage(props, 'developedBy', edge.getObject())
                    break
                case IS_A :
                    props = handlePage(props, 'isA', edge.getObject())
                    break
                case INSTANCE_OF :
                    props = handlePage(props, 'instanceOf', edge.getObject())
                    break
                case IMPLEMENTS :
                    props = handlePage(props, 'implements', edge.getObject())
                    break
                case USES :
                    props = handlePage(props, 'uses', edge.getObject())
                    break
                case CITES :
                    props = handleUrlObject(props, 'cites', edge.getObject())
                    break
                case LINKS_TO :
                    props = handleUrlObject(props, 'linksTo', edge.getObject())
                    break
                case IDENTIFIES :
                    props = handleUrlObject(props, 'identifies', edge.getObject())
                    break
                case DEPENDS_ON :
                    props = handlePage(props, 'dependsOn', edge.getObject())
                    break
                case RELATES_TO:
                    props = handlePage(props, 'relatesTo', edge.getObject())
                    break
                case TYPE:
                    props['type'] = edge.getObject().getLocalName()
                    break
            }
        }
        return props
    }

    public JsonBuilder toJson(){
        def json = new JsonBuilder()
        def props = getProperties();
        json.page
        {
            properties(props)
            content("")
        }

        return json
    }
}
