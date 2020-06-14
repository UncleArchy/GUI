from tkinter import *
from tkinter import filedialog
from PIL import ImageTk, Image
import subprocess
import trimesh
import dummy


def diagnosisDialog():
    global inputFile
    global outputFileAddress
    inputFile = filedialog.askopenfilename()
    # Вбрасываем изображение в окно
    userImage = Image.open(inputFile)
    userImage.thumbnail((200, 200), Image.ANTIALIAS)
    # print(inputFile)
    imageTk = ImageTk.PhotoImage(userImage)
    # imageLabel = Label(window, image=imageTk)
    # imageLabel.image = imageTk
    # imageLabel.grid(column=0, row=0)
    imageLabel.configure(image=imageTk)
    imageLabel.image = imageTk

    # Здесь должен происходить вызов функции, которая вернёт адрес файла с диагнозом
    # Пример ниже
    outputFileAddress = dummy.dummy(inputFile)
    diagnosis = open(outputFileAddress, 'r')
    diagnosisLabel.configure(text=diagnosis.read())
    diagnosisButton.configure(text="Choose another file to scan")


def tridimensionalDialog():
    inputDirectory = filedialog.askdirectory()
    utilInput = "-i " + inputDirectory
    utilOutput = inputDirectory + ".stl"
    # TODO: уточнить синтаксис вызова консольной команды, как минимум слеши в разных операционках в разные стороны
    subprocess.call(['./dicom2mesh ', utilInput, '-t 150', utilOutput])

    mesh = trimesh.load(utilOutput)
    volume = mesh.volume

    diagnosisLabel.configure(text="you can find your STL model in " + utilOutput)
    volumeLabel.configure(text="Volume of model is " + volume)
    stlButton.configure(text="Choose another directory for modelling")
    print()


window = Tk()
window.title("Добро пожаловать в приложение PythonRu")
window.geometry('700x700')

diagnosisLabel = Label(window, text="Welcome!", font=("Times New Roman", 16))
diagnosisLabel.grid(column=0, row=1)
volumeLabel = Label(window, text=" ", font=("Times New Roman", 16))
volumeLabel.grid(column=1, row=1)

welcomeImage = Image.open("2218.jpg")
welcomeImage.thumbnail((200, 200), Image.ANTIALIAS)
welcomeImageTk = ImageTk.PhotoImage(welcomeImage)

imageLabel = Label(window, image=welcomeImageTk)
imageLabel.image = welcomeImage
imageLabel.grid(column=0, row=0)

diagnosisButton = Button(window, text="Choose file to scan", command=diagnosisDialog)
diagnosisButton.grid(column=0, row=2)
stlButton = Button(window, text="Choose directory for modelling", command=tridimensionalDialog)
stlButton.grid(column=2, row=2)
window.mainloop()
