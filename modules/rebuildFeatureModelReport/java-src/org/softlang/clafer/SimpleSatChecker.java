package org.softlang.clafer;

import edu.mit.csail.sdg.alloy4.A4Reporter;
import edu.mit.csail.sdg.alloy4.Err;
import edu.mit.csail.sdg.alloy4compiler.ast.Command;
import edu.mit.csail.sdg.alloy4compiler.ast.Module;
import edu.mit.csail.sdg.alloy4compiler.parser.CompUtil;
import edu.mit.csail.sdg.alloy4compiler.translator.A4Options;
import edu.mit.csail.sdg.alloy4compiler.translator.A4Solution;
import edu.mit.csail.sdg.alloy4compiler.translator.TranslateAlloyToKodkod;

public class SimpleSatChecker {

	public static void main(String[] args) throws Err {
		Module world = CompUtil.parseEverything_fromFile(new A4Reporter(), null, args[0]);
		A4Options options = new A4Options();
		options.solver = A4Options.SatSolver.SAT4J;
		for (Command command: world.getAllCommands()) {
			A4Solution ans = TranslateAlloyToKodkod.execute_command(new A4Reporter(), world.getAllReachableSigs(),  command, options);
			System.out.println(ans.satisfiable() ? 1 : 0);
		}
	}

}
