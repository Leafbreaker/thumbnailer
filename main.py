import subprocess
import os
import PIL
import re
import sys
from time import sleep
from PIL import Image
from random import randint



global pathToDirectory
pathToDirectory = subprocess.check_output('echo %cd%\\', shell=True).strip()
print pathToDirectory

def changeThumbnail(thumbnail, image):    
    pathToExiftool = '"' + pathToDirectory  + 'exiftool.exe' + '"' + ' "-thumbnailimage<=' + thumbnail +'" "' + image + '"'
    subprocess.call(pathToExiftool)

def changeThumbnailMP4(thumbnail, video):
    pathToAtomicParsley = '"' + pathToDirectory  + 'AtomicParsley.exe"' + ' "' + video +'" --artwork "' + thumbnail + '"'
    subprocess.call(pathToAtomicParsley)
    
def randomizeSelectionOfThumbnailsToImage(listOfimgs, listOfThumbnails):
    currentImage = 0
    chosenThumbnail = 0
    totalAmountOfImg = len(listOfimgs)
    for image in listOfimgs:
        currentImage += 1
        
        chosenThumbnail = randint(0,len(listOfThumbnails)-1)
        #thumbnail = resizeThumbnail(listOfThumbnails[chosenThumbnail], image[1], image[2])
        thumbnail = resizeThumbnail(listOfThumbnails[chosenThumbnail], image[1], image[2])
        print 'Changing image ' + str(currentImage) + '/' + str(totalAmountOfImg) + '\n'
        if not 'mp4' in image:
            #changeThumbnail(listOfThumbnails[thumbnail], image)
            changeThumbnail(thumbnail, image[0])
            print listOfThumbnails[chosenThumbnail] + ' , ' + image[0]
        else:
            #changeThumbnailMP4(listOfThumbnails[thumbnail], image)
            print listOfThumbnails[chosenThumbnail] + ' , ' + image[0]
        #chosenThumbnail += 1
def resizeThumbnail(imageName, targetImgWidth, targetImgHight):
    while ((targetImgWidth > 200) & (targetImgHight > 200)):
        targetImgWidth /= 10
        targetImgHight /= 10
        
    fileName=imageName.split('\\')[-1]
    img = Image.open(imageName)
    #img = img.resize((targetImgWidth, targetImgHight), Image.ANTIALIAS)
    img = img.resize((targetImgWidth, targetImgHight), Image.ANTIALIAS)
    nameOfThumbnailCreated = pathToDirectory + 'thumbnails\\' + fileName
    img.save(nameOfThumbnailCreated)
    img.close()
    #sleep(5)
    return nameOfThumbnailCreated



def setDirectories():
    thumbnailDirectory = '.'
    imageDirectory = '.'
    DirectoryNames = []
    print "The follwing folders where found in working directory:\n"
    for root, dirs , files in os.walk(pathToDirectory, topdown=False):
        for name in dirs:
            print name
            #print(os.path.join(root, name))
            DirectoryNames.append(name)
    
    while thumbnailDirectory not in DirectoryNames:
        thumbnailDirectory = raw_input('Write the name of the directory containing the fake thumbnails: ')
    while imageDirectory not in DirectoryNames:
        imageDirectory = raw_input('Write the name of the directory containing the images to be changed: ')
    
    return (thumbnailDirectory, imageDirectory)

def mapImageDirectory(imageDirectory):
    listOfimgs = []
    for root, dirs , files in os.walk(pathToDirectory+imageDirectory, topdown=False):
        for name in files: 
            listOfimgs.append(infoTupleAboutImage(os.path.join(root, name)))            
    return listOfimgs

def infoTupleAboutImage(imageLocation):
    im = Image.open(imageLocation)
    imgWidth, imgHight = im.size
    #fileName=imageLocation.split('\\')[-1]
    #imageLocation = pathToDirectory + 'target\\' + fileName
    #im.save(imageLocation, dpi=(96,96))
    im.close()
    return (imageLocation,imgWidth,imgHight)
    
def createThumbnails(thumbnailDirectory):
    print 'Creating thumbnails...\n'
    listOfThumbs = []
    listOfThumbFileName = []
    if not os.path.exists('thumbnails'):
        os.makedirs('thumbnails')
    for root, dirs , files in os.walk(pathToDirectory+thumbnailDirectory, topdown=False):
        for name in files:
            listOfThumbs.append((os.path.join(root, name)))
    
    #for image in listOfThumbs:
    #    listOfThumbFileName.append(createThumbnail(image))
    print 'Thumbnails created!!!\n'
    print listOfThumbs
    return listOfThumbs

def cleanUp(images, imageDirectory):
    filesToBeRestored = []
    if not os.path.exists('originals'):
        os.makedirs('originals')
    print "Placing original images in originals directory"
    for image in images:
        if '_original' in image:
            originalFileName = re.sub('_original', '', image)
            originalFileName = re.sub(imageDirectory, 'originals', originalFileName)
            try:
                os.rename(image, originalFileName)
            except:
                print "Could not move " + image + " to originals folder!"
                pass
        if'.mp4' in image:
            if '-temp-' in image:
                originalFileName = re.sub('-temp-\d+', '', image)
                try:
                    os.rename(image, originalFileName)
                except:
                    filesToBeRestored.append((image, originalFileName))
                
            else:
                originalFileName = re.sub(imageDirectory, 'originals', originalFileName)
                os.rename(image, originalFileName)
                
    if filesToBeRestored:
        for file in filesToBeRestored:
            os.rename(file[0], file[1])
#------------------------------------------MAIN----------------------------------------------------------------
print "  _______ _                     _                 _ _           "
print " |__   __| |                   | |               |_| |          " 
print "    | |  | |__  _   _ _ __ ___ | |__  _ __   __ _ _| | ___ _ __ " 
print "    | |  | '_ \| | | | '_ ` _ \| '_ \| '_ \ / _` | | |/ _ \ '__|" 
print "    | |  | | | | |_| | | | | | | |_) | | | | (_| | | |  __/ |   " 
print "    |_|  |_| |_|\__,_|_| |_| |_|_.__/|_| |_|\__,_|_|_|\___|_|   " 
print "                         by Leafbreaker                         "

thumbnailDirectory, imageDirectory = setDirectories()

listOfThumbnails = createThumbnails(thumbnailDirectory)
listOfimgs = mapImageDirectory(imageDirectory)

randomizeSelectionOfThumbnailsToImage(listOfimgs, listOfThumbnails)

cleanUp(mapImageDirectory(imageDirectory), imageDirectory)

print "Finished! :3"