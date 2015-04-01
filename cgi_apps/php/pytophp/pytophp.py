#!/usr/bin/python
import sys

class PYtoPHP(object) :
  types = [int,float,str,list,tuple,dict]
  def str_escape(self,s):
    return s.replace('\\','\\\\').replace('\'','\\\'')

  def convert(self,v):
    typp = type(v)
    if typp == int or typp == float:
      return str(v)
    elif typp == str:
      return "'" + self.str_escape(v) +"'"
    elif typp == list:
      return "array(" + ",".join(map(self.convert,v)) +")"
    elif typp == dict:
      return "array(" + ",".join([self.convert(key)+"=>"+self.convert(v[key]) for key in v]) + ")"
    elif typp == tuple:
      return self.convert(list(v))
    else: 
      raise Exception("Can't convert the type")
  
  def php_var(self,(o,v)):
    try:
      pvalue = self.convert(v)
    except Exception as e:
      return ""
    else:
      return "$" + o + " = " + pvalue +";\n"
  
  def php(self,alls):
    return "global " + ",".join(map(lambda (o,v):"$"+o,alls)) + ";\n" + "".join(map(self.php_var,alls))

pytophp = PYtoPHP()
if len(sys.argv) < 2:
  print "Enter a filename to import."
else:
  fromlist = []
  if len(sys.argv) > 2:
    fromlist = sys.argv[2:]
  filepath = sys.argv[1]
  if filepath[-3:] == ".py":
    filepath = filepath[:-3]
  path = '/'.join(filepath.split('/')[:-1])
  filename = filepath.split('/')[-1]
  sys.path.insert(0,path) 
  module = __import__(filename)
  if fromlist:
    object_names = fromlist
  else:
    object_names = filter(lambda o: False if o[0] == '_' else True,dir(module))
  alls = map(lambda o:(o,getattr(module,o)),object_names)
  print pytophp.php(alls)[:-1]
