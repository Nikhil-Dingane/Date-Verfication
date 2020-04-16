#! python3
import csv,datetime,os,sys

# input file
csvinputfile=open(sys.argv[1])
csvinputfilereader=csv.DictReader(csvinputfile)
csvinputfiledata=list(csvinputfilereader)

# output file
csvoutputfile=open(sys.argv[2])
csvoutputfilereader=csv.DictReader(csvoutputfile)
csvoutputfilefiledata=list(csvoutputfilereader)

#result file name
resultfilename="result_"+(str(datetime.datetime.now())).replace(" ","_")

#result file
resultfile=open(resultfilename,'w')
resulfilewriter=csv.writer(resultfile)

#header
resultheaders=list(csv.reader(open(sys.argv[2])))[0]

#new field added
resultheaders.append("Comment")
resulfilewriter.writerow(resultheaders)

# mappingfile
csvmappingreader=csv.reader(open(sys.argv[3]))
csvmappingdata=list(csvmappingreader)

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
    for j in range(0,len(csvmappingdata)):
        newrow.append(row[csvmappingdata[j][1]])
        if csvinputfiledata[index][csvmappingdata[j][0]]!=row[csvmappingdata[j][1]]:
            flag=False
            comment=comment+" "+csvmappingdata[j][1]
    if flag==True:
        newrow.append("Matched")
    else:
        newrow.append("Not matched : "+comment)
    resulfilewriter.writerow(newrow)
    
    
#os.system("rm "+resultfilename)