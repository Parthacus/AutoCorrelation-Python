class points:
    data = 0
    timepoint = 0
    deviation = 0

    def calculateDeviation(self, average):
        self.deviation = self.data - average

    def calculateNumerator(self, lagtime, timepoints):
        return self.deviation * (timepoints[self.timepoint + lagtime].deviation)

    def calculateDenominator(self):
        return self.deviation ** 2

def readData(location):
    return open(location).read()

def returnDataList(data, delimiter):
    return list(filter(None, data.split(delimiter)))

def convertToInt(data):
    return list(map(int, data))

def getDataLength(data):
    return len(data)

def convertToObjects(data, length):
    objects = []
    for i in range(0, length):
        point = points()
        point.data = data[i]
        point.timepoint = i
        objects.append(point)
    return objects

def calculateAverage(timepoints):
    total = 0
    length = 0
    for point in timepoints:
        total += point.data
        length += 1
    return total/length

def calculateDeviation(timepoints, avg):
    for point in timepoints:
        point.calculateDeviation(avg)

def drawLineGraph(data, title):
    import matplotlib.pyplot as plt
    plt.title(title)
    plt.plot(data)
    plt.show()

def autocorrelateAtLagtime(timepoints, length, lag):
    numerator = 0
    denominator = 0
    for i in range(length - lag):
        numerator += timepoints[i].calculateNumerator(lag, timepoints)
        denominator += timepoints[i].calculateDenominator()
    return numerator/denominator

DATA = convertToInt(returnDataList(readData('timeseriesdata.txt'), '\n'))
LENGTH = getDataLength(DATA)
TIMEPOINTS = convertToObjects(DATA, LENGTH)
AVG = calculateAverage(TIMEPOINTS)
calculateDeviation(TIMEPOINTS, AVG)

results = []
for LAG in range(0, LENGTH - 1):
    results.append(autocorrelateAtLagtime(TIMEPOINTS, LENGTH, LAG))

drawLineGraph(results, 'coefficient vs lagtime')
