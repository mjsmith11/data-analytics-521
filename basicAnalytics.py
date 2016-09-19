import utilities as u

def frequencies(data,field):
	result = {}
	for row in data:
		value = row[u.indexLookup(field)]
		if (result.has_key(value)):
			result[value] = result[value]+1
		else:
			result[value] = 1
	
	return result