import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import generalGifs


def getYears(variant, country_name):
    filename = "data/TotalPopulation_%s.csv" % (variant)

    cf = pd.read_csv(filename)
    # Get the headers with the years
    years = list(cf.columns.values)[4:]
    years = list(map(int, years))

    return years


def getAllPops(variant, country_name, year):
    # returns population for all the groups
    year = str(year)
    groups = ["Total", "Male", "Female"]
    filename = "data/TotalPopulation_%s.csv" % (variant)

    cf = pd.read_csv(filename)
    # choose your country
    country = cf.loc[cf["Location"] == country_name]
    pops = {}

    for group in groups:
        # choose the group row, extracting the years and making it into a list
        pop = country.loc[country["Group"] == group][year].values.tolist()[0]
        pop = float(pop)
        pops[group] = pop

    return (variant, country_name), (year, pops)


def saveDoughnut(contriesOfInterest, figname, variant, year):

    outsideNames = []
    outsideSize = []
    outsideColors = []
    insideNames = []
    insideSize = []
    intsideColors = []
    colorOffset = 0
    colorSet = [plt.cm.Reds, plt.cm.Blues, plt.cm.Greens, plt.cm.Purples, plt.cm.Oranges]

    for country in contriesOfInterest:
        gmeta, (years, pops) = getAllPops(variant, country, year)
        country = country.replace(" ", "")

        thisColor = colorSet[colorOffset % len(colorSet)]

        outsideNames.append(country)
        outsideSize.append(pops["Total"])
        outsideColors.append(thisColor(0.6))

        insideNames.append("M")
        insideNames.append("F")
        insideSize.append(pops["Male"])
        insideSize.append(pops["Female"])
        intsideColors.append(thisColor(0.4))
        intsideColors.append(thisColor(0.2))

        colorOffset += 1

    # https://python-graph-gallery.com/163-donut-plot-with-subgroups/
    plt.axis('equal')
    mypie, _ = plt.pie(outsideSize, radius=1.3, colors=outsideColors)
    plt.setp(mypie, width=0.3, edgecolor='white')

    mypie2, _ = plt.pie(insideSize, radius=1, labeldistance=0.7, colors=intsideColors)
    plt.setp(mypie2, width=0.4, edgecolor='white')
    plt.margins(0, 0)

    plt.title("Total Population Breakdown | %s | %s" % (variant, year))

    # put labels: https://matplotlib.org/3.1.0/gallery/pie_and_polar_charts/pie_and_donut_labels.html
    bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
    kw = dict(arrowprops=dict(arrowstyle="-"),
              bbox=bbox_props, zorder=0, va="center")

    for i, p in enumerate(mypie):
        ang = (p.theta2 - p.theta1)/2. + p.theta1
        y = np.sin(np.deg2rad(ang))
        x = np.cos(np.deg2rad(ang))
        horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
        connectionstyle = "angle,angleA=0,angleB={}".format(ang)
        kw["arrowprops"].update({"connectionstyle": connectionstyle})
        plt.annotate(outsideNames[i], xy=(x, y), xytext=(1.35*np.sign(x), 1.4*y),
                     horizontalalignment=horizontalalignment, **kw)

    print("saving %s \t\t\t" % (figname), end="\r")
    plt.savefig(figname, bbox_inches='tight')
    plt.close()
    plt.clf()


variants = ["ConstantFertility", "ConstantMortality", "High", "InstantReplacement", "Low", "Medium", "Momentum", "NoChange", "ZeroMigration"]
contriesOfInterest = ["China", "United States of America", "Indonesia", "Brazil", "Pakistan",
                      "Bangladesh", "Russian Federation", "Mexico", "Japan", "Ethiopia", "Nigeria", "India"]

years = getYears("Medium", "World")  # same for everything

for variant in variants:
    print("making doughnut for %s" % (variant))
    generalGifs.initFolders()
    imageNames = []
    for year in years:
        filename = "tempimages/doughnut_%s_%s.png" % (variant, str(year))
        imageNames.append(filename)
        saveDoughnut(contriesOfInterest, filename, variant, year)

    gifname = "doughnut_%s.gif" % (variant)
    generalGifs.createGif(imageNames, gifname)
