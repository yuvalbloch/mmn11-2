import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseButton
import numpy as np
import area
import math
sunFactorBase =0.3 #lower ths parmrter to see the world die realy realy slow (tousends of circels)
fig , (axH, axF , axP) = plt.subplots(3)
axH.set_title('temprture')
axF.set_title('bioMass')
axP.set_title('co2')
data = { 'heat' : [] , 'damp' : [] , 'co2' : [] , 'bioMass': []}
class World:
    def __init__(self):
        # create the grid of the area
        self.grid = []
        for north in range(area.northMax):
            skyLine = []
            for east in range(area.eastMax):
                if area.northMax / 4 < north < area.northMax * 3 / 4 and area.eastMax / 4 < east < area.eastMax * 3 / 4:
                    skyLine.append(area.Area(east * area.eastMax + north, area.sea, sunFactorBase - math.pow(0.5 - (north / area.northMax), 2) * 6))
                else:
                    skyLine.append(area.Area(east * area.eastMax + north, area.dirt, sunFactorBase - math.pow(0.5 - (north / area.northMax), 2) * 6))
            self.grid.append(skyLine)

        # make any member of the area know about his niber
        for north in range(0, area.northMax):
            for east in range(0, area.eastMax):
                if east + 1 < area.eastMax:
                    self.grid[east][north].right = self.grid[east + 1][north]
                else:
                    self.grid[east][north].right = self.grid[0][north]
                if east > 1:
                    self.grid[east][north].left = self.grid[east - 1][north]
                else:
                    self.grid[east][north].left = self.grid[area.eastMax - 1][north]

                if north + 1 < area.northMax:
                    self.grid[east][north].up = self.grid[east][north + 1]
                else:
                    self.grid[east][north].up = self.grid[east][area.northMax - 1]
                if north > 1:
                    self.grid[east][north].down = self.grid[east][north - 1]
                else:
                    self.grid[east][north].down = self.grid[east][0]
        print("sky is ready")

    # the update must update all the parmter of all the area at once
    # so it create arey for each parmter fill it with all the infrmtio print it as if neede
    # and just after all the arrey are been created update the grid of area
    def update(self, i):
        # create arrey
        heat_shape = (area.eastMax, area.northMax)
        wind_shape = (area.eastMax, area.northMax, 2)
        rain = np.ones(heat_shape)
        damp = np.ones(heat_shape)
        heat = np.ones(heat_shape)
        wind = np.ones(wind_shape)
        landDamp = np.ones(heat_shape)
        printWind = np.ones(heat_shape)
        forest = np.ones(heat_shape)
        co2 = np.ones(heat_shape)
        sumOfHeat =0
        sumOfBioMass =0
        sumOfDamp =0
        sumOfCo2  = 0
        # fill arrey
        for east in range(area.eastMax):
            for north in range(area.northMax):
                heat[east][north] = self.grid[east][north].nextHeat()
                wind[east][north] = self.grid[east][north].nextWind()
                damp[east][north] = self.grid[east][north].nextDamp()
                rain[east][north] = self.grid[east][north].nextRain()
                landDamp[east][north] = self.grid[east][north].nextLandDamp()
                forest[east][north] = self.grid[east][north].nextForest()
                co2[east][north] = self.grid[east][north].nextCo2()
                sumOfHeat  += heat[east][north]
                sumOfBioMass  +=forest[east][north]
                sumOfDamp += damp[east][north]
                sumOfCo2 += co2[east][north]


        #save data
        data.get('heat').append(sumOfHeat / (area.eastMax * area.northMax))
        data.get('damp').append(sumOfDamp / (area.eastMax * area.northMax))
        data.get('bioMass').append(sumOfBioMass / (area.eastMax * area.northMax))
        data.get('co2').append(sumOfCo2 / (area.eastMax * area.northMax))

        # print maps
        axH.imshow(heat, vmax=area.maxHeat, vmin=area.minHeat)
        axF.imshow(forest)
        axP.imshow(co2)
        # update data
        for east in range(area.eastMax):
            for north in range(area.northMax):
                self.grid[east][north].heat = heat[east][north]
                self.grid[east][north].damp = damp[east][north]
                self.grid[east][north].windDir = wind[east][north]
                self.grid[east][north].rain = rain[east][north]
                self.grid[east][north].landDamp = landDamp[east][north]
                self.grid[east][north].forest = forest[east][north]
                self.grid[east][north].co2 = co2[east][north]

#start world
earth = World()
earth.update(1)

#event handelaer
def jump(event):
    print(event.button)
    if event.button is MouseButton.LEFT:
        for t in range(100):
            earth.update(1)
    elif event.button is MouseButton.RIGHT:
        earth.grid[25][1].Foctory =True
    else:
        df = pd.DataFrame(data)
        #df.to_excel(r'C:\Users\יובל\OneDrive\Desktop\climte-for-celluar-aoutomta1.xlsx' )# put file loction

plt.connect('button_press_event', jump)

#normal run
for t in range(1000):
    earth.update(1)
    fig.canvas.draw_idle()
    plt.pause(0.01)





plt.show()
