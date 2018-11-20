import sys
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches
import random

data = sys.argv[1]
allCandidates = sys.argv[2]
dataOfTheElection = open(data, "r")
outputMyAnswer = open("myAnswer.txt", "w")

votes = []  # This list holds the each candidates' total votes separately
candIndexs = []  # This list hold the candidates's index
candNameList = []  # This list holds the candidates' names
candAndVotes = {}  # This dictionary holds each candidates' name as a key and their votes as a value
retrieveList = []  # This list holds the all votes in order
twoCands = []  # This list holds the two dominant candidates
twoMaxVotes = []  # This list holds the two dominant candidates' votes
statesAndCand = {}  # This dict holds the the candidates' names as a key and their votes each states as a value
states = []  # This list holds the states, separately
list1 = []
nominees = []
percentages = []
meanlist = [0.10] * 10


def retrieveData(electionData, candidates):
    output = open("retrievedData.txt", "w")
    candidatesList = candidates.split(",")
    for i in candidatesList:
        candNameList.append(i)
    lineNum = 0
    for line in electionData.readlines():
        line = line.rstrip("\n")
        line = line.split(",")
        lineNum += 1
        if lineNum == 1:
            for i in candidatesList:
                candIndexs.append(line.index(i))
        else:
            break
    electionData.close()
    electionData = open(data, "r")
    count = 0
    for i in candIndexs:
        states.clear()
        for line in electionData.readlines():
                line = line.rstrip("\n")
                line = line.split(",")
                if not line[i].isdigit():
                    statesAndCand["%s" % line[i]] = []
                if line[i].isdigit():
                    states.append(line[0])
                    retrieveList.append(int(line[i]))
                    output.write(line[i] + " ")
                    statesAndCand[candNameList[count]].append(int(line[i]))
        count += 1
        eachCandidateVotes = sum(retrieveList) - sum(votes)
        votes.append(eachCandidateVotes)
        electionData.close()
        electionData = open(data, "r")
    electionData.close()
    for i in range(len(candIndexs)):
        a = (candNameList[i])
        candAndVotes[a] = votes[i]
    a = votes.copy()
    b = candNameList.copy()
    firstMax = max(a)
    twoMaxVotes.append(firstMax)
    firstIndex = a.index(firstMax)
    twoCands.append(b[firstIndex])
    a.remove(max(a))
    b.remove(b[firstIndex])
    secondMax = max(a)
    twoMaxVotes.append(secondMax)
    secondIndex = a.index(secondMax)
    twoCands.append(b[secondIndex])
    return retrieveList


def displayBarPlot():
    displayPdf = plt.figure(1)
    votesOfTwoCand = [statesAndCand[twoCands[0]], statesAndCand[twoCands[1]]]
    x_pos = [x for x in range(0, len(states)+1)]
    a = np.arange(len(states)+1)
    states.insert(0, "")
    plt.xticks(x_pos, states, rotation='vertical', fontsize=4)
    plt.ylabel("Vote Count")
    plt.xlabel("States")
    votesOfTwoCand[1].insert(0, 0)
    votesOfTwoCand[0].insert(0, 0)
    plt.bar(a + 0.00, votesOfTwoCand[1], align='center', color='r', width=0.25)
    plt.bar(a + 0.25, votesOfTwoCand[0], align='center', color='b', width=0.25)
    plt.xlim(0, len(states))
    red_patch = mpatches.Patch(color='red', label=twoCands[1])
    blue_patch = mpatches.Patch(color='blue', label=twoCands[0])
    plt.legend(handles=[red_patch, blue_patch])
    displayPdf.savefig("ComparativeVotes.pdf")


def CompareVoteonBar():
    comparePdf = plt.figure()
    a = sorted(list(zip(votes, candNameList)))
    a.reverse()
    perc = []
    for i in range(len(a)):
        list1.append(a[i][0])
        nominees.append(a[i][1])
    for j in list1:
        a = j*100/sum(list1)
        b = round(a, 3)
        percentages.append(b)
    for l in percentages:
        a = str(l) + " %"
        perc.append(a)
    x_pos = [x for x in range(len(nominees))]
    dist = np.arange(len(nominees))
    plt.xticks(x_pos, perc)
    plt.bar(dist + 0.00, percentages, align='center', color='r', width=0.75)
    barlist = plt.bar(dist + 0.00, percentages, align='center', color='r', width=0.75)

    colors = "rbycmgkw"
    colors_index = 0
    listofpatches = []
    for k in nominees:
        patch = mpatches.Patch(color=colors[colors_index], label=k)
        listofpatches.append(patch)
        barlist[colors_index].set_color(colors[colors_index])
        colors_index += 1

    plt.legend(handles=listofpatches)
    plt.xlabel("Nominess")
    plt.ylabel("Vote Percentages")
    comparePdf.savefig("CompVotePercs.pdf")


