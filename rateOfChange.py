import pandas as pd
from numpy import diff
import matplotlib.pyplot as plt
import generalGifs


def getPop(variant, country_name, group="Total"):

    filename = "data/TotalPopulation_%s.csv" % (variant)

    cf = pd.read_csv(filename)
    # Get the headers with the years
    years = list(cf.columns.values)[4:]
    # choose your country
    country = cf.loc[cf["Location"] == country_name]
    # choose the "total" row, extracting the years and making it into a list
    pop = country.loc[country["Group"] == group][years].values.tolist()[0]
    # from string to float
    pop = list(map(float, pop))
    years = list(map(int, years))

    return (variant, country_name, group), (years, pop)


def saveGraph(filename, data, meta):
    variant, country, group = meta
    pop, first, second, years = data
    tendToZero = ""
    lastx = 2  # get the last 2 numbers from second derivative
    lastxavg = sum(second[-lastx:])/lastx

    if abs(lastxavg) < 20:
        tendToZero = " - tends to 0"

    plt.xticks(rotation=90)
    plt.title("%s | %s, %s %s" % (variant, group, country, tendToZero))
    plt.plot(years[1:], first, label='first')
    plt.plot(years[2:], second, label='second')
    plt.plot(years, [0]*len(years), color="black", linestyle='dashed', linewidth="0.5", label="zero")
    plt.legend()
    plt.savefig(filename, bbox_inches='tight')
    plt.clf()


def analyzeROC():
    # only interested in Medium variant
    variant = "Medium"
    contriesOfInterest = ["China", "United States of America", "Indonesia", "Brazil", "Pakistan",
                          "Bangladesh", "Russian Federation", "Mexico", "Japan", "Ethiopia", "Nigeria", "India"]

    highestList1 = []
    lowestList1 = []
    highestList2 = []
    lowestList2 = []

    for country in contriesOfInterest:
        meta, (years, pop) = getPop(variant, country)
        # get first derivative
        first = diff(pop)
        # get second derivative
        second = diff(first)

        # create and add tuples
        low1 = first.min()
        low2 = second.min()
        lowestList1.append((low1, country))
        lowestList2.append((low2, country))

        high1 = first.max()
        high2 = second.max()
        highestList1.append((high1, country))
        highestList2.append((high2, country))

        # print(country, low1, high1)
        # print(country, low2, high2)

    # sort the lists (accending order)
    highestList1.sort()
    lowestList1.sort()
    highestList2.sort()
    lowestList2.sort()

    # get highest and lowest values
    highest1, highest1country = highestList1[-1]
    highest2, highest2country = highestList2[-1]
    lowest1, lowest1country = lowestList1[0]
    lowest2, lowest2country = lowestList2[0]

    print("highest first derivative:   %s:  %d  ppl/yr" % (highest1country, highest1))
    print("highest second derivative:  %s:  %d  ppl/yr^2" % (highest2country, highest2))
    print("lowest first derivative:    %s:  %d  ppl/yr" % (lowest1country, lowest1))
    print("lowest second derivative:   %s:  %d  ppl/yr^2" % (lowest2country, lowest2))


# ignore "ConstantFertility", "ConstantMortality"
variants = ["High", "InstantReplacement", "Low", "Medium", "Momentum", "NoChange", "ZeroMigration"]
contriesOfInterest = ["China", "United States of America", "Indonesia", "Brazil", "Pakistan",
                      "Bangladesh", "Russian Federation", "Mexico", "Japan", "Ethiopia", "Nigeria", "India", "World"]

group = "Total"
for country in contriesOfInterest:
    generalGifs.initFolders()
    print("making gif for %s" % (country))
    imageNames = []
    for var in variants:
        meta, (years, pop) = getPop(var, country, group)

        # get first derivative
        first = diff(pop)
        # get second derivative
        second = diff(first)
        countryFile = country.replace(" ", "")
        filename = "tempimages/%s_%s_%s.png" % (group, countryFile, var)
        imageNames.append(filename)
        saveGraph(filename, (pop, first, second, years), meta)

    generalGifs.createGif(imageNames, "rateOfChange_%s_%s.gif" % (countryFile, group), 1)

print("\n\nfind the most extreme values from our countries of interest")
analyzeROC()
