#KLIENTI TCP
#Autor Eltion Musa


from tkinter import *
from tkinter import simpledialog
import socket

s =  None;

serverName = "127.0.0.1"
port = "1200"
KeepConnect = 1

class MyDialog(simpledialog.Dialog):

    def body(self, master):

        Label(master, text="Hosi:").grid(row=0,column=0)
        Label(master, text="Porti:").grid(row=1,column=0)
        self.KeepConnect = IntVar()
        self.CheckBox = Checkbutton(master, text="Mbaje lidhjen deri ne fund", variable=self.KeepConnect,pady=10)
        self.CheckBox.grid(row=3,column=1)
        self.CheckBox.select() 
        self.e1 = Entry(master)
        self.e2 = Entry(master)

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        return self.e1 # initial focus

    def apply(self):
        global serverName, port, c
        serverName = self.e1.get()
        port = self.e2.get()
        c = self.KeepConnect.get()
        if(c == 1):
            connect()

def showEditText(help):
    vhelp_text.set(help)
    help_text.grid(row=9, column=0,sticky=W)
    textEntry.grid(row=10,column=0,columnspan=2)

def hideEditText():
    help_text.grid_forget()
    textEntry.grid_forget()

def hideFrame():
    frame.grid_forget()

def showFrame():
    frame.grid(row=7, column=0, columnspan=2)


def ndyshoPamjen():
    textEntry.delete(0,END)

    if(var.get() == "KONVERTIMI"):
        showFrame()
        showEditText("Shenoni nje numer:")
    elif(var.get() == "BASHKETINGELLORE" or var.get() == "PRINTIMI"):
        hideFrame()
        showEditText("Shenoni nje fjali:")
    elif(var.get() == "FIBONACCI" or var.get() == "NUMRIITHJESHT"):
        hideFrame()
        showEditText("Shenoni nje numer:")
    else:
        hideFrame()
        hideEditText()
                  
       
window = Tk()                           #Krijon dritaren

window.title('FIEK KLIENT')             #titilli e dritares

window.iconbitmap("logo.ico");          #Ikona e dritares

window.resizable(width=False, height=False)  #Nuk lejon ndrrimin e madhesise se dritares

Label(window,text="\nZgjedhni njerin nga opcionet\n").grid(row=0, column=0,sticky=W) #Vendos nje Label


var = StringVar()
var.set("IPADRESA")

RadioButonat = {
        "IPADRESA":"IPADRESA",
        "NUMRI I PORTIT":"NUMRIIPORTIT",
        "BASHKETINGELLORE":"BASHKETINGELLORE",
        "PRINTIMI":"PRINTIMI",
        "EMRI I KOMPJUTERIT":"EMRIIKOMPJUTERIT",
        "KOHA":"KOHA",
        "LOJA":"LOJA",
        "NUMRI FIBONACCI":"FIBONACCI",
        "KONVERTIMI":"KONVERTIMI",
        "LAJMET" : "LAJMET",
        "NUMRI I THJESHT":"NUMRIITHJESHT"
}

#Krijimi i radioButonave
row = 1
column = 0
for text, funksioni in RadioButonat.items(): 
    R1 = Radiobutton(window, text=text, variable=var, value=funksioni, command=ndyshoPamjen)
    R1.grid(row=row, column=column, sticky=W)
    row+=1
    if(row == 7):
        column+= 1
        row = 1;



frame = Frame(window)
frame.grid(row=7, column=0, columnspan=2)

Label(frame,text="\nZgjedhni njerin nga opcionet\n").grid(row=0, column=0,sticky=W)

RadioButonatKonvertimi = ["KilowattToHorsepower","HorsepowerToKilowatt",
                          "DegreesToRadians","RadiansToDegrees","GallonsToLiters",
                          "LitersToGallons"]

var1 = StringVar() 
var1.set("KilowattToHorsepower")

row = 1
column = 0
for opcioni in RadioButonatKonvertimi:
    print(opcioni)
    RB = Radiobutton(frame, text=opcioni, variable=var1, value=opcioni)
    RB.grid(row=row, column=column, sticky=W)
    row+=1
    if(row == 4):
        column+= 1
        row = 1;


vhelp_text = StringVar()
help_text = Label(window,textvariable=vhelp_text)
help_text.grid(row=9, column=0,sticky=W)


textEntry = Entry(window,width=50)
textEntry.grid(row=10,column=0,columnspan=2)

def connect():
    print(serverName+":"+port)
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((serverName, int(port)))
    if(c == 1):
        s.send("Mbaje Lidhjen".encode())

def TestoFloat(n):
    try:
        float(n)
        return True
    except ValueError as e:
        return False 

def verefikoKerkesen():
    if(var.get() == "BASHKETINGELLORE" or var.get() == "PRINTIMI"):
        if(textEntry.get().replace(" ","") == ""):
            return "Shenoni nje fjali!!!!"
        else:
            return True    
    elif(var.get() == "FIBONACCI" or var.get() == "NUMRIITHJESHT"):
        if(not textEntry.get().isdigit()):
            return "Shenoni nje numer!!!"
        else:
            return True    
    elif(var.get() == "KONVERTIMI"):
        if(not TestoFloat(textEntry.get())):
            return "Ju duhet te shenoni nje numer"
        else:
            return True    
    else:
        return True

def send():
    verifikimi = verefikoKerkesen()
    if(verifikimi != True):
        print(verifikimi)
        text_box.delete("1.0",END)    
        text_box.insert(END,verifikimi)
        return
    if(c == 0):
        connect()
    funksioni = var.get() +" "

    if(var.get() == "KONVERTIMI"):
        message = funksioni + var1.get() + " " + textEntry.get()
    else:
        message = funksioni + textEntry.get()
    s.send(str.encode(message))

    r = s.recv(2048).decode()
    if(c == 0):
        s.close()

    text_box.delete("1.0",END)    
    text_box.insert(END,r)


sendButton = Button(window,text="DERGO",command=send)
sendButton.grid(row=11,column=0,columnspan=2,pady=15)




Label(window,text="\nResultati:\n").grid(row=12, column=0, sticky=W)

text_box = Text(window,width=40,height=8)
text_box.grid(row=13, column=0, columnspan=2)

hideFrame()

d = MyDialog(window)


window.mainloop() 


