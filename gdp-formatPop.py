# script to break up and reformat the population data

import csv
import time

ORIG_DATA = "data/UNdata_gdp.csv"


# break the original file into other, reformated files
# we ignore midPeriod, and ID values in the reformatted files
with open(ORIG_DATA, "r") as origdata:
    baseFile = "data/formatted-gdp.csv"  # [[VARIANT]] will be replaced
    origReader = csv.reader(origdata)
    header = next(origReader)
    #print(header)

    # Group is Male, Female, or Total
    newHeader = ["Location", "Variant"]
    # create years
    for y in range(1970, 2018):  # data has year range 1950-2100
        newHeader.append(y)
    #print(newHeader)

    # read first line and set initial values for tracking variables
    firstLine = next(origReader)
    print(firstLine)
    # tracking variables
    currLoc = firstLine[0]
    currVar = firstLine[2]
#    var = firstLine[3].title().replace(" ", "")  # make "Hello world"  to "HelloWorld"
#    print("New variant: %s" % (var))
    #currFileName = baseFile.replace("[[VARIANT]]", var)
    # print(currFileName)

    # write new header
    with open(baseFile, "w", newline="") as newFile:
        newWriter = csv.writer(newFile)
        newWriter.writerow(newHeader)

    # data in orig is a column from 1970-2018, we make it part of the row
    # data of population values per year
    # each of these is for one country/location
    gdpData = [firstLine[3]]
#    femaleData = [firstLine[7]]
#    totalData = [firstLine[8]]
#
    # read in all the other lines
    for line in origReader:
        #print(line)

        # set tracking vars
        lineLoc = line[0]
#        lineVar = line[3]
#
#        if lineVar != currVar:  # new variant, want to make new file
#            # the way the orig data is done, if the variant changes, so does the location
#            # create new file name
#            var = line[3].title().replace(" ", "")  # make "Hello world"  to "HelloWorld"
#            currFileName = baseFile.replace("[[VARIANT]]", var)
#
#            # write new header to new file
#            with open(currFileName, "w", newline="") as newFile:
#                newWriter = csv.writer(newFile)
#                newWriter.writerow(newHeader)
#
#            # reset tracking variables
#            currLoc = line[1]
#            currVar = line[3]
#
#            # clear the data lists (this line will be added below)
#            maleData.clear()
#            femaleData.clear()
#            totalData.clear()
#
#            print("New variant: %s" % (var))
#
        if lineLoc != currLoc:  # new location
            rows = []
            # remember new header: ["Location", "Variant", "Group", 1959, ..., 2100]
            # male data
            print(gdpData)
            gdpData.reverse()
            gdpRow = [currLoc, currVar] + gdpData
            rows.append(gdpRow)
#            # female data
#            femaleRow = [currLoc, currVar, "Female"] + femaleData
#            rows.append(femaleRow)
#            # total data
#            totalRow = [currLoc, currVar, "Total"] + totalData
#            rows.append(totalRow)
#
#            # print(maleRow)
#            # print(femaleRow)
#            # print(totalRow)
#
            # write all the rows
            with open(baseFile, "a", newline="") as newFile:
                # append to the new file
                newWriter = csv.writer(newFile)
                newWriter.writerows(rows)
#
            # reset tracker for location
            currLoc = line[0]
#
#            # and reset data lists
            gdpData.clear()
#            femaleData.clear()
#            totalData.clear()
#
#        # add the populations to the data list
#        # will be empty if needed (ie. new variant or new location)
        gdpData.append(line[3])
#        femaleData.append(line[7])
#        totalData.append(line[8])