def obtainHistogram(samplelist):
    freq = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in samplelist:
        if i <= 9:
            freq[0] += 1
            freq[i] += 1
        else:
            ones = i % 10
            tens = (i // 10) % 10
            freq[ones] += 1
            freq[tens] += 1
    count = 0
    for j in freq:
        freq[count] = j / (len(samplelist) * 2)
        count += 1
    return freq


def plotHistogram(freqlist):
    histPdf = plt.figure()
    mean, = plt.plot(meanlist, label="Mean", linestyle="--", color="g")
    digitdist, = plt.plot(freqlist, label="Digit Dist.", linewidth=1, color="r")
    plt.legend(handles=[mean, digitdist], loc=1)
    plt.title("Histogram of least sign. digits")
    plt.xlabel("Digits")
    plt.ylabel("Distribution")
    histPdf.savefig("Histogram.pdf")


def plotHistogramWithSample():
    ten = []
    for i in range(10):
        ten.append(random.randrange(100))
    tens = obtainHistogram(ten)
    hist1Pdf = plt.figure()
    mean, = plt.plot(meanlist, label="Mean", linestyle="--", color="g")
    digitdist, = plt.plot(tens, label="Digit Dist.", linewidth=1, color="r")
    plt.legend(handles=[mean, digitdist], loc=2)
    plt.title("Histogram of least sign. digits - Sample:1")
    plt.xlabel("Digits")
    plt.ylabel("Distribution")
    hist1Pdf.savefig("HistogramofSample1.pdf")

    fifty = []
    for j in range(50):
        fifty.append(random.randrange(100))
    fiftys = obtainHistogram(fifty)
    hist2Pdf = plt.figure()
    mean, = plt.plot(meanlist, label="Mean", linestyle="--", color="g")
    digitdist, = plt.plot(fiftys, label="Digit Dist.", linewidth=1, color="b")
    plt.legend(handles=[mean, digitdist], loc=2)
    plt.title("Histogram of least sign. digits - Sample:2")
    plt.xlabel("Digits")
    plt.ylabel("Distribution")
    hist2Pdf.savefig("HistogramofSample2.pdf")

    hundred = []
    for k in range(100):
        hundred.append(random.randrange(100))
    hundreds = obtainHistogram(hundred)
    hist3Pdf = plt.figure()
    mean, = plt.plot(meanlist, label="Mean", linestyle="--", color="g")
    digitdist, = plt.plot(hundreds, label="Digit Dist.", linewidth=1, color="y")
    plt.legend(handles=[mean, digitdist], loc=2)
    plt.title("Histogram of least sign. digits - Sample:3")
    plt.xlabel("Digits")
    plt.ylabel("Distribution")
    hist3Pdf.savefig("HistogramofSample3.pdf")

    thousand = []
    for k in range(1000):
        thousand.append(random.randrange(100))
    thousands = obtainHistogram(thousand)
    hist4Pdf = plt.figure()
    mean, = plt.plot(meanlist, label="Mean", linestyle="--", color="g")
    digitdist, = plt.plot(thousands, label="Digit Dist.", linewidth=1, color="c")
    plt.legend(handles=[mean, digitdist], loc=2)
    plt.title("Histogram of least sign. digits - Sample:4")
    plt.xlabel("Digits")
    plt.ylabel("Distribution")
    hist4Pdf.savefig("HistogramofSample4.pdf")

    tenthousand = []
    for k in range(10000):
        tenthousand.append(random.randrange(100))
    tenthousands = obtainHistogram(tenthousand)
    hist5Pdf = plt.figure()
    mean, = plt.plot(meanlist, label="Mean", linestyle="--", color="g")
    digitdist, = plt.plot(tenthousands, label="Digit Dist.", linewidth=1, color="k")
    plt.legend(handles=[mean, digitdist], loc=2)
    plt.title("Histogram of least sign. digits - Sample 5")
    plt.xlabel("Digits")
    plt.ylabel("Distribution")
    hist5Pdf.savefig("HistogramofSample5.pdf")


def calculateMSE(list1, list2):
    mse = 0
    for i in range(len(list1)):
        mse += ((list1[i]-list2[i])**2)
    return mse


def compareMSEs(mseofusa):
    smallermse = 0
    for i in range(10000):
        mselist = []
        for j in range(204):
            mselist.append(random.randrange(100))
        if mseofusa >= calculateMSE(obtainHistogram(mselist), meanlist):
            smallermse += 1
        mselist.clear()
    greatermse = 10000 - smallermse
    pvalue = smallermse / 10000
    mseofusa = str(mseofusa)
    print("MSE value of 2012 USA election is " + mseofusa)
    outputMyAnswer.write("MSE value of 2012 USA election is " + str(mseofusa) + "\n")
    print("The number of MSE of random samples which are larger than or equal to USA election MSE is "+str(greatermse))
    outputMyAnswer.write("The number of MSE of random samples which are larger than or equal to USA election MSE is "+str(greatermse) + "\n")
    print("The number of MSE of random samples which are smaller than or equal to USA election MSE is "+str(smallermse))
    outputMyAnswer.write("The number of MSE of random samples which are smaller than or equal to USA election MSE is "+str(smallermse) + "\n")
    print("2012 USA election rejection level p is " + str(pvalue))
    outputMyAnswer.write("2012 USA election rejection level p is " + str(pvalue) + "\n")
    if pvalue < 5/100:
        print("Finding: We reject the null hypothesis at the p= " + str(pvalue) + " level")
        outputMyAnswer.write("Finding: We reject the null hypothesis at the p= " + str(pvalue) + " level\n")
    else:
        print("Finding: There is no statistical evidence to reject null hypothesis")
        outputMyAnswer.write("Finding: There is no statistical evidence to reject null hypothesis\n")


retrieveData(dataOfTheElection, allCandidates)
displayBarPlot()
CompareVoteonBar()
plotHistogram(obtainHistogram(retrieveList))
plotHistogramWithSample()
compareMSEs(calculateMSE(obtainHistogram(retrieveList), meanlist))
