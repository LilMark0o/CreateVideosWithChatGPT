from gtts import gTTS
import os
import shutil
from PIL import Image
from moviepy.editor import *

fileName = "chessWorldChampions"
filePath = "scripts/"+fileName+".txt"
script = open(filePath)
language = "en"
i = 1

def titulo(texto:str):
    separador = "-"*20
    aPrintear = "{0} {1} {0}".format(separador,texto)
    print(aPrintear)

def emptyFolderData():
    listDir = os.listdir("data")
    for directory in listDir:
        if ((directory[0]!=".") and not(directory=="staticFolder")):
            shutil.rmtree("data/"+directory)


def createAllDirectories():
    if not (os.path.isdir("data/"+fileName)):
        os.mkdir("data/"+fileName)
    if not (os.path.isdir("supportData/"+fileName)):
        os.mkdir("supportData/"+fileName)
    if not (os.path.isdir("finalData/"+fileName)):
        os.mkdir("finalData/"+fileName)
    if not (os.path.isdir("data/"+fileName+"/instructions")):
        os.mkdir("data/"+fileName+"/instructions")
    if not (os.path.isdir("data/"+fileName+"/audios")):
        os.mkdir("data/"+fileName+"/audios")
    if not (os.path.isdir("data/"+fileName+"/imagesFinal")):
        os.mkdir("data/"+fileName+"/imagesFinal")

def niceInstruction(text:str,i:int):
    text = text.replace("[","").replace("]","")
    newText = "audio {0} must have: \n{1}\n\n".format(i,text)
    return newText

def createInstructionFile(text:str):
    instructionFileName = "data/"+fileName+"/instructions/"+"Instructions.txt"
    instructionFile = open(instructionFileName,"w+")
    instructionFile.write(text)
    instructionFile.close()

def textToAudioFile(textPar,language,i)->None:
    myobj = gTTS(text=textPar, lang=language, slow=False)
    name = "data/"+fileName+"/audios/audio"+str(i)+".mp3"
    myobj.save(name)

def readFileAndCreateAudios(language,i):
    titulo("Let's start!")
    createAllDirectories()
    instructions = "--- " +fileName + " instructions for images over the video ---\n\n"
    for line in script:
        line=line.replace("\n","")
        if (line!=""):
            if (line[0]!="[" and not("PART" in line) and (line[-1]!=":")):
                if ":" in line:
                    parts = line.split(":")
                    useful = parts[1].replace("\n","")
                else:
                    useful = line
                textToAudioFile(useful,language,i)
                i +=1
            else:
                instructions += niceInstruction(line,i)
    createInstructionFile(instructions)
    titulo("Task was completed successfully!")

def standardizeImages():
    titulo("Let's standardize all the images!")
    listDir = os.listdir("supportData/"+fileName)
    for directory in listDir:
        backgroundIMG = Image.open("data/staticFolder/background.jpg")
        widthBack,heightBack=backgroundIMG.size
        if directory[0]!=".":
            image= Image.open("supportData/"+fileName+"/"+directory)
            width,height=image.size
            diferenceWidth = width/widthBack
            diferenceHeight = height/heightBack
            if diferenceWidth>diferenceHeight:
                image = image.resize((round(width/diferenceWidth),round(height/diferenceWidth)))
            else:
                image = image.resize((round(width/diferenceHeight),round(height/diferenceHeight)))
            width,height=image.size
            heightToPaste = round((heightBack-height)/2)
            widthToPaste = round((widthBack-width)/2)
            backgroundIMG.paste(image,(widthToPaste,heightToPaste))
                                     
            image = backgroundIMG.convert("RGB")
            fileNameImage = directory.split(".")[0]

            image.save("data/"+fileName+"/imagesFinal/"+fileNameImage+".jpg")
    titulo("Task was completed successfully!")

def createClips():
    titulo("Let's create all the miniClips!")

    listDir = os.listdir("data/"+fileName+"/imagesFinal")
    clips = []
    for number in range(1,len(listDir)+1):
        # Import the audio(Insert to location of your audio instead of audioClip.mp3)
        audioName = "audio{}.mp3".format(number)
        audioPath = "data/"+fileName+"/audios/"+audioName
        audio = AudioFileClip(audioPath)
        # Import the Image and set its duration same as the audio (Insert the location of your photo instead of photo.jpg)
        imageName = "img{}.jpg".format(number)
        imagePath = "data/"+fileName+"/imagesFinal/"+imageName
        clip = ImageClip(imagePath).set_duration(audio.duration)
        # Set the audio of the clip
        clip = clip.set_audio(audio)
        #! let's try something better
        clips.append(clip)

    videoName = fileName+".mp4"
    finalVideoPath = "finalData/"+fileName+"/"+videoName
    finalClip = concatenate_videoclips(clips)
    finalClip.write_videofile(finalVideoPath,fps=30)

    titulo("Task was completed successfully!")
