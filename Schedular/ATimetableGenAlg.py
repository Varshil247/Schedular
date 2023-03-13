import json
from random import choices, randint, randrange, random
import time
from unittest import result

from numpy import int0

path = r'C:\Users\Varshil Patel\OneDrive - Loughborough College\Computer Science\2. NEA CODE\SchedularVa\timetableConfig.json'
#path = r'C:\Users\258488\OneDrive - Loughborough College\Computer Science\2. NEA CODE\Schedular_py\GenAlgTimetable\data.json'

##!create another variable for classrooms
##!evaluate this in the fitness function that the teacher cannot teach 2 classes in 2 different rooms at one time

##!for number of students just create array showing the class room and number of student that can go into that classroom

class geneticAlg:
    def __init__(self):
        self.data = {}
        self.result = []
        self.clashes = 0
        self.accuracy = 0
        self.completionTime = 0
        
        self.finalData = []

        with open(path) as file:
            self.data = json.load(file)["config"]

        self.rooms = self.data['rooms']
        self.faculty = self.data['teachers']
        self.days = [1,2,3,4,5]
        self.periods = [1,2,3,4,5]

        self.scheduleSize = len(self.days)*len(self.periods)
        self.timetableSize = len(self.rooms)
        self.populationSize = 10    
        self.genLim = 100

        if len(self.rooms) >= 2 or len(self.faculty) >= 2:
            self.runEvolution()

    def generateGenome(self):
        genome = []
        for i in(self.faculty, self.days, self.periods):
            gene = format(randint(1,len(i)), f'0{(len((format(len(i)),"b")))}b')
            genome.append(gene)
        self.genomeLen = len(genome)
        return genome

    def generateRoomSchedule(self, scheduleSize):
        return[self.generateGenome() for _ in range(scheduleSize)]
        
    def generateTimetable(self, scheduleSize, timetableSize):
        return[self.generateRoomSchedule(scheduleSize) for _ in range(timetableSize)]

    def generatePopulation(self, scheduleSize, timetableSize, popuSize):
        return[self.generateTimetable(scheduleSize, timetableSize) for _ in range(popuSize)]


    def fitness(self, timetable):
        clash = 0
        #x = roomschedule
        for x in range(len(timetable)):
            #y = lesson genome
            for y in range(len(timetable[x])):
                #print(timetable[x][y])
                #print('\n')
                if timetable[x].count(timetable[x][y]) > 1:
                    clash+=1
                #if timetable[x][y].count(timetable[x][y][2]) > 1 and timetable[x][y].count(timetable[x][y][3]) > 1:
                if timetable[x][y].count(timetable[x][y][1]) > 1 and timetable[x][y].count(timetable[x][y][2]) > 1:
                    clash+=1
                    
        #print(clash)
        return clash
    

    def selection(self, Population, fitness):
        return choices(
            population = Population,
            weights=[fitness(timetable) for timetable in Population],
            k=2
        )


    def crossover(self, timetableA, timetableB):
        if len(timetableA) != len(timetableB):
            raise ValueError('genome A and genome B are not the same length')
        
        if len(timetableA) < 2:
            return timetableA, timetableB
         
        position = randint(1, len(timetableA)-1)
        return timetableA[0:position] + timetableB[position:], timetableB[0:position] + timetableA[position:]


    def mutation(self, timetable):
        for _ in range(1):
            roomIndex = randrange(len(timetable))
            geneIndex = randrange(len(timetable[roomIndex]))
            valueIndex = randrange(len(timetable[roomIndex][geneIndex]))
            if random() > 0.5:
                timetable[roomIndex] = timetable[roomIndex]
            else:
                timetableListGeneIndexed = abs(int(timetable[roomIndex][geneIndex][valueIndex])-1)
            return timetable


    def genome_to_data(self, roomSchedule):
        result = []
        for lesson in range(len(roomSchedule)):
            result.append([])
            geneIndex = 0
            #for j in(self.subjects, self.faculty, self.days, self.periods):
            for j in(self.faculty, self.days, self.periods):
                gene = roomSchedule[lesson][geneIndex]
                if int(gene,2) != 0: 
                    if j == self.periods:
                        val = j[int(gene,2)-2]
                    else:
                        val = j[int(gene,2)-1]
                else:
                    val = j[randint(0,len(j))-1]
                result[lesson].append(val)
                geneIndex+=1
        return result


    def evolution(self):
        population = self.generatePopulation(scheduleSize=self.scheduleSize, timetableSize=self.timetableSize, popuSize=self.populationSize)
        for genNum in range(self.genLim):
            population = sorted(
                population,
                key=lambda timetable: self.fitness(timetable=timetable),
                reverse=False
            )
    
            if self.fitness(timetable=population[0]) == self.fitness:
                break

            nextGen = population[0:2]
            for j in range(int(len(population)/2)-1):
                parents = self.selection(population, self.fitness)
                offspring_a, offspring_b = self.crossover(parents[0], parents[1])
                offspring_a = self.mutation(offspring_a)
                offspring_b = self.mutation(offspring_b)
                nextGen += [offspring_a, offspring_b]

            population = nextGen

        population = sorted(
            population,
            key=lambda timetable: self.fitness(timetable=timetable),
            reverse=False,
        )
        return population, genNum


    def sortLessonSchedule(self, lesson):
        #lessonDay = int(lesson[2])
        #lessonPeriod = int(lesson[3])
        lessonDay = int(lesson[1])
        lessonPeriod = int(lesson[2])
        noPeriods = len(self.periods)

        #equation = 5n-4, to get first period of each day
        lessonNumber = (noPeriods*(lessonDay) - (noPeriods-1)) + lessonPeriod
        
        return lessonNumber

    def runEvolution(self):
        start = time.time()
        population, genNum = self.evolution()
        end = time.time()
        
        #self.result1 = []
        self.result = population[0]
        self.clashes = self.fitness(self.result)
        self.accuracy = ((((self.timetableSize*self.scheduleSize)-self.clashes)/(self.timetableSize*self.scheduleSize))*100)
        self.completionTime = (end - start)
        self.roomScheduleDataSortedArray = []


        for i, roomScheduleGenomes in enumerate(self.result):
            roomScheduleData = self.genome_to_data(roomSchedule=roomScheduleGenomes)
            for j, lesson in enumerate(roomScheduleData):
                roomScheduleDataSorted = sorted(
                    roomScheduleData,
                    key=lambda lesson: self.sortLessonSchedule(lesson),
                    reverse=False,
                )
        
            for x, lesson in enumerate(roomScheduleDataSorted):
                room = self.rooms[i]
                teacher = lesson[0].split("-")[0]
                subject = lesson[0].split("-")[1]
                day = lesson[1]
                period = lesson[2]
                newLesson = room, subject, teacher, day, period
                self.roomScheduleDataSortedArray.append(newLesson)

        self.finalData.append(self.roomScheduleDataSortedArray)
        self.finalData.append(self.clashes)
        self.finalData.append(self.accuracy)
        self.finalData.append(self.completionTime)
        
        #for lesson in self.roomScheduleDataSortedArray:
        #    print(lesson)
        ##   
        #print(f'-> clashes: {self.clashes}')
        #print(f'-> accuracy: {self.accuracy}%')
        #print(f'-> no.gens: {genNum}')
        #print((f'-> time: {self.completionTime}s'))
        #
        #for i in range(len(self.result)):
        #    return population[0][i]
        #
        #return (self.roomScheduleDataSortedArray, self.clashes, self.accuracy, self.completionTime)
#geneticAlg()