def soundxfunction(name,padspaces="false",len=4):
	"""converts the name into corresponding soundx.The result can have a maximum of 4 characters"""
	# digits holds the soundex values for the alphabet respect of their place
	#	group 0:aehiouwy
	#	group 1:bfpv
	#	group 2:cgjkqsxz
	#	group 3:dt
	#	group 4:l
	#	group 5:mn
	#	group 6:r
	digits = '01230120022455012623010202'
	#         abcdefghijklmnopqrstuvwxyz	
	sndx = ''
	fc = ''
	# translate alpha chars in name to soundex digits
	for c in name.upper():
		if c.isalpha():
			if not fc:
				fc = c   # remember first letter
			d = digits[ord(c)-ord('A')]
			# duplicate consecutive soundex digits are skipped
			if not sndx or (d != sndx[-1]):
				sndx += d
	# replace first digit with first alpha character
	sndx = fc + sndx[1:]
	# remove all 0s from the soundex code
	sndx = sndx.replace('0','')
	# return soundex code padded to len characters
	if padspaces=="true":
		return (sndx + (len * '0'))[:len]
	return sndx[0:4]
