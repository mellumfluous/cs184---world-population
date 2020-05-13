import pandas as pd
# from bokeh.plotting import figure, output_file, show
import matplotlib.pyplot as plt
import os


def getPop(variant, country_name, group="Total"):

    filename = "data/TotalPopulation_%s.csv" % (variant)

    cf = pd.read_csv(filename)
    # Get the headers with the years
    headers = list(cf.columns.values)[4:]
    # choose your country
    country = cf.loc[cf["Location"] == country_name]
    # choose the "total" row, extracting the years and making it into a list
    pops = country.loc[country["Group"] == group][headers].values.tolist()[0]
    # from string to float
    pops = list(map(float, pops))

    return (variant, country_name, group), (headers, pops)


# ignore "ConstantFertility", "ConstantMortality"
variants = ["High", "InstantReplacement", "Low", "Medium", "Momentum", "NoChange", "ZeroMigration"]

contriesOfInterest = ["China", "United States of America", "Indonesia", "Brazil", "Pakistan",
                      "Bangladesh", "Russian Federation", "Mexico", "Japan", "Ethiopia", "Nigeria", "India", "World"]
# top 61% countries from 2020

# make sure figs is a real directory
if not os.path.isdir("figs"):
    os.mkdir("figs")

for country in contriesOfInterest:
    xtix = None
    fig, axs = plt.subplots(1, 1)
    # track the highest and lowest variants
    greatestMeanGraphData = ([float("-inf")], [float("-inf")])  # float inf
    smallestMeanGraphData = ([float("inf")], [float("inf")])
    for v in variants:
        gmeta, gdata = getPop(v, country)
        axs.plot(gdata[0], gdata[1], label=v)

        dataMean = sum(gdata[1])/len(gdata[1])
        # set smallest mean data
        smallestMean = sum(smallestMeanGraphData[1])/len(smallestMeanGraphData[1])
        if dataMean < smallestMean:
            smallestMeanGraphData = gdata

        # set largest mean data
        greatestMean = sum(greatestMeanGraphData[1])/len(greatestMeanGraphData[1])
        if dataMean > greatestMean:
            greatestMeanGraphData = gdata

        # set ticks
        if xtix is None:
            xtix = [t for t in gdata[0] if int(t) % 10 == 0]

    # shade between the first line drawn and last line drawn
    # axs.fill_between(firstGraphData[0], firstGraphData[1], lastGraphData[1], alpha=0.3, color="#e0a05f")
    axs.fill_between(smallestMeanGraphData[0], smallestMeanGraphData[1], greatestMeanGraphData[1], alpha=0.3, color="#e0a05f")

    # Shrink current axis by 20%
    box = axs.get_position()
    axs.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    # Put a legend to the right of the current axis
    axs.legend(loc='center left', bbox_to_anchor=(1, 0.5), prop={"size": 7})

    axs.set_xticks(xtix)
    plt.title("Population for %s by variant" % (country))
    plt.xticks(rotation=90)
    figname = "figs/popFan_%s" % (country.replace(" ", ""))
    plt.savefig(figname, bbox_inches='tight')
    print("saved figure for %s" % (country))
