from pickle import FALSE
import matplotlib.pyplot as plt
import numpy as np
import random
import math

maxCo2 =8
root2 = math.sqrt(2)
maxLandDamp =8
maxWind = 1
minWind = -1
minHeat =-40
maxHeat =40
minDamp = 0
maxDamp =40
maxCo2 =100
minCo2 =0
eastMax =50
northMax =50
maxForest =10
sea = 0
dirt = 1




# the area reprasent the area over one peace of area
#its hold all the atmosphric an ecolgical information about this area
# it also can update this information base on the niber of this area
class Area:
        def __init__(self ,id,landType ,sunFactor ):
            self.forest = 0
            self.id =id
            self.heat = random.randint(minHeat ,maxHeat)
            self.windDir = [random.uniform(minWind, maxWind),random.uniform(minWind, maxWind)]
            self.co2 =0
            self.damp =0
            self.landType = landType
            self.up = self
            self.down = self
            self.right =self
            self.left = self
            self.landDamp = 0
            self.rain = 0
            self.sunFactor = sunFactor
            self.Foctory = False
        # to find the next heat parmter we need to consider 3 element
        # 1 how mouch heat it get from each niber dicide by the wind of the nibet and it heat
        # 2 how much heat it give to the niber base on self wind
        # 3(not writen yet) how mouch heat it get from the sun base on thw type of land and level of polltion
        def nextHeat(self):
            addUp = self.windFactor(self.up.windDir,[1,0])*self.up.heat
            addRight = self.windFactor(self.right.windDir,[0,1])*self.right.heat
            addDown = self.windFactor(self.down.windDir,[-1,0])*self.down.heat
            addLeft = self.windFactor(self.left.windDir,[0,-1])*self.left.heat
            heat  = (self.heat*(1-self.windSize(self.windDir[0],self.windDir[1])) + addUp + addRight +addDown + addLeft  )*self.landHeatFactor() + self.sunFactor
            if heat > maxHeat:
                return maxHeat
            elif heat < minHeat:
                return minHeat
            return heat

        # nextWind calaculte the wind in cell base on the the sum of the wind that it get from it niber
        def nextWind(self):
            wind = self.windDir.copy()
            wind[0] = (self.down.windDir[0] + self.up.windDir[0])/3 + ( self.up.heat - self.down.heat)/(maxHeat*20)
            wind[1] =  (self.left.windDir[1] + self.right.windDir[1])/3 + ( self.right.heat - self.left.heat)/(maxHeat*20)
            power = self.windSize(wind[0] , wind[1])
            if power > 1:
               wind[0] = wind[0]/math.sqrt(power)
               wind[1] = wind[1]/math.sqrt(power)
            return wind


         # the next damp effect by 3 paremter
         # the damp in the niber cell multypell by the wind factor
         # if there is rain it take the damp out of the air
         # if the land type is sea the heat up the damp
        def nextDamp(self):
            addUp = self.windFactor(self.up.windDir,[1,0])*self.up.damp*(1-self.up.rain)
            addRight = self.windFactor(self.right.windDir,[0,1])*self.right.damp*(1-self.right.rain)
            addDown = self.windFactor(self.down.windDir,[-1,0])*self.down.damp*(1-self.down.rain)
            addLeft = self.windFactor(self.left.windDir,[0,-1])*self.left.damp*(1-self.left.rain)
            if self.rain == True:
                damp = addUp + addRight +addDown + addLeft
            else:
                damp  = (self.damp*(1-self.windSize(self.left.windDir[0] ,self.left.windDir[1])) + addUp + addRight +addDown + addLeft)
            if self.landType == sea and self.heat > 0:
                damp += self.heat/maxHeat
            if damp > maxDamp:
                return maxDamp
            if damp < minDamp:
                return minDamp
            return damp

        # the next co2 are base on the last co2 in the niber multypel in the wind factor and rise only above factory
        def nextCo2(self):
            addUp = self.windFactor(self.up.windDir,[1,0])*self.up.co2*(1-self.up.rain)
            addRight = self.windFactor(self.right.windDir,[0,1])*self.right.co2*(1-self.right.rain)
            addDown = self.windFactor(self.down.windDir,[-1,0])*self.down.co2*(1-self.down.rain)
            addLeft = self.windFactor(self.left.windDir,[0,-1])*self.left.co2*(1-self.left.rain)
            if self.rain == 1:
                co2 = addUp + addRight + addDown + addLeft
            else:
                co2 = self.co2 * (1 - self.windSize(self.left.windDir[0],self.left.windDir[1])) + addUp + addRight + addDown + addLeft
            if self.Foctory == True :
                co2 +=0.5
            if(co2 > maxCo2):
                return maxCo2
            return co2
        # the rain is factor of the heat and the damp
        def nextRain(self):
            if self.damp* (maxHeat-self.heat)  > maxHeat*maxDamp/4:
                return 1
            else:
                return 0


        #next landDamp the dump increase when there is rain and decrese
        def nextLandDamp(self):
            if self.landType == sea:
                return 0
            if self.rain == 1:
                if self.landDamp< maxLandDamp:
                    return self.landDamp + 3
                else:
                    return self.landDamp
            elif self.landDamp > 1:
                return self.landDamp-1
            return 0

        # the forest grow when the condtion are goo not too hot not too cold not to dry and not to wet
        def nextForest(self):
            if self.landType == sea:
                return 0
            grow =0
            if self.heat < 30 and self.heat >5:
                grow+=0.5
            elif self.heat >35 or self.heat <-5:
                grow -=0.5
            if self.landDamp > 2 and self.landDamp < maxLandDamp -1:
                grow += 0.5
            elif self.landDamp == 0 or self.landDamp == maxLandDamp:
                grow-=0.5
            if self.forest + grow <0:
                return 0
            elif self.forest +grow > maxForest :
                return maxForest
            else:
                return self.forest+ grow
        # the wind factor use to find how mouch cell will effect his niber
        # by calculate how mouch wind came from him in that ditction using scalr multple of vectors
        def windFactor(self ,wind , dirction):
                if (dirction[0]*wind[0] +dirction[1]*wind[1])>0:
                    return math.sqrt(dirction[0]*wind[0] +dirction[1]*wind[1])*(0.9 - self.forest/(maxForest*10))
                else:
                    return 0

        # the inWindFactor use to find how mouch heat it give by calculte the oclidian length of the wind vector
        def windSize(self , x ,y):
            return math.sqrt(math.pow(x,2) + math.pow(y,2))/root2

        #the landHeatFactor efect on the temprture base on the type of the land
        def landHeatFactor(self):
            if self.landType == sea:
                return 0.75
            elif self.landType == dirt:
                return 0.91 - 0.15*(self.forest/maxForest) + 0.15 * self.co2/maxCo2


