/*That test executes follow if-Statements in the extractor file
	if(tree.type == 'VariableDeclaration')
	if(tree.type == 'IfStatement') 
	if(tree.type == 'FunctionDeclaration') 
*/

var func = function(arg1, arg12) {
	var result = 0;
	if(arg1 < arg2) {
		result =arg2 - arg1;
	}
	else {
		result = arg1 - arg2;
	}
	return result;
};


var var1 = 40;
var var2 = 2;
var result = func(var1, var2);
