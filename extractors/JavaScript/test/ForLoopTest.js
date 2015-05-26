/*That test executes follow if-Statements in the extractor file
	if(tree.type == 'VariableDeclaration')
	if(tree.type == 'IfStatement') 
	if(tree.type == 'ForStatement')
	if(tree.type == 'FunctionDeclaration') 
*/
var result = 0;


for(var i = 0; i < 12; i++) {
	var temp = 0;
	var doIt = function(x) {
		var test = x + 1;
		if(test == 42) {
			return 0;
		}
		return test;
	};
	temp = doIt(i);
	result += temp;
}

