The predicates will be executed by the predicate101 module of the worker. They will be referenced over the predicate constraint
in the 101language. The rule bellow would execute the dotNetImport/predicate.py with the argument: "System.Xml" :

 {
    predicate: "dotNETImport",
    args: ["System.Xml"],
    language: "CSharp",
    metadata: [
        {
            dependsOn: ".NET"
        }
    ]
}


If you want to add another predicate make sure that the file that shall be executed has the name predicate.py.
Further there should be a predicate description (predicate.json) that sums up the most important informations about the predicate.
It contains follow keywords:

    - name : The name of the predicate. That is a simple string
    - args : The number of arguments the predicate takes. The definition of that one is a bit more complex than the other.
             Follow types of values are valid
             null : That means that it doesn't matter how many arguments you give to the predicate. It can be in the range from 0 to infinity
             [x, y] : The minimal and maximal number the predicate expects. If we just have a minimal number the y value can be "null"
                      The value of x, however, shoud be a positive integer smaller than y.
                      Examples: [1, 1] : exact one argument
                                [1, 3] : Between 1 and three arguments
                                [1, null] : At least one argument
    - dependencies  : A list with all modules of the 101worker that should run before that predicate can execute successfully.
                      Make sure that that dependency is also a part of the module description of predicate101 or the execution will fail
    -  metadata    :  Dependencies to metadata keys. It is not implemented yet hence there are no such dependencies yet. The type would be a list of strings though


Example:
{

	"name" : "ClassifierChecker",
	"args" : [3,3],
	"dependencies" : ["extract101meta"],
	"metadata" : []

}