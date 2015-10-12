# -*- coding: utf-8 -*-

def handleUmlauts(txt):
  txt = txt.encode('utf-8').replace("ä", "\\\"{a}")
  txt = txt.encode('utf-8').replace("ö", "\\\"{o}")
  txt = txt.encode('utf-8').replace("è", "e")
  txt = txt.encode('utf-8').replace("ü", "\\\"{u}")
  return txt

def toTex(txt):
  txt = txt.replace('&','\&')
  txt = txt.replace('<nowiki>','')
  txt = txt.replace('</nowiki>','') 
  txt = txt.replace('$','\\textdollar{}')
  txt = txt.replace('->','$\rightarrow$')
  txt = txt.replace('=>','$\Rightarrow$')
  txt = txt.replace('<','$<$')
  txt = txt.replace('>','$>$')
  txt = txt.replace('%','\%')   
       
  txt = txt.replace("<references>", "")
  txt = txt.replace("<references/>", "")
  txt = txt.replace('^','\^')
  txt = txt.replace('#','\#')
  txt = txt.replace('_','\\_')

  return handleUmlauts(txt) 

def getTexCommandName(txt):
  txt = txt.encode('utf-8').replace(".", "dot")
  txt = txt.replace("-", "")
  txt = txt.replace("/", "")
  txt = txt.encode('utf-8').replace("ä", "ae")
  txt = txt.encode('utf-8').replace("ü", "ou")
  txt = txt.encode('utf-8').replace("ö", "oe")
  txt = txt.encode('utf-8').replace("è", "e")
  txt = txt.replace(":", "")
  res = txt.replace(' ', '')
  return res

