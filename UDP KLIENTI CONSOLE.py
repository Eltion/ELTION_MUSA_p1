import socket

Socket = None


def AskPort():
    port = input("Porti: ")
    if not port.isdigit():
        print("Porti duhet te jete numer")
        return AskPort()
    else:
        return port;  

def connect():
    global Socket
    Socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def send():
    connect()
    Socket.sendto(KERKESA.encode(),(serverName,int(port)))
    r,addr = Socket.recvfrom(1024) #kthen tuple (,) 
    r = r.decode() 
    print(r)

serverName = input("Host: ")
port = AskPort()


KomandatUsage = ["IPADRESA","NUMRIIPORTIT","BASHKETINGELLORE {nje fjali}",
            "PRINTIMI {nje fjali}","EMRIIKOMPJUTERIT","KOHA","LOJA","FIBONACCI {numer}",
            "KONVERTIMI {KilowattToHorsepower,HorsepowerToKilowatt,DegreesToRadians"+
            ",RadiansToDegrees,GallonsToLiters,LitersToGallons} {numer}","LAJMET","NUMRIITHJESHT {numer}"] 

Komandat = ["IPADRESA","NUMRIIPORTIT","BASHKETINGELLORE",
            "PRINTIMI","EMRIIKOMPJUTERIT","KOHA","LOJA","FIBONACCI",
            "KONVERTIMI","LAJMET","NUMRIITHJESHT"]

KonvertimiOptions = ["KilowattToHorsepower","HorsepowerToKilowatt",
                          "DegreesToRadians","RadiansToDegrees","GallonsToLiters",
                          "LitersToGallons"]

KERKESA = "";

def BuildKerkesa(k):
    global KERKESA
    KERKESA = k;
    if(k == "BASHKETINGELLORE" or k == "PRINTIMI"):
        fjalia = input("Shkruani nje fjali: ")
        if(fjalia.replace(" ","") == ""):
            print("######ERROR: Fjalia e zbrazet")
            BuildKerkesa(k)
        else:
            KERKESA += " " + fjalia    
    elif(k == "FIBONACCI" or k == "NUMRIITHJESHT"):
        numri = input("Shkruani nje numër: ")
        if(not numri.isdigit()):
            print("######ERROR:Parametri duhet te jete numer i plot")
            BuildKerkesa(k)
        else:
            KERKESA += " " + numri    
    elif(k == "KONVERTIMI"):
        KONVERTIMI()

def KONVERTIMI():
    global KERKESA
    for i in range(0,len(KonvertimiOptions)):
        print(str(i+1)+". "+KonvertimiOptions[i])
    
    numri = input("Shkruani nje number:")
    if((not numri.isdigit()) or (int(numri) < 1 or int(numri) > 6)):
        print("\n######ERROR:Gabim!!!\n")
        KONVERTIMI()
    else:    
        KERKESA += " " + KonvertimiOptions[int(numri)-1]
        numri = input("Shkrani cilen vler doni ta konvertoni:")    
        try:
            float(numri)
            KERKESA += " " + numri    
        except ValueError:
            print("\n######ERROR:Parametri i fundit Gabim\n")
            KONVERTIMI()
         
def TestoFloat(n):
    try:
        float(n)
        return True
    except ValueError as e:
        return False 

def VerifikoKerkesen(kerkesa):
    global KERKESA
    kerkesaArray = kerkesa.split(" ");
    funksioni = kerkesa.split(" ")[0];
    firstSpace = kerkesa.find(" ");
    if(funksioni not in Komandat):
        return False
    elif((funksioni == "BASHKETINGELLORE" or funksioni == "PRINTIMI") and (firstSpace == -1 or kerkesa[firstSpace:].replace(" ","")=="" )):
        BuildKerkesa(funksioni)
           #nese eshte konveritmi shiko a i ka 3 prarametra,         opcioni eshte i sakte,                      parametri i trete a eshte float
    elif(funksioni == "KONVERTIMI" and (len(kerkesaArray) < 3 or (kerkesaArray[1] not in KonvertimiOptions) or not TestoFloat(kerkesaArray[2]))):
        BuildKerkesa(funksioni)
    elif((funksioni == "FIBONACCI" or funksioni == "NUMRIITHJESHT") and (len(kerkesaArray)< 2 or not kerkesaArray[1].isdigit())):
        BuildKerkesa(funksioni)
    else:
        KERKESA = kerkesa    


print("\n\n\n---------UDP KLIENTI------------------\n\n\n")
print("Perdorimi: Shkruani kerkesen, ose numrin e saj\n\n")

   

for i in range(0,len(KomandatUsage)):
    print(str(i+1)+". "+KomandatUsage[i]+"\n")            



while 1:
    kerkesa = input("Shkruani kerkesen, ose numrin e saj:")
    if(kerkesa == "EXIT"):
        
        if(ConnectionAlive == 1):
            socket.close()
        print("Programi u mbylle")
        break

    elif(kerkesa.isdigit() and  (0 <= int(kerkesa) <= 11 ) ):
        BuildKerkesa(Komandat[int(kerkesa)-1])
    
    else:
        if VerifikoKerkesen(kerkesa) == False:
            print("KERKESA ESHTE GABIM")
            KERKESA = "";
            continue

    send()

