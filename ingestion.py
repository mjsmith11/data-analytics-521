#Matthew Smith
#CS521 Project 2
# Data Ingestion and Preprocesisng

import csv
import utilities as u

data = []


# accepts a file path as a string and parses it as csv
# each element of the list data will be a list of length 75 with entries ordered according to the index lookup in utilities.py
# returns an integer indicating the number of records removed due to improper formatting
def readAndPreprocess(file):
    skippedRecords = 0
    f = open(file)
    csv_f = csv.reader(f)
    for row in csv_f:
        # length other than 75 indicates an error in the data object
        if (len(row) == 75):
            row[0] = u.checkNotBlank(row[0])  # unique_transaction_id
            row[1] = u.checkDollars(row[1])  # dollarsobligated
            row[2] = u.checkDollars(row[2])  # baseandexercisedoptionsvalue
            row[3] = u.checkDollars(row[3])  # baseandalloptionsvalue
            row[4] = u.checkNotBlank(row[4])  # contractingofficeagencyid
            row[5] = u.checkNotBlank(row[5])  # contractingofficeid
            row[6] = u.checkNotBlank(row[6])  # fundingrequestingagencyid
            row[7] = u.checkNotBlank(row[7])  # fundingrequestingofficeid
            row[8] = u.checkNotBlank(row[8])  # fundedbyforeignentity
            row[9] = u.checkDate(row[9])  # signeddate
            row[10] = u.checkDate(row[10])  # effectivedate
            row[11] = u.checkDate(row[11])  # currentcompletiondate
            row[12] = u.checkNotBlank(row[12])  # typeofcontractpricing
            row[13] = u.checkNotBlank(row[13])  # priceevaluationpercentdifference
            row[14] = u.checkNotBlank(row[14])  # subcontractplan
            row[15] = u.checkYesNo(row[15])  # multiyearcontract
            row[16] = u.checkNotBlank(row[16])  # majorprogramcode
            row[17] = u.checkNotBlank(row[17])  # contractfinancing
            row[18] = u.checkNotBlank(row[18])  # descriptionofcontractrequirement
            row[19] = u.checkNotBlank(row[19])  # nationalinterestactioncode
            row[20] = u.checkNotBlank(row[20])  # vendorname
            row[21] = u.checkNotBlank(row[21])  # vendoralternatename
            row[22] = u.checkNotBlank(row[22])  # vendorlegalorganizationname
            row[23] = u.checkNotBlank(row[23])  # vendordoingasbusinessname
            row[24] = u.checkNotBlank(row[24])  # divisionname
            row[25] = u.checkNotBlank(row[25])  # divisionnumberorofficecode
            row[26] = u.checkNotBlank(row[26])  # streetaddress
            row[27] = u.checkNotBlank(row[27])  # streetaddress2
            row[28] = u.checkNotBlank(row[28])  # streetaddress3
            row[29] = u.checkNotBlank(row[29])  # city
            row[30] = u.checkNotBlank(row[30])  # state
            row[31] = u.checkInt(row[31])  # zipcode
            row[32] = u.checkNotBlank(row[32])  # vendorcountrycode
            row[33] = u.checkNotBlank(row[33])  # vendor_state_code
            row[34] = u.checkInt(row[34])  # vendor_cd
            row[35] = u.checkInt(row[35])  # congressionaldistrict
            row[36] = u.checkInt(row[36])  # phoneno
            row[37] = u.checkNotBlank(row[37])  # statecode
            row[38] = u.checkNotBlank(row[38])  # placeofperformancecity
            row[39] = u.checkNotBlank(row[39])  # pop_state_code
            row[40] = u.checkNotBlank(row[40])  # placeofperformancecountrycode
            row[41] = u.checkInt(row[41])  # placeofperformancezipcode
            row[42] = u.checkNotBlank(row[42])  # pop_cd
            row[43] = u.checkNotBlank(row[43])  # placeofperformancecongressionaldistrict
            row[44] = u.checkNotBlank(row[44])  # informationtechnologycommercialitemcategory
            row[45] = u.checkNotBlank(row[45])  # useofepadesignatedproducts
            row[46] = u.checkNotBlank(row[46])  # seatransportation
            row[47] = u.checkNotBlank(row[47])  # countryoforigin
            row[48] = u.checkNotBlank(row[48])  # placeofmanufacture
            row[49] = u.checkNotBlank(row[49])  # agencyid
            row[50] = u.checkInt(row[50])  # numberofoffersreceived
            row[51] = u.checkNotBlank(row[51])  # organizationaltype
            row[52] = u.checkInt(row[52])  # numberofemployees
            row[53] = u.checkInt(row[53])  # annualRevenue
            row[54] = u.checkTF(row[54])  # hbcuflag
            row[55] = u.checkTF(row[55])  # educationalinstitutionflag
            row[56] = u.checkTF(row[56])  # womanownedflag
            row[57] = u.checkTF(row[57])  # veteranownedflag
            row[58] = u.checkTF(row[58])  # localgovernmentflag
            row[59] = u.checkTF(row[59])  # minorityinstitutionflag
            row[60] = u.checkTF(row[60])  # aiobflag
            row[61] = u.checkTF(row[61])  # stategovernmentflag
            row[62] = u.checkTF(row[62])  # federalgovernmentflag
            row[63] = u.checkTF(row[63])  # minorityownedbusinessflag
            row[64] = u.checkTF(row[64])  # apaobflag
            row[65] = u.checkTF(row[65])  # tribalgovernmentflag
            row[66] = u.checkTF(row[66])  # baobflag
            row[67] = u.checkTF(row[67])  # naobflag
            row[68] = u.checkTF(row[68])  # saaobflag
            row[69] = u.checkTF(row[69])  # nonprofitorganizationflag
            row[70] = u.checkTF(row[70])  # isfoundation
            row[71] = u.checkTF(row[71])  # haobflag
            row[72] = u.checkTF(row[72])  # isprivateuniversityorcollege
            row[73] = u.checkTF(row[73])  # isstatecontrolledinstitutionofhigherlearning
            row[74] = u.checkDate(row[74])  # last_modified_date

            data.append(row)

        else:
            skippedRecords += 1
    del data[0]  # this is the headings
    return skippedRecords
