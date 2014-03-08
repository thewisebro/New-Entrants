import crypt
from optparse import OptionParser

if __name__=="__main__":
	parser = OptionParser()
	parser.add_option("-u", "--user", dest="new_user",
                  help="The username", metavar="FILE")
	parser.add_option("-p", "--passwd", dest="passwd",
                  help="Password", metavar="FILE")
	parser.add_option("-d", "--display", dest="display",
                  help="Display Text", metavar="FILE")

	(options, args) = parser.parse_args()
	line=options.new_user+":"+crypt.crypt(options.passwd,options.new_user[:2])+"::"+options.display
	print line
	

