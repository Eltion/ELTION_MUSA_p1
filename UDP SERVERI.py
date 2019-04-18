from datetime import datetime
from socket import *
import random
import math
from _thread import * 
from urllib.request import Request, urlopen
import re

serverName = '127.0.0.1'
serverPort = 12000
serverSocket = socket(AF_INET, SOCK_DGRAM) #SOCK_DGRAM per UDP
serverSocket.bind((serverName, serverPort))

print("------FIEK UDP SERVER------")
print("SERVERI ESHTE DUKE NDEGJUAR")

def EMRIIKOMPJUTERIT():
    if(gethostname() == None or gethostname() == ""):
        return "Nuk mund te mirret emri"
    else:    
        return gethostname()

def IPADRESA(addr):
    return addr[0]

def NUMRIIPORTIT(addr):
    return addr[1]

def BASHKETINGELLORE(fjalia):
    k = 0;
    zanoret = "AEËIOUYaëeiouy";
    for shkronja in fjalia:
        if(shkronja not in zanoret and shkronja.isalpha()):
            k += 1

    return k

def KOHA():
    koha = datetime.now();
    #strftime ("%Y.%m.%d %H:%M:%S", koha);
    koha = koha.strftime("%Y.%m.%d %H:%M:%S %p");
    return koha

def LOJA():
    res = ""
    for i in range(7):
        x = random.randint(1,29)
        res += str(x)+","
    return res[:-1] #kthen stringun pa karakterin e fundit

def FIBONACCI(n):
    a = 0;
    b = 1;

    for i in range(n-1):
        temp = a #ruan
        a = b
        b +=  temp
    return b

def KONVERTIMI(o, n):
    print(n)
    if( o == "KilowattToHorsepower"):
        return n*1.341
    elif( o == "HorsepowerToKilowatt"):
        return n/1.341
    elif( o == "DegreesToRadians"):
        return (n*math.pi)/180
    elif(o == "RadiansToDegrees"):
        return (n*180)/math.pi
    elif(o == "GallonsToLiters"):
        return n*3.78541
    elif(o == "LitersToGallons"):
        return n/3.78541

def PRINTIMI(fjalia):
    fjalia = fjalia.lstrip().rstrip();
    return fjalia

def LAJMET():
    res = "";
    try:
        res = urlopen("https://www.gazetaexpress.com/lajme/").read().decode();
    except Exception  as err: 
        return "Serveri nuk ka qasje ne rrjet"

    res = res.split("news-box")
    if(len(res) < 4):
        return "Serveri nuk mund ta procesoj kerkesen"

    resultati = "";
    for i in range(1,5):
        r1 = re.search('href="([^"]*)',res[i])
        r2 = re.search('<h2>([^<]*)',res[i])
        resultati += r2.group(1).lstrip()+"\nUrl: "+r1.group(1) +"\n\n";

    return resultati    

def NUMRIITHJESHT(n):
    if(n < 1):
        return "Numri duhet te jet me i madh se 0"
    for i in range(2,n):
        if(n % i == 0):
            return "NUMRI NUK ESHTE I THJESHT"
    return "NUMRI ESHTE I THJESHT"    
    
def TestoFloat(n):
    try:
        float(n)
        return True
    except ValueError as e:
        return False 

def VerifikoKerkesen(kerkesa):
    if(len(kerkesa) > 128):
        return False

    KonvertimiOptions = ["KilowattToHorsepower","HorsepowerToKilowatt",
                          "DegreesToRadians","RadiansToDegrees","GallonsToLiters",
                          "LitersToGallons"]

    Komandat = ["IPADRESA","NUMRIIPORTIT","EMRIIKOMPJUTERIT","KOHA","LOJA","LAJMET"]                      

    kerkesaArray = kerkesa.split(" ");
    funksioni = kerkesa.split(" ")[0];
    firstSpace = kerkesa.find(" ");
    if(funksioni in Komandat):
        return [funksioni]
    elif((funksioni == "BASHKETINGELLORE" or funksioni == "PRINTIMI") and (firstSpace != -1 or not kerkesa[firstSpace:].replace(" ","")=="" )):
        return [funksioni,kerkesa[firstSpace:]]
           #nese eshte konveritmi shiko a i ka 3 prarametra,         opcioni eshte i sakte,                      parametri i trete a eshte float
    elif(funksioni == "KONVERTIMI" and len(kerkesaArray) >= 3 and (kerkesaArray[1] in KonvertimiOptions) and TestoFloat(kerkesaArray[2])):
        return kerkesaArray
    elif((funksioni == "FIBONACCI" or funksioni == "NUMRIITHJESHT") and len(kerkesaArray) >= 2 and kerkesaArray[1].isdigit()):
        return kerkesaArray
    else:
        return False 

def main(kerkesa1,addr):
    print("KERKESA: "+ kerkesa1)
    kerkesa = VerifikoKerkesen(kerkesa1)
    if(kerkesa == False):
        return "FUNKISONI NUK EKZISTON"
    elif(kerkesa[0] == "BASHKETINGELLORE"):
       return BASHKETINGELLORE(kerkesa[1])
    elif(kerkesa[0] == "KOHA"):
        return KOHA()
    elif(kerkesa[0] == "LOJA"):
        return LOJA()
    elif(kerkesa[0] == "FIBONACCI"):
        return FIBONACCI(int(kerkesa[1]))
    elif(kerkesa[0] == "KONVERTIMI"):
        return KONVERTIMI(kerkesa[1],float(kerkesa[2]))
    elif(kerkesa[0] == "EMRIIKOMPJUTERIT"):
        return EMRIIKOMPJUTERIT()
    elif(kerkesa[0] == "NUMRIIPORTIT"):
        return NUMRIIPORTIT(addr)
    elif(kerkesa[0] == "IPADRESA"):
        return IPADRESA(addr)
    elif(kerkesa[0] == "PRINTIMI"):
        return PRINTIMI(kerkesa[1])  
    elif(kerkesa[0] == "LAJMET"):
        return LAJMET()   
    elif(kerkesa[0] == "NUMRIITHJESHT"):
        return NUMRIITHJESHT(int(kerkesa[1])) 

def NdegjoKlientin(s,message, addr):    
    print("Klienti "+ addr[0] + " me portin "+ str(addr[1]))
    res = str(main(message.decode(),addr));
    print(res)
    s.sendto(res.encode(),(addr[0],addr[1]));
    

while True:
    message, addr = serverSocket.recvfrom(1024)
    start_new_thread(NdegjoKlientin, (serverSocket,message,addr) )

