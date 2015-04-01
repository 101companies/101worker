/*That test executes follow if-Statements in the extractor file
	if(tree.type == 'VariableDeclaration')
	if(tree.type == 'IfStatement') 
	if(tree.type == 'WhileStatement')
	if(tree.type == 'FunctionDeclaration') 
*/
var result = 0;
var i = 12;

while(i > 0){
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
	i--;
}

