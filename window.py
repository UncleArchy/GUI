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
    userImage = Image.open(inputFile)
    userImage.thumbnail((200, 200), Image.ANTIALIAS)
    imageTk = ImageTk.PhotoImage(userImage)
    imageLabel.configure(image=imageTk)
    imageLabel.image = imageTk

    outputFileAddress = predict.predict_category(inputFile)
    diagnosis = open(outputFileAddress, 'r')
    diagnosisLabel.configure(text=diagnosis.read())
    # diagnosisButton.configure(text="Выбрать другой файл для сканирования")


def tridimensionalDialog():
    startPath = os.path.curdir
    inputDirectoryAbsolutePath = filedialog.askdirectory()
    inputDirectoryRelPath = os.path.relpath(inputDirectoryAbsolutePath, startPath)
    print(inputDirectoryRelPath)
    utilInput = inputDirectoryRelPath
    utilOutput = inputDirectoryRelPath + ".stl"
    subprocess.call(
        ["dicom2mesh.exe", "-i", utilInput, "-t", isoFrom.get(), "-tu", isoTo.get(), "-e", "0.1", "-o", utilOutput])

    diagnosisLabel.configure(text="STL-модель находится в  " + utilOutput)
    # modellingButton.configure(text="Выбрать другую папку для моделирования")


def volumeDialog():
    stlPath = filedialog.askopenfilename()
    mesh = trimesh.load(stlPath)
    volume = mesh.volume
    diagnosisLabel.configure(text="Объём модели " + "{:10.1f}".format(volume) + " куб.мм")


window = Tk()
window.title("Анализ DICOM-снимков")
window.geometry('420x450')

diagnosisLabel = Label(window, text="Добро пожаловать!", font=("Times New Roman", 16))
diagnosisLabel.place(x=70, y=220)
# volumeLabel = Label(window, text=" ", font=("Times New Roman", 16))
# volumeLabel.place(x=100, y=245)

welcomeImage = Image.open("2218.jpg")
welcomeImage.thumbnail((200, 200), Image.ANTIALIAS)
welcomeImageTk = ImageTk.PhotoImage(welcomeImage)

imageLabel = Label(window, image=welcomeImageTk)
imageLabel.image = welcomeImage
imageLabel.place(x=70, y=0)

diagnosisButton = Button(window, text="Выбрать файл для сканирования", command=diagnosisDialog)
diagnosisButton.place(x=20, y=260)
modellingButton = Button(window, text="Выбрать папку для моделирования", command=tridimensionalDialog)
modellingButton.place(x=20, y=295)
volumeButton = Button(window, text="Вычислить объём модели", command=volumeDialog)
volumeButton.place(x=20, y=330)

isoFrom = StringVar()
isoTo = StringVar()

# Заполнять значения ISO нужно ДО выбора папки
isoFromLabel = Label(window, text="мин. ISO:")
isoFromLabel.place(x=20, y=365)
isoFromEntry = Entry(window, textvariable=isoFrom)
isoFromEntry.place(x=120, y=365)
isoToLabel = Label(window, text="макс. ISO:")
isoToLabel.place(x=20, y=395)
isoToEntry = Entry(window, textvariable=isoTo)
isoToEntry.placeЗ(x=120, y=395)

window.mainloop()
