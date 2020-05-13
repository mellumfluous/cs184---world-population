# script to break up and reformat the population data

import csv
import time

ORIG_DATA = "data/WPP2017_TotalPopulationBySex.csv"


# helper function to write the three rows per location
def writeLocRows(filename, trackingVars, data):
    currLocID,currLoc, currVar = trackingVars
    maleData, femaleData, totalData = data

    rows = []
    # remember new header: ["LocationID","Location", "Variant", "Group", 1959, ..., 2100]
    # male data
    maleRow = [currLocID,currLoc, currVar, "Male"] + maleData
    rows.append(maleRow)
    # female data
    femaleRow = [currLocID,currLoc, currVar, "Female"] + femaleData
    rows.append(femaleRow)
    # total data
    totalRow = [currLocID,currLoc, currVar, "Total"] + totalData
    rows.append(totalRow)

    # print(maleRow)
    # print(femaleRow)
    # print(totalRow)

    # write all the rows
    with open(filename, "a", newline="") as newFile:
        # append to the new file
        newWriter = csv.writer(newFile)
        newWriter.writerows(rows)


# break the original file into other, reformated files
# we ignore midPeriod, and ID values in the reformatted files
with open(ORIG_DATA, "r") as origdata:
    baseFile = "data/TotalPopulation_[[VARIANT]].csv"  # [[VARIANT]] will be replaced
    origReader = csv.reader(origdata)
    header = next(origReader)
    # print(header)

    # Group is Male, Female, or Total
    newHeader = ["LocationID","Location", "Variant", "Group"]
    # create years
    for y in range(1950, 2101):  # data has year range 1950-2100
        newHeader.append(y)
    # print(newHeader)

    # read first line and set initial values for tracking variables
    firstLine = next(origReader)
    # tracking variables
    currLocID = firstLine[0]
    currLoc = firstLine[1]
    currVar = firstLine[3]
    var = firstLine[3].title().replace(" ", "")  # make "Hello world"  to "HelloWorld"
    currFileName = baseFile.replace("[[VARIANT]]", var)
    print("Now writing to: %s" % (currFileName))
    # print(currFileName)

    # write new header
    with open(currFileName, "w", newline="") as newFile:
        newWriter = csv.writer(newFile)
        newWriter.writerow(newHeader)

    # data in orig is a column from 1950-2100, we make it part of the row
    # data of population values per year
    # each of these is for one country/location
    maleData = [firstLine[6]]
    femaleData = [firstLine[7]]
    totalData = [firstLine[8]]

    # read in all the other lines
    for line in origReader:
        # print(line)

        # set tracking vars
        lineLocID = line[0]
        lineLoc = line[1]
        lineVar = line[3]

        if lineLoc != currLoc:  # new location

            # write location data
            trackingVars = (currLocID,currLoc, currVar)
            data = (maleData, femaleData, totalData)
            writeLocRows(currFileName, trackingVars, data)

            # reset tracker for location
            currLocID = lineLocID
            currLoc = lineLoc

            # and reset data lists
            maleData.clear()
            femaleData.clear()
            totalData.clear()

        if lineVar != currVar:  # new variant, want to make new file
            # the way the orig data is done, if the variant changes, so does the location
            #   which means the location block above is also run

            # create new file name
            var = line[3].title().replace(" ", "")  # make "Hello world"  to "HelloWorld"
            currFileName = baseFile.replace("[[VARIANT]]", var)
            print("Now writing to: %s" % (currFileName))

            # write new header to new file
            with open(currFileName, "w", newline="") as newFile:
                newWriter = csv.writer(newFile)
                newWriter.writerow(newHeader)

            # reset tracking variables
            # currLoc already set in location block above
            currVar = lineVar

            # data lists already cleared in location block above

        # add the populations to the data list
        # will be empty if needed (ie. new variant or new location)
        maleData.append(line[6])
        femaleData.append(line[7])
        totalData.append(line[8])

    # write the stuff that hasnt been written yet ()
    trackingVars = (currLocID,currLoc, currVar)
    data = (maleData, femaleData, totalData)
    writeLocRows(currFileName, trackingVars, data)
