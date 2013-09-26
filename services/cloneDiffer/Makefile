# define the path to libraries
LIBRARY = ./lib

CLASSPATH = -cp $(LIBRARY)/commons-beanutils-1.8.0.jar -cp $(LIBRARY)/commons-collections-3.2.1.jar -cp $(LIBRARY)/commons-lang-2.5.jar -cp $(LIBRARY)/commons-logging-1.1.1.jar -cp $(LIBRARY)/ezmorph-1.0.6.jar -cp $(LIBRARY)/json-lib-1.1-jdk15.jar

default:FeatureDiff.jar
	@echo  FeatureDiff.jar has been created.

FeatureDiff.jar: FeatureDiff.java JarMetaInfo.mf
	javac $(CLASSPATH) FeatureDiff.java
	jar cfm FeatureDiff.jar JarMetaInfo.mf FeatureDiff.class
	$(RM) FeatureDiff.class	

clean: 	
	$(RM) FeatureDiff.jar *~
	
	


