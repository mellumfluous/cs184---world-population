import os
import imageio
import shutil


# Flow:
# call initFolders()
#     tempfolder and all contents will be automatically removed
# create and save figure images in folder tempimages/
#     save the path name into a list
#        imglist = ["tempimages/img1.png", "tempimages/img2.png"...]
# pass that list and the desired name of the gif into createGif(imglist,gifname, speed)
#     note: gif will automatically be put into gifs/ folder don't include "gifs/" in the path for gifname
#     example call: createGif(imglist,"foo.gif")
#     speed is the time in between frames in seconds (default = 0.25)

def initFolders():
    # crate temp folder
    if not os.path.isdir("tempimages"):
        os.mkdir("tempimages")
    else:
        for filename in os.listdir("tempimages"):
            os.remove("tempimages/%s" % (filename))

    if not os.path.isdir("gifs"):
        os.mkdir("gifs")


def createGif(imageList, gifname, speed=0.25):
    gifname = "gifs/%s" % (gifname)
    # create the gif
    # https://stackoverflow.com/questions/753190/programmatically-generate-video-or-animated-gif-in-python

    totalFiles = len(imageList)
    imgnum = 0
    figures = []
    for img in imageList:
        imgnum += 1
        print("[%d/%d] | processing %s \t\t\t" % (imgnum, totalFiles, img), end="\r")
        figures.append(imageio.imread(img))

    imageio.mimsave(gifname, figures, duration=speed)
    print("\ngif made at % s" % (gifname))

    # remove images and temp folder
    if os.path.isdir("tempimages"):  # should always be true here
        shutil.rmtree("tempimages")
    print("Images, temp folder removed")
