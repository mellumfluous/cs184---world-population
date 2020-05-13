import pandas
import re
import os
import matplotlib.pyplot as plt
import imageio
import shutil

# the top locations that make up targetPercent of the worlds population for the given year
# data taken from the given file (assumed to be the output of the reformated population data)
# populations are in thousands


def saveGraphCumulative(totals, filename, meta):
    variant, year, percent = meta

    plt.xticks(rotation=90)
    plt.title("%s, %s | %s of total" % (variant, year, str(percent)+"%"))
    plt.plot(totals["Location"], totals["CumPercent"])
    plt.savefig(filename, bbox_inches='tight')
    plt.clf()


def graphCumulative(totals):
    plt.xticks(rotation=90)
    plt.plot(totals["Location"], totals["CumPercent"])
    plt.show()


def findTopXPercent(variant, year, targetPercent):
    # returns top Locations as well as cumulative percentage
    fileName = "data/TotalPopulation_%s.csv" % (variant)
    popDF = pandas.read_csv(fileName)

    # extract the totals per country from the data
    yearData = popDF[["LocationID", "Location", "Group", year]]
    yearTotals = yearData.loc[yearData["Group"] == "Total"]
    # ^ a DF with the location and its total population for the year given

    # extract the world's total population for the year
    # get the total world population for the year as given by the data
    totalWorldPopulation = yearTotals.loc[yearTotals["Location"] == "World"][year].item()
    # print(totalWorldPopulation)

    with open("country-list.txt") as country_list:
        # read in list of countries
        countries_file = country_list.read()

    # make list of countries
    countries = countries_file.split("\n")  # split on newline instead of whitespace (we want two worded countries)
    countries = [c for c in countries if c]  # remove empty lines
    countriesDF = pandas.DataFrame(data={"countries": countries})
    # print(countriesDF.countries)

    # remove all non-country locations by merging
    # make a common dataframe that has only countries and removes non-countries, dropping na values
    common = countriesDF.merge(yearTotals, how='inner', left_on=['countries'], right_on=['Location'])
    yearTotals = common.dropna()
    yearTotals = yearTotals.drop(columns=["countries"])  # drop countries since same as location
    # print(yearTotals)

    # find the percent of the world's total by location and add a column with that
    yearTotals["Percent"] = yearTotals[year]/totalWorldPopulation  # % of the world's population

    # sort by percent of world population
    yearTotals.sort_values(by=["Percent"], ascending=False, inplace=True)
    # print(yearTotals)

    # find the cumulative sum of percent
    yearTotals["CumPercent"] = yearTotals["Percent"].cumsum()
    # print(yearTotals)

    # find the locations that collectively make up targetPercent of the world's population
    topLocations = yearTotals[yearTotals["CumPercent"] < targetPercent]
    # print(topLocations)

    # the locations with populations than targetPercent (not needed, but done for fun)
    # greaterLocations = yearTotals.loc[yearTotals["Percent"] > targetPercent]
    # print(greaterLocations)

    return yearTotals, topLocations


def findTop():

    variant = "Medium"  # can be:
    #  "ConstantFertility" "ConstantMortality" "High" "InstantReplacement" "Low" "Medium" "Momentum" "NoChange" "ZeroMigration"

    year = "2020"
    targetPercent = 0.61  # 0 to 1
    # returns top Locations as well as cumulative percentage
    cumulativeTotals, topLocations = findTopXPercent(variant, year, targetPercent)

    # drops group not needed
    cumulativeTotals.drop(['Group'], axis=1, inplace=True)

    # exporting dataframe to intermediate data folder
    newfile = "intermediate-data/Medium-TotalPop-CountID%s.csv" % (year)
    # export_csv = cumulativeTotals.to_csv(newfile, index = None, header=True)  #Don't forget to add '.csv' at the end of the path

    # graph the cumulative sum (does not depend on targetPercent)
    # graphCumulative(cumulativeTotals)
    graphCumulative(topLocations)  # plot only the topLocations


def createGif():

    variants = ["ConstantFertility", "ConstantMortality", "High", "InstantReplacement", "Low", "Medium", "Momentum", "NoChange", "ZeroMigration"]
    variant = "Medium"  # can be:
    #  "ConstantFertility" "ConstantMortality" "High" "InstantReplacement" "Low" "Medium" "Momentum" "NoChange" "ZeroMigration"

    years = [str(y) for y in range(1950, 2101)]
    # years = [str(y) for y in range(2000, 2021)]
    targetPercent = 0.61  # 0 to 1
    # returns top Locations as well as cumulative percentage

    # crate temp folder
    if not os.path.isdir("tempimages"):
        os.mkdir("tempimages")

    if not os.path.isdir("gifs"):
        os.mkdir("gifs")

    imagenames = []
    gifname = "gifs/top%dpercent.gif" % (int(targetPercent*100))  # makes 0.xx to xx%
    for year in years:
        print("Variant: %s, year: %s" % (variant, year), end="\r")  # \r makes it stay on the same line
        cumulativeTotals, topLocations = findTopXPercent(variant, year, targetPercent)

        # save image
        imgname = "tempimages/image_%s_%s.png" % (variant, year)
        imagenames.append(imgname)
        metadata = (variant, year, targetPercent)
        saveGraphCumulative(topLocations, imgname, metadata)

    print("\nDone creating images")
    # create the gif
    totalFiles = len(imagenames)
    imgnum = 0
    figures = []
    for img in imagenames:
        imgnum += 1
        print("processing %s  [%d/%d]" % (img, imgnum, totalFiles), end="\r")
        figures.append(imageio.imread(img))

    imageio.mimsave(gifname, figures, duration=0.25)
    print("gif made at % s" % (gifname))

    # remove images and temp folder
    if os.path.isdir("tempimages"):  # should always be true here
        shutil.rmtree("tempimages")
    print("Images, temp folder removed")


# findTop()
createGif()
