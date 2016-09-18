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
# This is designed to reduce memory usage. We don't need to use a dictionary and key-value pairs for every single data object.
# This way we just store the key and field number relationship once and we can store the data objects as lists.
def indexLookup(field):
	if (field in dd.keys()):
		return dd[field]
	else:
		return "invalid"
