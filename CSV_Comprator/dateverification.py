#! python3
from datetime import datetime
import csv,os,sys,platform

def clearScreen():
    if platform.system()=="Linux":
        os.system("clear")
    elif platform.system()=="Windows":
        os.system("cls")

def getFile(printtext):
    while(True):
        clearScreen();
        print(printtext)
        validfilename=input()
        if os.path.isfile(validfilename):
            return validfilename;
        print("\nThere is no file : "+validfilename+"\n\nPlease enter valid path!!")
        print("\nPress any key to continue....")
        input()


def main():
    inputfilename=getFile("Enter input file:")
    outputfilename=getFile("Enter output file:")
    mappingfilename=getFile("Enter mapping file:")
    clearScreen()

    print("Files are set as below:")
    print("\nInput file name: "+ inputfilename)
    print("\nOutput file name: "+ outputfilename)
    print("\nMapping file name: "+ mappingfilename)
    
    print("\nPress any key to continue...\n")
    input()
    clearScreen()
    
    # input file
    csvinputfile=open(inputfilename)
    csvinputfilereader=csv.DictReader(csvinputfile)
    csvinputfiledata=list(csvinputfilereader)

    # output file
    csvoutputfile=open(outputfilename)
    csvoutputfilereader=csv.DictReader(csvoutputfile)
    csvoutputfilefiledata=list(csvoutputfilereader)

    # mappingfile
    csvmappingreader=csv.reader(open(mappingfilename))
    csvmappingdata=list(csvmappingreader)
    
    for i in range(1, len(csvmappingdata)):
        try:
            csvinputfiledata[1][csvmappingdata[i][0]]
        except:
            print('"'+csvmappingdata[i][0]+'"'+" this field is not in "+'"'+inputfilename+'"'+" file.\n\nPlease check your mapping file : "+'"'+mappingfilename+'"')
            print("\nPress any key to continue...")
            input()
            return
        try:
            csvoutputfilefiledata[1][csvmappingdata[i][1]]
        except:
            print('"'+csvmappingdata[i][1]+'"'+" this field is not in "+'"'+outputfilename+'"'+" file.\nPlease check your mapping file : "+'"'+mappingfilename+'"')
            print("\nPress any key to continue...")
            input()
            return
        
    
    #result file name
    currentTime=datetime.now()
    d=datetime.strptime(str(currentTime.hour)+":"+str(currentTime.minute)+":"+str(currentTime.second),"%H:%M:%S")
    time_stamp=d.strftime("%I_%M_%S_%p")
    resultfilename="result_"+str(currentTime.date())+"_"+time_stamp+".csv"


    #result file
    resultfile=open(resultfilename,'w')
    resulfilewriter=csv.writer(resultfile)

    #header
    resultheaders=list(csv.reader(open(outputfilename)))[0]

    #new field added
    resultheaders.append("Comment")
    resulfilewriter.writerow(resultheaders)

    

    # unique keys within input file
    keys=[]
    for i in csvmappingdata:
        if i[2]=="yes":
            keys.append(i[0])

    # dictionary to keep mapping between unique key and its row number
    inputFileDictionary={}
    #making dictionary of input file
    for i in range(0,len(csvinputfiledata)):
        key=""
        for keyfield in keys:
            key=key+csvinputfiledata[i][keyfield]
        inputFileDictionary[key]=i

    # unique keys list within output file
    outputkeys=[]
    for i in csvmappingdata:
        if i[2]=="yes":
            outputkeys.append(i[1])

    # reading output file row by row
    for row in csvoutputfilefiledata:
        # key to be mapped within input file key and row number dictionary 
        searchkey=""
        for keyfield in outputkeys:
            searchkey=searchkey+row[keyfield]
        try:
            index=inputFileDictionary[str(searchkey)]
        except KeyError:
            index=-1;
        newrow=[]
        flag=True
        comment=""
        for j in range(1,len(csvmappingdata)):
            newrow.append(row[csvmappingdata[j][1]])
            # print(csvinputfiledata[index][csvmappingdata[j][0]]+" = "+row[csvmappingdata[j][1]])
            if csvinputfiledata[index][csvmappingdata[j][0]]!=row[csvmappingdata[j][1]]:
                flag=False
                if csvmappingdata[j][2]!="yes":

                    comment=comment+csvmappingdata[j][1]+", "
        if flag==True:
            newrow.append("Matched")
        else:
            newrow.append("Not matched : "+comment)
        resulfilewriter.writerow(newrow)
    print("Result file is successfully saved as :"+resultfilename)
    print("\nPress any key to continue...")
    input()
    #os.system("rm "+resultfilename)

while(True):
    clearScreen()
    print("1) Compare CSV files.")
    print("0) Exit")
    print("\nPlease enter your choice:")
    choice=input()
    if choice=="1":
        main()
    elif choice == "0":
        exit()
    else:
        print("\n\nInvalid choice!!!")
        print("\nPress any key to continue...")
        input()
