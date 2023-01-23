import random
import sys
from time import sleep
import matplotlib.pyplot as plt



class clSimulation():
    def __init__(self):
        self.DT = 0.1  # seconds
        self.vCar = []
        self.vRoad = []
        self.timeMax = 100  # sec #2*60*60   2*60*60=2 hours (time of simulation in secs)
        self.Strategies = self.clStrategies()

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


    def simul(self, bPrint=True, bPrintCarPositions=True):
        self.addRoad()
        self.addRoad()

        self.Strategies.iStrategy = self.Strategies.iStrategy_fromGUI_get()
        self.simulCars()

        time_current = 0
        if len(self.vCar) > 0:  # if there is any car
            iCar = 0  # the index of the first car
            car = self.vCar[iCar]
            while time_current < self.timeMax:
                for Road in self.vRoad:
                    Road.update_car_locations(self.DT, time_current)
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
                        iRoad = self.Strategies.iRoad_get(car, Simulation, time_current)  #get the road for the car
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
        with open('varResult1.txt', 'w') as f:
            f.write('Standard deviation: '+ str(round(std1,2))+ ', '+ str(round(std2,2)))

        x1,y1=self.vRoad[0].tOnRoadAverage_onAllFinished_print()  # print average driving tine road 1
        x2,y2=self.vRoad[1].tOnRoadAverage_onAllFinished_print()  # print average driving tine road 2
        list1=[x1,x2]
        list2=[y1,y2]
        plt.bar(list1, list2, width = 0.8, color = ['red', 'green'])
        plt.xlabel('Cars on road')
        plt.ylabel('Average time on the road')
        plt.title('Simulation result')
        plt.legend(loc='best')
        plt.savefig('C:\\\\Users\\\\franc\\\\eclipse-workspace\\\\Phase2\\\\src\\\\GUI\\\\tests result.png')
        # plt.show()

    class clStrategies():
        def __init__(self):
            self.vStrategy = []

            self.addStrategy("0 - random", "Random road with equal probability")
            self.addStrategy("1 - based on preference", "Each driver to his preferred road, or go randomly")
            self.addStrategy("2 - all to the first road", "all to road 1")
            self.addStrategy("3 - all to the second road", "all to road 2")
            self.addStrategy("4 - less congested", "each driver observes the roads and takes the less congested")
            self.addStrategy("5 - our", "our strategy to recommend drivers")

            self.iStrategy = 2

        def addStrategy(self, sName, sDiscription):  # add strategy to the list
            n = len(self.vStrategy)
            self.vStrategy.append(self.clStrategy(n, sName, sDiscription))

        def iRoad_get(self, car, Simulation, time_current):  # get the road for the car
            return self.vStrategy[self.iStrategy].iRoad_get(car, Simulation, time_current)

        class clStrategy():
            def __init__(self, id, sName, sDiscription):
                self.id = id
                self.sName = sName
                self.sDiscription = sDiscription

            def iRoad_get(self, car, Simulation, time_current):  # get the road that the car will go to by the
                # suitable strategy
                nRoads = len(Simulation.vRoad)
                if nRoads < 2:  # if there is only one road then send to it
                    return 0
                if self.id == 0:
                    return random.randint(0, nRoads - 1)
                if self.id == 1:
                    if car.index_pref == 1:
                        return 0
                    if car.index_pref == 2:
                        return 1
                    return random.randint(0, nRoads - 1)
                if self.id == 2:
                    return 0
                if self.id == 3:
                    return 1
                if self.id == 4:
                    road1_cars = Simulation.vRoad[0].nCarsOnRoadPart_get(0, 100)
                    road2_cars = Simulation.vRoad[1].nCarsOnRoadPart_get(0, 100)
                    if road1_cars > road2_cars:
                        return 1
                    else:
                        return 0
                if self.id == 5:
                    if time_current <= 50:  # if time <=50 then there is more chance for driver to follow
                        # instructs to his fav road
                        if car.index_pref == 1:
                            car.probability_for_1 = min(car.probability_for_1 + 0.05, 1)
                            car.probability_for_2 = 1 - car.probability_for_1
                        elif car.index_pref == 2:
                            car.probability_for_2 = min(car.probability_for_2 + 0.05, 1)
                            car.probability_for_1 = 1 - car.probability_for_2

                    if random.uniform(0, 1) <= car.probability_for_1:
                        return 0
                    else:
                        return 1

        def iStrategy_fromGUI_get(self):  # set strategy to run
            index=0
            # here we take each value in each row seperatly
            file_path = sys.argv[1]
            
            with open(file_path, 'r') as f:
                for line in f:
                    values = line.strip().split(',')
                    if index==0:
                        r1_len=values[0]
                        r1_max_speed = values[1]
            
                    elif index == 1:
                            r2_len = values[0]
                            r2_max_speed = values[1]
            
                    elif index == 2:
                        chosen_strategy=values[0]
            
                    index+=1
            
            if chosen_strategy == "Random road with equal probability":
                strategy_num = 0
            
            elif chosen_strategy == "send each driver to his preferred road":
                strategy_num = 1
            
            elif chosen_strategy == "all in road 1":
                strategy_num = 2
            
            else:
                strategy_num = 3

           
            return strategy_num

    class clCar():
        def __init__(self, id):
            self.id = id
            self.road = None
            self.entrance_time = None  # sec
            self.exit_time = None  # sec

            self.carPrevOnRoad = None
            self.location = 0  # m
            self.speed = 0  # m/sec

            self.safeDist = 2  # meters
            self.safeCoef = float(2) / 3  # 40 m for 60 km/h => t=40/(60*1000/(60*60))=2.4 sec
            self.length = 3  # meters
            
            # 1 - prefer the first road (p>0.5)
            # 2 - prefer the second road (p>0.5)
            # 3 - random of two roads
            self.index_pref = random.randint(1, 3)  # set car preferred road
            if self.index_pref == 1:
                self.probability_for_1 = random.uniform(1, 0.51)  # probability to follow 1 if recommended
                self.probability_for_2 = 1 - self.probability_for_1  # probability to follow 2 if recommended

            elif self.index_pref == 2:
                self.probability_for_2 = random.uniform(1, 0.51)
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

        def Vms_get(self, Vkmh):  # get speed in meter/sec
            return float(Vkmh) * 1000 / (60 * 60)

        def Vkmh_get(self, Vms):  # get speed in km/h
            return float(Vms) * 60 * 60 / 1000

        def add_car(self, car):  # ,entrance_time):
            car.road = self
            car.carPrevOnRoad = self.carLast
            # car.entrance_time=entrance_time
            self.carLast = car

        def update_car_locations(self, dt, time_current):
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
                t = car.exit_time - car.entrance_time
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
            s = "Road " + str(self.id) + " average driving time by " + str(n) + " drivers is: " + str(
                tOnRoadAverage_onAllFinished)
            print(s)
            return n,tOnRoadAverage_onAllFinished


Simulation = clSimulation()
Simulation.simul(False, False)  # false= don't print all details, just the road status

# cd C:/Frenkel/Braude/2021-2022b/trafficJam/prog/
# python "C:/Frenkel/Braude/2021-2022b/trafficJam/prog/test1.py"
