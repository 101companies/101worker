import groovy.json.JsonBuilder
import groovy.json.JsonOutput
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

    private handleUrlObject(props, name, object){
        if (props.containsKey(name))
            props[name] += object.toString()
        else
            props[name] = [object.toString()]

        return props
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
                    props['page'] = obj.label
                    break
                /*case PAGE :
                    props['page'] = edge.getObject().getLocalName()
                    break     */
                case REVIEWED_BY :
                    props = handleObject(props, 'reviewedBy', edge.getObject())
                    break
                case DEVELOPED_BY :
                    props = handleObject(props, 'developedBy', edge.getObject())
                    break
                case IS_A :
                    props = handleObject(props, 'isA', edge.getObject())
                    break
                case INSTANCE_OF :
                    props = handleObject(props, 'instanceOf', edge.getObject())
                    break
                case IMPLEMENTS :
                    props = handleObject(props, 'implements', edge.getObject())
                    break
                case USES :
                    props = handleObject(props, 'uses', edge.getObject())
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
                    props = handleObject(props, 'dependsOn', edge.getObject())
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
