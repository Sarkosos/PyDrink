"""
By Felix Quinque & Zbigniew Szymon Fonau
This method creates an array with the BAC over time for all drinks consumed, it does not yet apply elimination
"""
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import matplotlib.dates as mdates
import pandas as pd

class Adder:
    def __init__(self, height, weight, minute):
        self.minute = minute
        self.time_array = [] # Array that will contain The Blood Alcohol Concentration (BAC) over time
        self.height = height
        self.weight = weight

    #find the widmark factor
    #Formulas taken from Searle, J. (2014). 'Alcohol calculations and their uncertainty'.
    def widmark(self, weight, height, gender):
        BMI = weight/pow((height/100),2)
        if gender:
            male_r = 1.0181 -0.01213 * BMI
            return male_r
        else:
            female_r = 0.9367 - 0.01240 * BMI
            return female_r

    #finds how much alcohol of each drink is absorbed at each time
    def drink(self, volume, percent, minutes, half_life):
        half_lifes_passed = minutes/half_life
        alcohol = (volume/1000)*(percent/100)- (volume/1000)*(percent/100) * pow(0.5, half_lifes_passed)
        return alcohol
    #Calculates The BAC for every minute
    def bac_calc(self,alcohol, widmark_factor, weight):
        density = 0.78974
        C = (100 * alcohol * density) / (widmark_factor * weight) #C is here the concentration of alcohol in blood
        if C < 0: return 0 #if the concentration would be under 0 return 0 since you can't have a concentration <0
        else: return C

    def array(self, volume, percent, time, half_life):
        try:
            self.time_array = np.load('added_drinks.npy') #If there is an array with drinks use that (allows muliple drinks)
        except:
            self.time_array = []
        minutes = -time
        gender = True
        temp_time_array = []

        while len(temp_time_array) < 1440+self.minute: # makes a graph that shows the BAC for 24 hours after intake
            abs_alc = self.drink(volume, percent, minutes, half_life)
            temp_time_array.append(self.bac_calc(abs_alc, self.widmark(self.weight, self.height, gender), self.weight))
            minutes += 1
        if len(self.time_array) == 0:
            self.time_array = temp_time_array
        else: self.time_array = np.add(self.time_array, temp_time_array)
        np.save("added_drinks.npy", self.time_array)
    def plot(self):
        x = [ dt.datetime.now() +dt.timedelta(hours = i) for i in range(int(len(self.time_array)))]
        times = pd.date_range(start=self.minute, periods=len(self.time_array), freq='1min')
        fig, ax = plt.subplots(1)
        fig.autofmt_xdate()
        plt.plot(times, self.time_array)

        xfmt = mdates.DateFormatter('%H:%M')
        ax.xaxis.set_major_formatter(xfmt)

        plt.show()
        xfmt = mdates.DateFormatter('%H:%M')
        ax.xaxis.set_major_formatter(xfmt)
        #plt.plot( x, self.time_array)
        #plt.gcf().autofmt_xdate()

        # plt.xlim(left=self.minute)
        # plt.ylabel('BAC')
        #
        # plt.show()



if __name__ == '__main__':
    add = Adder(170,60,800)
    add.array(330, 9, 1120)
    add.plot()


