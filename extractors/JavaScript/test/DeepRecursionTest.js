/*That test executes follow if-Statements in the extractor file
	if(tree.type == 'VariableDeclaration')
	if(tree.type == 'IfStatement') 
	if(tree.type == 'FunctionDeclaration') 
	
	
	Furthermore it aims to get deeper into the parse-tree structure
*/

var func = function(arg1, arg12) {
	var xyz = 0;
	var func2 = function(x) {
	    var newVariable2 = 12;
	    var newFuncLevelTwo = function(y) {
	        var newVariable3 = 12;
	        var funLevelThree = function() {
	            var result = 42;
	            return result;
	        };
	        var result3 =  newFuncLevelThree + newVariable3;
	        return result3;
	    }
	    var result2 = newFuncLevelTwo(newVariable2) + x;
	    return result2;
	}
    var result =  fucn2(arg1) + xyz + arg12;
    return result;
}


var var1 = 40;
var var2 = 2;
var result = func(var1, var2);
