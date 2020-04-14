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

for i in range(0,len(csvinputfiledata)):
    newrow=[]
    flag=True
    comment=""
    for j in range(0,len(csvmappingdata)):
        newrow.append(csvoutputfilefiledata[i][csvmappingdata[j][1]])
        if csvinputfiledata[i][csvmappingdata[j][0]]==csvoutputfilefiledata[i][csvmappingdata[j][1]]:
            print("matched")
        else:
            flag=False
            comment=comment+" "+csvmappingdata[j][1]
            print("unmatched")
    if flag==True:
        newrow.append("Matched")
    else:
        newrow.append("Not matched : "+comment)
    resulfilewriter.writerow(newrow)
