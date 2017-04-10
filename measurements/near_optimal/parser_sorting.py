#!/usr/bin/env python
import re
import sys
import itertools
import csv
import operator

def split_list(alist, wanted_parts=1):
    length = len(alist)
    return [ alist[i*length // wanted_parts: (i+1)*length // wanted_parts] 
             for i in range(wanted_parts) ]

def csv_writer(rs, param):
    #for fileType in xrange(0, 6):
    flag = True
    for fr in xrange(0, 16):
        transponed = map\
            (list, zip(*rs[fr]))
        #print transponed
        if flag:
            header = list(transponed[0])

            header.append('FR')

            toWrite = split_list(header, wanted_parts=1)

            values = list(transponed[1])
            print(values)
            values.append(transponed[2][0])
            toWrite.append(values)
        else:
            toWrite = list(transponed[1])
            toWrite.append(transponed[2][0])
        #with open('csv/pbzip2_'+transponed[0][0]+'_'+param+'_compress.csv', 'ab') as result:
        with open('test_'+param+"_"+sys.argv[1][:5] +"_"+sys.argv[1][-10:], 'ab') as result:
            if flag:
                writer = csv.writer(result, dialect='excel')
                writer.writerows(toWrite)
                flag = False
            else:
                writer = csv.writer(result, dialect='excel')
                writer.writerow(toWrite)


#content = open("../log_pbzip2_compress", "r")
# regexThread = re.compile(r'p(\d+)\s\/.*\/.*\/.*\/(.*)\"')
# regexTime = re.compile(r'\d+:\d{2}.\d{2}')
# regexMemory = re.compile(r'Maximum.*\:\s(\d+)')
# regexSize = re.compile(r'^\d+$')
# regexFrequency = re.compile(r'userspace (\d+) MHz')
# regexFixName = re.compile(r'(.*).tar')

# contentWatts = open("../log_pbzip2_compress_watts", "r")
# regexWatts = re.compile(r'Average: (\d+.\d+) watts')
# regexJoules = re.compile(r'Energy: (\d+.\d+) joule')

realTimes = []
threads = []
# fileNames = []
# peakMemory = []
# fileSizes = []
frequencies = []
freqNum = 0
# initialSizes = [[408361984]*6, [124204544]*6, [211723776]*6, [100000000]*6, [1000000000]*6, [700765696]*6]
# from itertools import chain
# initialSizes = list(chain.from_iterable(initialSizes))

starts = 0
energies = 0

joules = []


content = csv.reader(open(sys.argv[1]))
content = sorted(content, key=operator.itemgetter(0,4))
#print content
for line in content:

    frequencies.append(float(line[0]))
    freqNum += 1
    realTimes.append(float(line[1]))
    joules.append(float(line[2]))
    threads.append(float(line[4]))


    # threadAndFilename = regexThread.findall(line)
    # #print(threadAndFilename)
    # times = regexTime.findall(line)
    # freq = regexFrequency.findall(line)
    # dirtyPeakMemory = regexMemory.findall(line)
    # dirtyFileSizes = regexSize.findall(line)
    # for peak in dirtyPeakMemory:
    #     if peak:
    #         peakMemory.append(float(peak))
    # for word in threadAndFilename:
    #     threads.append(int(word[0]))
    #     if(word[1] != "enwik8" and word[1] != "enwik9"):
    #         fileNames.append(regexFixName.findall(word[1])[0])
    #         starts += 1
    #     else:
    #         fileNames.append(word[1])
    #         starts += 1
    # for time in times:
    #     if time:
    #         realTimes.append(time)
    # for fileSize in dirtyFileSizes:
    #     if fileSize:
    #         fileSizes.append(float(fileSize))
    # for f in freq:
    #     if f:
    #         frequencies.append(float(f))
    #         freqNum += 1

#
# watts = []
# joules = []
# for line in contentWatts:
#     dirtyWatts = regexWatts.findall(line)
#     dirtyJoules = regexJoules.findall(line)
#     for w in dirtyWatts:
#         if w:
#             watts.append(float(w))
#     for j in dirtyJoules:
#         if j:
#             joules.append(float(j))
#             energies +=1

print starts
print energies
#print "freqNum" + str(freqNum)
#print split_list(realTimes, wanted_parts=24)

# seconds = []
# regexMinsAndSecs = re.compile(r'(\d+):(\d+.\d+)')
# for line in realTimes:
#     minsAndSecs = regexMinsAndSecs.findall(line)
#     for t in minsAndSecs:
#         seconds.append(float(t[0])*60+float(t[1]))

splitTimes = split_list(realTimes, wanted_parts=freqNum/10) #*10
splitThreads = split_list(threads, wanted_parts=freqNum/10) #*10
# splitNames = split_list(fileNames, wanted_parts=freqNum/360*6*6) #*10
# splitPeaks = split_list(peakMemory, wanted_parts=freqNum/360*6*6) #*10
# splitSizes = split_list(fileSizes, wanted_parts=freqNum/360*6*6) #*10
splitFreqs = split_list(frequencies, wanted_parts=freqNum/10) #*10

#splitWatts =  split_list(watts, wanted_parts=freqNum/360*6*6) #*10
splitJoules =  split_list(joules, wanted_parts=freqNum/10) #*10
#print splitFreqs
print len(splitTimes)
#print(splitFreqs)

avgTimes = []
threadNumber = []
# names = []
# peaks = []
# sizes = []
freqs = []
# avgWatts = []
avgJoules = []

for time in splitTimes:
    avgTimes.append(round(sum(time)/len(time), 2))
    #avgTimes.append(round(float(time[0]), 2))
for tr in splitThreads:
    threadNumber.append(tr[0])
# for n in splitNames:
#     names.append(n[0])
# for p in splitPeaks:
#     peaks.append(round(sum(p)/len(p), 2))
#     #peaks.append(round(float(p[0]),2))
# for s in splitSizes:
#     sizes.append(round(sum(s)/len(s), 2))
#     #sizes.append(round(float(s[0]),2))
for f in splitFreqs:
    freqs.append(round(sum(f)/len(f), 2))
    #freqs.append(round(float(f[0]),2))
# for w in splitWatts:
#     avgWatts.append(round(sum(w)/len(w), 2))
    #avgWatts.append(round(float(w[0]),2))
for j in splitJoules:
    avgJoules.append(round(sum(j)/len(j), 2))
    #avgJoules.append(round(float(j[0]),2))
print len(avgTimes)

#compression_ratios = [round(float(initSize)/float(size), 2) for initSize, size in zip(initialSizes*freqNum, sizes)]

#ratio_time = [float(rat)/float(time) for rat, time in zip(compression_ratios, avgTimes)]

resultSet = zip(threadNumber, avgTimes, freqs, avgJoules)

resultSetTime = zip(threadNumber, avgTimes, freqs)
# resultSetMem = zip(names, threadNumber, peaks, freqs)
# resultSetSize = zip(names, threadNumber, sizes, freqs)
# resultSetRatio = zip(names, threadNumber,compression_ratios, freqs)
# resultSetRT = zip(names, threadNumber,ratio_time, freqs)
# resultSetWatts = zip(names, threadNumber,avgWatts, freqs)
resultSetJoules = zip(threadNumber,avgJoules, freqs)


resultSetTime = sorted(resultSetTime, key=operator.itemgetter(2,int(0)))
# resultSetMem = sorted(resultSetMem, key=operator.itemgetter(0,3))
# resultSetSize = sorted(resultSetSize, key=operator.itemgetter(0,3))
# resultSetRatio = sorted(resultSetRatio, key=operator.itemgetter(0,3))
# resultSetRT = sorted(resultSetRT, key=operator.itemgetter(0,3))
# resultSetWatts = sorted(resultSetWatts, key=operator.itemgetter(0,3))
resultSetJoules = sorted(resultSetJoules, key=operator.itemgetter(2,int(0)))


# resultSetTime = split_list(resultSetTime, wanted_parts=6)
# resultSetMem = split_list(resultSetMem, wanted_parts=6)
# resultSetSize = split_list(resultSetSize, wanted_parts=6)
# resultSetRatio = split_list(resultSetRatio, wanted_parts=6)
# resultSetRT = split_list(resultSetRT, wanted_parts=6)
# resultSetWatts = split_list(resultSetWatts, wanted_parts=6)
# resultSetJoules = split_list(resultSetJoules, wanted_parts=6)

resultSetTime = split_list(resultSetTime, wanted_parts=16)
# resultSetMem = split_list(resultSetMem, wanted_parts=6)
# resultSetSize = split_list(resultSetSize, wanted_parts=6)
# resultSetRatio = split_list(resultSetRatio, wanted_parts=6)
# resultSetRT = split_list(resultSetRT, wanted_parts=6)
# resultSetWatts = split_list(resultSetWatts, wanted_parts=6)
resultSetJoules = split_list(resultSetJoules, wanted_parts=16)


#for fileType in xrange(0, 6):
    # resultSetTime[fileType][0] = split_list( resultSetTime[fileType][0], wanted_parts=16)
    # resultSetMem[fileType][0] = split_list(resultSetMem[fileType][0], wanted_parts=16)
    # resultSetSize[fileType][0] = split_list(resultSetSize[fileType][0], wanted_parts=16)
    # resultSetRatio[fileType][0] = split_list(resultSetRatio[fileType][0], wanted_parts=16)
    # resultSetRT[fileType][0] = split_list(resultSetRT[fileType][0], wanted_parts=16)
    # resultSetWatts[fileType][0] = split_list(resultSetWatts[fileType][0], wanted_parts=16)
    # resultSetJoules[fileType][0] = split_list(resultSetJoules[fileType][0], wanted_parts=16)

#print resultSetTime

csv_writer(resultSetTime, 'time')
#csv_writer(resultSetMem, 'memory')
#csv_writer(resultSetSize, 'size')
#csv_writer(resultSetRatio, 'ratio')
#csv_writer(resultSetRT, 'ratio_time')
#csv_writer(resultSetWatts, 'power')
csv_writer(resultSetJoules, 'energy')


header = [("Name","TR","TIM","MEM","SIZ","RAT","RT","FR","POW","EN")]

resultSet = header + resultSet

#print(resultSet)

# with open('pbzip2_compress.csv', 'wb') as result:
#     writer = csv.writer(result, dialect='excel')
#     writer.writerows(resultSet)


'''
f = open('pbzip2_compress', 'w')
print(resultSet, file = f)
'''
'''
for i in xrange(0, 6):
    currentFileType = resultSet[i*4:(i*4)+4]
    fileName = currentFileType[0][0]
    f = open("Rscript" , "a")
    #f.write(fileName+ "_pbzip2_time_compress <- c(" + str(currentFileType[0][2])+", "+str(currentFileType[1][2])+", "+str(currentFileType[2][2])+", "+str(currentFileType[3][2])+")\n")
    #f.write(fileName + "_pbzip2_memory_compress <- c(" + str(currentFileType[0][3])+", "+str(currentFileType[1][3])+", "+str(currentFileType[2][3])+", "+str(currentFileType[3][3])+")\n")
    #f.write(fileName +"_pbzip2_size_compress <- c(" + str(currentFileType[0][4])+", "+str(currentFileType[1][4])+", "+str(currentFileType[2][4])+", "+str(currentFileType[3][4])+")\n")
    #f.write(fileName +"_pbzip2_compression_ratio <- c(" + str(currentFileType[0][5])+", "+str(currentFileType[1][5])+", "+str(currentFileType[2][5])+", "+str(currentFileType[3][5])+")\n")
    f.write(fileName +"_pbzip2_ratio_time <- c(" + str(currentFileType[0][6])+", "+str(currentFileType[1][6])+", "+str(currentFileType[2][6])+", "+str(currentFileType[3][6])+")\n")
'''
'''
for i in xrange(0, 6):
    currentFileType = resultSet[i*4:(i*4)+4]
    fileName = currentFileType[0][0]
    if currentFileType[0][0] != "enwik9" and currentFileType[0][0] != "enwik8":
        fileNameWithoutTar = currentFileType[0][0][:-4]
    else:
	fileNameWithoutTar = currentFileType[0][0]
    f = open("Rscript" , "a")
    #f.write(fileName+ "_pbzip2_time_compress <- c(" + str(currentFileType[0][2])+", "+str(currentFileType[1][2])+", "+str(currentFileType[2][2])+", "+str(currentFileType[3][2])+")\n")
    #f.write(fileName + "_pbzip2_memory_compress <- c(" + str(currentFileType[0][3])+", "+str(currentFileType[1][3])+", "+str(currentFileType[2][3])+", "+str(currentFileType[3][3])+")\n")
    #f.write(fileName +"_pbzip2_size_compress <- c(" + str(currentFileType[0][4])+", "+str(currentFileType[1][4])+", "+str(currentFileType[2][4])+", "+str(currentFileType[3][4])+")\n")
    #f.write("plot("+fileName+"_pbzip2_time_compress, main=\"" + fileNameWithoutTar + " compress\", xlab=\"Number of threads\", ylab=\"time, s\", ylim="+fileNameWithoutTar+"_compress_time_g_range, col=\"red\", type=\"o\")\ndev.out()\n")
    #f.write("plot("+fileName+"_pbzip2_memory_compress, main=\"" + fileNameWithoutTar + " compress\", xlab=\"Number of threads\", ylab=\"Peak memory, KBytes\", ylim="+fileNameWithoutTar+"_compress_memory_g_range, col=\"red\", type=\"o\")\ndev.out()\n")
    #f.write("plot("+fileName+"_pbzip2_size_compress, main=\"" + fileNameWithoutTar + " compress\", xlab=\"Number of threads\", ylab=\"Size, Bytes\", ylim="+fileNameWithoutTar+"_compress_size_g_range, col=\"red\", type=\"o\")\ndev.out()\n")
    #f.write("png('"+fileName+".png')\nplot("+fileName+"_pbzip2_compression_ratio, main=\"" + fileNameWithoutTar + " compression ratio\", xlab=\"Number of threads\", ylab=\"Ratio, number of times\", ylim="+fileNameWithoutTar+"_compression_ratio_g_range, col=\"red\", type=\"o\")\ndev.off()\n")
    f.write("png('"+fileName+"_pbzip2_ratio_time.png')\nplot( threads, "+fileName+"_pbzip2_ratio_time, main=\"" + fileNameWithoutTar + " compression ratio\", xlab=\"Number of threads\", ylab=\"Ratio/time, times/s\", ylim="+fileNameWithoutTar+"_ratio_time_g_range, col=\"red\", type=\"o\", xaxt = \"n\")\ndev.off()\n")
'''
