package org.softlang.igraph;

import org.jgrapht.ext.VertexNameProvider;

public class NameProvider101 implements VertexNameProvider<Vertex> {

	@Override
	public String getVertexName(Vertex v) {
		//return MD5(v.getName());
		return v.getClass().getSimpleName() + v.getName().replace(" ", "_").replace("/", "_");
	}

	public String MD5(String md5) {
		try {
			java.security.MessageDigest md = java.security.MessageDigest.getInstance("MD5");
			byte[] array = md.digest(md5.getBytes());
			StringBuffer sb = new StringBuffer();
			for (int i = 0; i < array.length; ++i) {
				sb.append(Integer.toHexString((array[i] & 0xFF) | 0x100)
						.substring(1, 3));
			}
			return sb.toString();
		} catch (java.security.NoSuchAlgorithmException e) {
		}
		return null;
	}
}
