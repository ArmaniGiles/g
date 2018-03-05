import time
from os import walk
from time import gmtime, strftime
from datetime import date, datetime


count = 0

def makeCVS(data): 
    import csv
    global count 
    Header =  [["Traffic_Type","Message Size (bytes)","Measure Rate (msps)","Time between messages","Msg1","Msg2","Design rate","Design size"]]
    print("data",data)
    with open('Result.csv', 'a') as csv_file:
        writer = csv.writer(csv_file)
        ##for key, value in data.items():
        print("A")
        if count == 0:
            print("B")
            writer.writerows(Header)
            count = count + 1
        
        print("data", data)
        writer.writerows(data)
        #writer.writerow([key, value])
    print("Completed It")


f = [ ]

for (dirpath, dirnames, filenames) in walk("./Get_the_Traffic_Size_Folder"):
    f.extend(filenames)
    break
inputFilePointer = []
for (dirpath, dirnames, filenames) in walk("./Input"):
    #print(filenames)
    print("AA")
    
    inputFilePointer.extend(filenames)
    #print(filenames)

    break
A= []
for i in  inputFilePointer:
    if "send" in i:
        A.append(i)

    

def getAvgofTrafficMessagePeriod(f):

    RecMList, SendMList,  =  [], []
    designRate = []
    table = [] 
    d,b,c =0,0,0
    for i in range( len(f)):
        temp_File = open("./Get_the_Traffic_Size_Folder"+"/"+f[i],"r")
        input_File = open("./Input"+"/"+A[i],"r") # Comment out here to 
    
        dummy  = input_File.readline() 

        for i in dummy.split():
            if "[" in i:
                c=i[1:]
                print(c)
            elif "]" in i:
                b = i[:-1]
                print(b)
                #d=b/c
        #exit(0)                                # To here and run the code and see what happens 
               
        
       
        RecMList=[datetime.strptime(line[:15], '%H:%M:%S.%f').strftime('%H:%M:%S.%f') for line in temp_File for word in line.split()  if  "RECV" in word ]
        temp_File.seek(0)
        SendMList = [datetime.strptime(word[5:], '%H:%M:%S.%f').strftime('%H:%M:%S.%f') for line in temp_File for word in line.split() if "sent>" in word]
        temp_File.seek(0)

        # import numpy as np
        # x = datetime.strptime("00:00:00.000000", '%H:%M:%S.%f') 
        # sumOfRecList = abs(RecMList[0]- RecMList[len(RecMList)-1]) # Taking the Average of time 
        # for i in range(0,len(RecMList) ):
        #     print(RecMList[i])
        #     x = RecMList[i]  - x
        # print(x)
        # exit(0)

        
        #designRate = [for line in Input_File for word in line if word is "["  ]

        AverageSize = [int(word[5:]) for line in temp_File for word in line.split() if "size>" in word]
        
        Msg1 = RecMList[0]
        Msg2 = RecMList[1]
        #lastMsg = RecMList[len(RecMList)-1]

        R = [int(i[-6:]) for i in RecMList] 
        S = [int(i[-6:]) for i in SendMList]
        # print("R is ",R)
        # print("S is ", S)
        #exit(0)

        getDiffFromRandS = [abs(round((x-y)/1000000,4) ) for x, y in zip(R, S)]     
       
        import numpy as np
        import math
        AverageSize = math.ceil(np.mean(AverageSize))
        
        mean = round(np.mean(getDiffFromRandS),4)
        
        msgpersec= 10**len(str(mean)[2:])

        table.extend((f[i],AverageSize,msgpersec, mean,Msg1,Msg2))
        print("Table:",table)

        makeCVS([table])
        table = []
                    
    return table

getAvgofTrafficMessagePeriod(f)