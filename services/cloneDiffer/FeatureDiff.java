import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.Reader;
import java.util.Iterator;

import net.sf.json.*;

public class FeatureDiff {
	private static String help = "Usage: java -jar FeatureDiff.jar <original file> <clone file> <output file>";
	private static String diff(String original, String clone){
		JSONObject originalObj,cloneObj,diffObj;
		diffObj = new JSONObject();
		originalObj = JSONObject.fromString(original);
		cloneObj = JSONObject.fromString(clone);
		Iterator<String> originIterator = originalObj.keys();
		while(originIterator.hasNext()){
			String currentKey = originIterator.next();
			JSONArray originalArray = originalObj.optJSONArray(currentKey);
			JSONArray cloneArray = cloneObj.optJSONArray(currentKey);
			JSONArray outputArray = new JSONArray();
			if(originalArray != null && cloneArray != null){
				Object[] originalObjArray = originalArray.toArray();
				Object[] cloneObjArray = cloneArray.toArray();
				for(int i = 0; i < originalObjArray.length; i++){
					for(int j = 0; j < cloneObjArray.length;j++){
						if(originalObjArray[i].toString().equals(cloneObjArray[j].toString())){
							outputArray.put(i+1);
							break;
						}
					}
				}	
			}
			diffObj.put(currentKey, outputArray);			
		}
		return diffObj.toString(4);
	}
	
	private static String readWholeTextFile(File in){
		BufferedReader inReader = null;
		StringBuilder rel = new StringBuilder();
		try {			
			inReader = new BufferedReader(new FileReader(in));			
			char s[] = new char[100];
			int n;
			while((n = inReader.read(s)) != -1){
				rel.append(s, 0, n);
			}
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} finally{
			try {
				if(inReader != null)
					inReader.close();
			} catch (IOException e) {				
			}
			
		}
		return rel.toString();
		
	}
	public static void main(String args[]){
		if(args.length != 3){
			System.out.println("Error: Incorrect number of arguments.");
			System.out.println(help);
			return;
		}
		File origin = new File(args[0]);
		File clone = new File(args[1]);
		File output = new File(args[2]);
		String originString,cloneString;		
		BufferedWriter out = null;
		try {
			originString = readWholeTextFile(origin);
		    cloneString = readWholeTextFile(clone);
		    String diff = diff(originString, cloneString);
		    out = new BufferedWriter(new FileWriter(output));
		    out.write(diff);		    
		} catch (IOException e) {			
			e.printStackTrace();			
		}finally{
			try {
				if(out != null)
					out.close();
			} catch (IOException e) {				
			}
		}
				
	}
}
