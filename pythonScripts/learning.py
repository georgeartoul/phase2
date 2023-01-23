import sys
import random
from time import sleep
import matplotlib.pyplot as plt



class clLearn:
    def __init__(self):  # Define the parameters of the Q-learning algorithm
        self.DT = 0.1  # seconds
        self.vCar = []
        self.vRoad = []
        self.timeMax = 90  # sec #2*60*60   2*60*60=2 hours (time of simulation in secs)
        self.alpha = 0.1  # learning rate
        self.gamma = 0.9  # discount factor
        self.epsilon = 0.1  # exploration rate
        # states (num of cars in 100 meters(0-10) in entrance of 2 roads and 3 drivers types)
        # q table= (first road number of cars, first road number of cars, driver type, 2 columns for values )
        self.q_table = [(i, j, k, 0, 0) for i in range(11) for j in range(11) for k in range(1, 4)]

    def addRoad(self):
        id = len(self.vRoad)
        Road = self.clRoad(id)
        self.vRoad.append(Road)

    def simulCars(self):  # add cars to the array with entrance time
        nCars = 0
        dtAve = 2  # sec- in average, every dtAve secs enters cars to the road
        dtSTDV = 3  # sec

        time_current = 0
        while time_current < self.timeMax:
            dt = random.gauss(dtAve, dtSTDV)  # time between 2 cars that entered the road
            time_current += dt
            if dt < 0:
                dt = 0
            car = self.clCar(nCars)
            car.entrance_time = time_current
            self.vCar.append(car)  # add the new car to cars list
            nCars += 1
        print("simulCars: nCars=" + str(nCars))  # print how many cars were entered in 100 secs

    def setRoad(self, car, time_current):
        p = 0.7
        rec = random.randint(0, 1)  # 0 or 1
        random_number = random.uniform(0, 1)  # between 0-1
        # check the roads status
        road1_status = self.vRoad[0].nCarsOnRoadPart_get(0, 100)
        road2_status = self.vRoad[1].nCarsOnRoadPart_get(0, 100)

        if rec == 0:
            if car.index_pref == 1:
                probability_for_1 = 1 - (1 - p) ** 2  # probability to follow 1 if recommended
                probability_for_2 = (1 - p) ** 2  # probability to follow 2 if recommended

            elif car.index_pref == 2:
                probability_for_1 = 1 - p * (1 - p)
                probability_for_2 = p * (1 - p)
            else:
                probability_for_1 = p
                probability_for_2 = 1 - p

            if probability_for_1 <= random_number:
                car.hisRoad_status = road1_status
                car.secondRoad_status = road2_status
                return 0
            else:
                car.hisRoad_status = road2_status
                car.secondRoad_status = road1_status
                return 1

        else:  # we recommended second road(1)
            if car.index_pref == 1:
                probability_for_1 = p * (1 - p)  # probability to follow 1 if recommended
                probability_for_2 = 1 - p * (1 - p)  # probability to follow 2 if recommended

            elif car.index_pref == 2:
                probability_for_1 = (1 - p) ** 2
                probability_for_2 = 1 - (1 - p) ** 2
            else:
                probability_for_1 = 1 - p
                probability_for_2 = p

            if probability_for_2 <= random_number:
                car.hisRoad_status = road2_status
                car.secondRoad_status = road1_status
                return 1
            else:
                car.hisRoad_status = road1_status
                car.secondRoad_status = road2_status
                return 0

    def updateQ(self, car):  # update the q table
        in_road = car.road  # the road the car was in
        if car.hisRoad_status > 10 or car.secondRoad_status > 10:
            result = [index for index, tup in enumerate(self.q_table) if tup[0] == 10 and
                      tup[1] == 10 and tup[2] == car.index_pref]
        else:

            if in_road == 0:
                # get the suitable row in the q table
                result = [index for index, tup in enumerate(self.q_table) if tup[0] == car.hisRoad_status and
                      tup[1] == car.secondRoad_status and tup[2] == car.index_pref]
            else:
                result = [index for index, tup in enumerate(self.q_table) if tup[0] == car.secondRoad_status and
                      tup[1] == car.hisRoad_status and tup[2] == car.index_pref]

        x = result[0]  # get the right index in the table
        self.calc_update(car, in_road.id, x)  # make the update

    def calc_update(self, car, in_road, x): # make the update in q table
        if in_road == 1:
            second_road = 0
        else:
            second_road = 1
        vt = self.vRoad[second_road].vt_get()
        l=len(vt)
        if l>0:
         other_road_lastFinished = vt[l-1]
        else:
         other_road_lastFinished=0
        # calculate the maxQ's',a')=the time took last car in second road to finish
        if other_road_lastFinished <= self.vRoad[second_road].avgTime:
            maxQQ = 10
        else:
            maxQQ = -10

        # calculate the reward
        if (car.exit_time - car.entrance_time) <= self.vRoad[in_road].avgTime:
            reward = 10
        else:
            reward = -10

        # make the update
        if in_road == 0:
            res = self.q_table[x][3] + self.alpha * (reward + self.gamma * maxQQ - self.q_table[x][3])
            self.q_table[x] = (self.q_table[x][0], self.q_table[x][1],
                               self.q_table[x][2], res, self.q_table[x][4])
        else:
            res = self.q_table[x][4] + self.alpha * (reward + self.gamma * maxQQ - self.q_table[x][4])
            self.q_table[x] = (self.q_table[x][0], self.q_table[x][1],
                               self.q_table[x][2], self.q_table[x][3], res)

    def simul(self, bPrint=True, bPrintCarPositions=True):
        self.addRoad()
        self.addRoad()
        self.simulCars()

        time_current = 0
        if len(self.vCar) > 0:  # if there is any car
            iCar = 0  # the index of the first car
            car = self.vCar[iCar]
            while time_current < self.timeMax:
                for Road in self.vRoad:
                    Road.update_car_locations(self.DT, time_current,self)
                if bPrint:
                    print("time_current=" + str(time_current))
                b = True  # b= should we enter more cars, at beginning yes
                while b:
                    b = (iCar < len(self.vCar))  # if there are more cars
                    if bPrint:
                        print("iCar=" + str(iCar))
                    if b:
                        car = self.vCar[iCar]  # last car that is not entered the road yet
                        if bPrint:
                            print(str(car.entrance_time))
                        b = (car.entrance_time < time_current)  # should we enter the car or not
                    if b:
                        iRoad = self.setRoad(car, time_current)  # get the road for the car
                        self.vRoad[iRoad].add_car(car)

                        if bPrint:
                            print("add car")
                        iCar += 1  # the id of next car that not entered yet
                if bPrintCarPositions:
                    print("t=" + str(time_current) + " " + self.vRoad[0].s_get())  # print road 1
                    print("t=" + str(time_current) + " " + self.vRoad[1].s_get())  # print road 2
                time_current += self.DT
        if bPrint:
            print("nCars=" + str(len(self.vCar)))
            for car in self.vCar:
                print(str(car.entrance_time))
        self.vRoad[0].tOnRoadAverage_onAllFinished_print()  # print average driving tine road 1
        self.vRoad[1].tOnRoadAverage_onAllFinished_print()  # print average driving tine road 2
        
        # -----------------------------------------run after learning-----------------------------------------------------
    def setRoad2(self, car, time_current):

        # check the roads status
        road1_status = self.vRoad[0].nCarsOnRoadPart_get(0, 100)
        road2_status = self.vRoad[1].nCarsOnRoadPart_get(0, 100)
        # get the suitable row in the q table
        if road1_status>10 or road2_status>10:
            result = [index for index, tup in enumerate(self.q_table) if tup[0] == 10 and
                      tup[1] == 10 and tup[2] == car.index_pref]
        else:
            result = [index for index, tup in enumerate(self.q_table) if tup[0] == road1_status and
                    tup[1] == road2_status and tup[2] == car.index_pref]
        x = result[0]  # get the right index in the table
        if (self.q_table[x][3] > self.q_table[x][4]):
            return 0
        else:
            return 1

    def simul2(self, bPrint=True, bPrintCarPositions=True):
        self.vCar = []
        self.simulCars()

        time_current = 0
        if len(self.vCar) > 0:  # if there is any car
            iCar = 0  # the index of the first car
            car = self.vCar[iCar]
            while time_current < self.timeMax:
                for Road in self.vRoad:
                    Road.update_car_locations(self.DT, time_current, self)
                if bPrint:
                    print("time_current=" + str(time_current))
                b = True  # b= should we enter more cars, at beginning yes
                while b:
                    b = (iCar < len(self.vCar))  # if there are more cars
                    if bPrint:
                        print("iCar=" + str(iCar))
                    if b:
                        car = self.vCar[iCar]  # last car that is not entered the road yet
                        if bPrint:
                            print(str(car.entrance_time))
                        b = (car.entrance_time < time_current)  # should we enter the car or not
                    if b:
                        iRoad = self.setRoad2(car, time_current)  # get the road for the car
                        self.vRoad[iRoad].add_car(car)

                        if bPrint:
                            print("add car")
                        iCar += 1  # the id of next car that not entered yet
                if bPrintCarPositions:
                    print("t=" + str(time_current) + " " + self.vRoad[0].s_get())  # print road 1
                    print("t=" + str(time_current) + " " + self.vRoad[1].s_get())  # print road 2
                time_current += self.DT
        if bPrint:
            print("nCars=" + str(len(self.vCar)))
            for car in self.vCar:
                print(str(car.entrance_time))
        
        pow_times1 = 0
        pow_times2 = 0
        avg1, n1 = self.vRoad[0].tOnRoadAverage_onAllFinished_get()
        avg2, n2 = self.vRoad[1].tOnRoadAverage_onAllFinished_get()

        finished_cars1 = self.vRoad[0].vt_get()
        finished_cars2 = self.vRoad[1].vt_get()
        for time in finished_cars1:
            pow_times1 += (time - avg1) ** 2
        for time in finished_cars2:
            pow_times2 += (time - avg2) ** 2

        variance1 = pow_times1 / (n1 - 1)
        variance2 = pow_times2 / (n2 - 1)
        std1 = variance1 ** 0.5
        std2 = variance2 ** 0.5
        print("variance of roads is= ", variance1, ", ", variance2, " and std are: ", std1, ", ", std2)
        with open('varResult2.txt', 'w') as f:
            f.write('Standard deviation: '+ str(round(std1,2))+ ', '+ str(round(std2,2)))

        
        x1,y1=self.vRoad[0].tOnRoadAverage_onAllFinished_print()  # print average driving tine road 1
        x2,y2=self.vRoad[1].tOnRoadAverage_onAllFinished_print()  # print average driving tine road 2
        list1=[x1,x2]
        list2=[y1,y2]
        plt.bar(list1, list2, width = 0.8, color = ['red', 'green'])
        plt.xlabel('Cars on road')
        plt.ylabel('Average time on the road')
        plt.title('Machine learning strategy result')
        plt.legend(loc='best')
        plt.savefig('C:\\\\Users\\\\franc\\\\eclipse-workspace\\\\Phase2\\\\src\\\\GUI\\\\tests result2.png')
        # plt.show()

    # -------------------------------------------------------------------------------------------------------------------

    class clCar():
        def __init__(self, id):
            self.id = id
            self.road = None
            self.entrance_time = None  # sec
            self.exit_time = None  # sec

            self.carPrevOnRoad = None
            self.location = 0  # m
            self.speed = 0  # m/sec
            self.hisRoad_status = 0  # status of the road when car entered ####################################
            self.secondRoad_status = 0  # status of the other road when car entered ########################
            self.safeDist = 2  # meters
            self.safeCoef = float(2) / 3  # 40 m for 60 km/h => t=40/(60*1000/(60*60))=2.4 sec
            self.length = 3  # meters
            self.p = 0.7
            # 1 - prefer the first road
            # 2 - prefer the second road
            # 3 - random of two roads
            self.index_pref = random.randint(1, 3)  # set car preferred road
            if self.index_pref == 1:
                self.probability_for_1 = 1 - (1 - self.p) ** 2  # probability to follow 1 if recommended
                self.probability_for_2 = 1 - self.probability_for_1  # probability to follow 2 if recommended

            elif self.index_pref == 2:
                self.probability_for_2 = 1 - (1 - self.p) ** 2
                self.probability_for_1 = 1 - self.probability_for_2

            else:
                self.probability_for_2 = random.uniform(0, 1)
                self.probability_for_1 = 1 - self.probability_for_2

        def update_location(self, dt):
            if self.carPrevOnRoad is None:
                self.speed = self.road.VMAX
            else:
                # Calculate distance to previous car
                distance_to_prev = self.carPrevOnRoad.location - self.location
                d = distance_to_prev - self.carPrevOnRoad.length - self.safeDist
                if d <= 0:
                    self.speed = 0
                else:
                    # Calculate safe distance
                    # safe_distance = distance_to_prev/3
                    # Calculate desired speed
                    # desired_speed = safe_distance / dt
                    # Set speed to be at least 0
                    desired_speed_kmh = float(d) / self.safeCoef  # 60 km/h for 40 m
                    desired_speed = self.road.Vms_get(desired_speed_kmh)
                    self.speed = min(self.road.VMAX, desired_speed)

            # Update location
            self.location += self.speed * dt

        def s_get(self):  # func to get car details
            return str([self.id, self.location, self.speed, self.road.Vkmh_get(self.speed)])

    class clRoad():
        def __init__(self, id, length_meters=1000, VMAXKmh=60):
            self.id = id
            self.ROAD_LENGTH = length_meters  # meters road length
            self.VMAXkmh = VMAXKmh  # km/h VMAX
            self.VMAX = self.Vms_get(self.VMAXkmh)  # meters per second
            self.carLast = None  # last car to enter the road
            self.vCarFinished = []
            self.avgTime = self.ROAD_LENGTH / self.VMAXkmh  # average time to finish should be########################

        def Vms_get(self, Vkmh):  # get speed in meter/sec
            return float(Vkmh) * 1000 / (60 * 60)

        def Vkmh_get(self, Vms):  # get speed in km/h
            return float(Vms) * 60 * 60 / 1000

        def add_car(self, car):  # ,entrance_time):
            car.road = self
            car.carPrevOnRoad = self.carLast
            # car.entrance_time=entrance_time
            self.carLast = car

        def update_car_locations(self, dt, time_current,clLearn):
            car = self.carLast  # we start with the last car to enter the road
            carFirst = None
            while not (car is None):
                car.update_location(dt)
                if car.location <= self.ROAD_LENGTH:
                    carFirst = car
                car = car.carPrevOnRoad

            # car = carFirst  # the first car on the road- closest to end
            if carFirst is None:  # if there's no cars in the road
                carLastToExit = self.carLast
                self.carLast = None
            else:
                carLastToExit = carFirst.carPrevOnRoad
                carFirst.carPrevOnRoad = None
            car = carLastToExit
            while not (car is None):  # take off the cars that finished from the road
                car.exit_time = time_current
                clLearn.updateQ(car)
                self.vCarFinished.append(car)
                carPrev = car
                car = car.carPrevOnRoad
                carPrev.carPrevOnRoad = None

        def nCarsOnRoad_get(self):  # count how many cars there is on the road
            n = 0
            car = self.carLast
            while not (car is None):
                n += 1
                car = car.carPrevOnRoad
            return n

        def nCarsOnRoadPart_get(self, xStart, xEnd):  # count how many cars there is on the road between 2 points
            n = 0
            car = self.carLast
            while not (car is None):
                if car.location >= xStart and car.location <= xEnd:
                    n += 1
                car = car.carPrevOnRoad
            return n

        def vt_get(self):  # save in array how much time took the cars to pass the road
            vt = []
            for car in self.vCarFinished:
                t = abs(car.exit_time - car.entrance_time)
                vt.append(t)
            return vt

        def s_get(self):  # get the road status
            s = "Road " + str(self.id) + ":"
            car = self.carLast
            while not (car is None):
                s += " " + car.s_get()
                car = car.carPrevOnRoad
            return s

        def tOnRoadAverage_onAllFinished_get(self):  # get the average time of road driving
            vt = self.vt_get()
            n = len(vt)
            if n == 0:
                return 0, 0
            tOnRoadAverage_onAllFinished = 0
            for t in vt:
                tOnRoadAverage_onAllFinished += t
            tOnRoadAverage_onAllFinished /= n
            return tOnRoadAverage_onAllFinished, n

        def tOnRoadAverage_onAllFinished_print(self):  # print the average time of road driving
            tOnRoadAverage_onAllFinished, n = self.tOnRoadAverage_onAllFinished_get()
            absolute_tOnRoadAverage_onAllFinished=abs(tOnRoadAverage_onAllFinished)
            s = "Road " + str(self.id) + " average driving time by " + str(n) + " drivers is: " + str(
                absolute_tOnRoadAverage_onAllFinished)
            print(s)
            return n,absolute_tOnRoadAverage_onAllFinished


Simulation = clLearn()
Simulation.simul(False, False)  # false= don't print all details, just the road status
Simulation.simul2(False, False)
