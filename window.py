import os
from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
import subprocess
import trimesh
import diagnosis_predict.stomach_predict as predict


def diagnosisDialog():
    global inputFile
    global outputFileAddress
    inputFile = filedialog.askopenfilename()
    # Вбрасываем изображение в окно
    userImage = Image.open(inputFile)
    userImage.thumbnail((200, 200), Image.ANTIALIAS)
    imageTk = ImageTk.PhotoImage(userImage)
    imageLabel.configure(image=imageTk)
    imageLabel.image = imageTk

    # Здесь должен происходить вызов функции, которая вернёт адрес файла с диагнозом
    # Пример ниже
    outputFileAddress = predict.predict_category(inputFile)#dummy.dummy(inputFile)
    diagnosis = open(outputFileAddress, 'r')
    diagnosisLabel.configure(text=diagnosis.read())
    diagnosisButton.configure(text="Choose another file to scan")


def tridimensionalDialog():
    startPath = os.path.curdir
    inputDirectoryAbsolutePath = filedialog.askdirectory()
    inputDirectoryRelPath = os.path.relpath(inputDirectoryAbsolutePath, startPath)
    print(inputDirectoryRelPath)
    utilInput = inputDirectoryRelPath
    utilOutput = inputDirectoryRelPath + ".stl"
    # TODO: уточнить синтаксис вызова консольной команды, как минимум слеши в разных операционках в разные стороны
    subprocess.call(["dicom2mesh.exe", "-i", utilInput, "-t", isoFrom.get(), "-tu", isoTo.get(), "-e", "0.1", "-o", utilOutput])

    mesh = trimesh.load(utilOutput)
    volume = mesh.volume

    print("I WAS HERE")
    diagnosisLabel.configure(text="you can find your STL model in " + utilOutput)
    volumeLabel.configure(text="Volume of model is " + "{:10.1f}".format(volume))
    stlButton.configure(text="Choose another directory for modelling")
    print()


window = Tk()
window.title("Добро пожаловать в приложение PythonRu")
window.geometry('500x400')

diagnosisLabel = Label(window, text="Welcome!", font=("Times New Roman", 16))
diagnosisLabel.place(x=70, y=220)
volumeLabel = Label(window, text=" ", font=("Times New Roman", 16))
volumeLabel.place(x=100, y=245)

welcomeImage = Image.open("2218.jpg")
welcomeImage.thumbnail((200, 200), Image.ANTIALIAS)
welcomeImageTk = ImageTk.PhotoImage(welcomeImage)

imageLabel = Label(window, image=welcomeImageTk)
imageLabel.image = welcomeImage
imageLabel.place(x=70, y=0)

diagnosisButton = Button(window, text="Choose file to scan", command=diagnosisDialog)
diagnosisButton.place(x=20, y=290)
stlButton = Button(window, text="Choose directory for modelling", command=tridimensionalDialog)
stlButton.place(x=150, y=290)

isoFrom = StringVar()
isoTo = StringVar()

#Заполнять значения ISO нужно ДО выбора папки
isoFromLabel = Label(window, text="ISO from:")
isoFromLabel.place(x=20, y=320)
isoFromEntry = Entry(window, textvariable=isoFrom)
isoFromEntry.place(x=120, y=320)
isoToLabel = Label(window, text="ISO to:")
isoToLabel.place(x=20, y=350)
isoToEntry = Entry(window, textvariable=isoTo)
isoToEntry.place(x=120, y=350)



window.mainloop()
