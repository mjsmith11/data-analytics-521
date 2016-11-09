#Matthew Smith
#CS521 Project 2
#Utility functions

from datetime import date

dd = {
	'unique_transaction_id':0,
	'dollarsobligated':1,
	'baseandexercisedoptionsvalue':2,
	'baseandalloptionsvalue':3,
	'contractingofficeagencyid':4,
	'contractingofficeid':5,
	'fundingrequestingagencyid':6,
	'fundingrequestingofficeid':7,
	'fundedbyforeignentity':8,
	'signeddate':9,
	'effectivedate':10,
	'currentcompletiondate':11,
	'typeofcontractpricing':12,
	'priceevaluationpercentdifference':13,
	'subcontractplan':14,
	'multiyearcontract':15,
	'majorprogramcode':16,
	'contractfinancing':17,
	'descriptionofcontractrequirement':18,
	'nationalinterestactioncode':19,
	'vendorname':20,
	'vendoralternatename':21,
	'vendorlegalorganizationname':22,
	'vendordoingasbusinessname':23,
	'divisionname':24,
	'divisionnumberorofficecode':25,
	'streetaddress':26,
	'streetaddress2':27,
	'streetaddress3':28,
	'city':29,
	'state':30,
	'zipcode':31,
	'vendorcountrycode':32,
	'vendor_state_code':33,
	'vendor_cd':34,
	'congressionaldistrict':35,
	'phoneno':36,
	'statecode':37,
	'placeofperformacecity':38,
	'pop_state_code':39,
	'placeofperformancecountrycode':40,
	'placeofperformancezipcode':41,
	'pop_cd':42,
	'placeofperformancecongressionaldistrict':43,
	'informationtechnologycommercialitemcategory':44,
	'useofepadesignatedproducts':45,
	'seatransportation':46,
	'countryoforigin':47,
	'placeofmanufacture':48,
	'agencyid':49,
	'numberofoffersreceived':50,
	'organizationaltype':51,
	'numberofemployees':52,
	'annualrevenue':53,
	'hbcuflag':54,
	'educationalinstitutionflag':55,
	'womenownedflag':56,
	'veteranownedflag':57,
	'localgovernmentflag':58,
	'minorityinstitutionflag':59,
	'aiobflag':60,
	'stategovernmentflag':61,
	'federalgovernmentflag':62,
	'minorityownedbusinessflag':63,
	'apaobflag':64,
	'tribalgovernmentflag':65,
	'baobflag':66,
	'naobflag':67,
	'saaobflag':68,
	'nonprofitorganizationflag':69,
	'isfoundation':70,
	'haobflag':71,
	'isprivateuniversityorcollege':72,
	'isstatecontrolledinstutionofhigherlearning':73,
	'last_modified_date':74
	
	
}
# This is designed to reduce memory usage. We don't need to store the key-value relationship for every single data object.
# This way we just store the key and field number relationship once and we can store the data objects as lists.
def indexLookup(field):
	if (field in dd.keys()):
		return dd[field]
	else:
		return "invalid"

# returns an empty string if input is an empty string or contains only spaces
# otherwise input is returned		
def checkNotBlank(input):
	if input == "":
		return input
	else:
		for ch in input:
			if ch != " ":
				return input
		return ""

# returns input coverted to a float and rounded to two decimal places
# returns "" if the input cannot be coverted to float
def checkDollars(input):
	try:
		input = float(input)
		return round(input,2)
	except:
		return ""

# returns a date object if the imput is a valid date in the form m(m)/d(d)/yyyy
# returns "" otherwise
def checkDate(input):
	parts = input.split("/")
	try:
		d = date(int(parts[2]),int(parts[0]),int(parts[1]))
		return d
	except:
		return ""

#returns Y if the input is Y: YES
#returns N if the input is N: NO
#returns "" otherwise
def checkYesNo(input):
	if(input == "Y: YES"):
		input = "Y"
	elif(input == "N: NO"):
		input = "N"
	else:
		input = ""
	
	return input
	
#returns an integer representation of the input if it can be converted and is between min and max inclusive
#returns "" otherwise
def checkInt(input,min,max):
	try:
		input = int(input)
		if(input<min):
			return ""
		elif(input>max):
			return ""
		else:
			return input
	except:
		return ""
		
#returns input if input is TRUE or FALSE
#returns "" otherwise
def checkTF(input):
	if(input == "true"):
		return input
	elif(input == "false"):
		return input
	else:
		return ""

#returns a number in string form which corresponds to the month abbreviation passed as a parameter.
def getMonthNum(strinp):
    d = {
        "Jan": "01",
        "Feb": "02",
        "Mar": "03",
        "Apr": "04",
        "May": "05",
        "Jun": "06",
        "Jul": "07",
        "Aug": "08",
        "Sep": "09",
        "Oct": "10",
        "Nov": "11",
        "Dec": "12"
    }
    return d[strinp]

#returns the string representation of an integer day of the week where 0 represents Monday and 6 represents Sunday
def getDayStr(dayInt):
    d = {
        0:"Monday",
        1:"Tuesday",
        2:"Wednesday",
        3:"Thursday",
        4:"Friday",
        5:"Saturday",
        6:"Sunday"
    }
    return d[dayInt]

#returns a string representing the day of the week for the input. Ex input: 09/Nov/2013
def getDayOfWeek(dateinput):
    splits = dateinput.split('/')
    myday = int(splits[0])
    mymonth = int(getMonthNum(splits[1]))
    myyear = int(splits[2])
    return getDayStr(date(myyear, mymonth, myday).weekday())