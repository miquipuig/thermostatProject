# thermostatProject
# Copyright (C) 2020  Miquel Puig Gibert @miquipuig
 
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
 
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
 
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

from datetime import datetime,timedelta
import numpy as np
import random
class ThermostatHistory:

    historicData = []
    compressData = []
    storedData = []
    fakecounter=0
    
    def __init__(self):
        self.loadData()

    def round1min(self, tm):
        tm = tm+timedelta(minutes=0.5)
        tm = tm-timedelta(minutes=tm.minute % 1, seconds=tm.second, microseconds=tm.microsecond)
        return tm
    
    def round15min(self,tm):
            tm = tm+ timedelta(minutes=7.5)
            tm = tm-timedelta(minutes=tm.minute % 15, seconds=tm.second, microseconds=tm.microsecond)
            return tm

    def roundTime(self,time,min):
        time = time+ timedelta(minutes=min/2)
        time = time-timedelta(minutes=time.minute % min, seconds=time.second, microseconds=time.microsecond)
        return time
    
    def meanData(self,tm, section):
        data1, data2, data3 = ([] for i in range(3))
        for x in range(len(section)):
            data1.append(section[x][1])
            data2.append(section[x][2])
            data3.append(section[x][3])
        return [tm,np.around(np.median(data1),decimals=1),np.around(np.mean(data2),decimals=1),np.around(np.mean(data3),decimals=1)]
    def compress(self,rTime=1):
        print('comppress')
        try:
            lastDate=datetime.now()-timedelta(minutes=rTime*1.5)
            roundLastDate=self.roundTime(lastDate,rTime)
            i=0
            while(i<len(self.historicData) and self.roundTime(self.historicData[i][0],rTime)< roundLastDate):
                tm=self.roundTime(self.historicData[i][0],rTime)
                tempData = []
                j=i
                while(i<len(self.historicData) and self.roundTime(self.historicData[i][0],rTime) == tm and tm < roundLastDate):
                    i+=1
                self.compressData.append(self.meanData(tm,self.historicData[j:i]))
                # Delete
                self.historicData=self.historicData[i:len(self.historicData)]
                #reset index
                i=0
        except Exception as ex:
            print(ex)   
        
        self.storeData()
        
    def loadData(self, data=datetime.now().strftime("%Y-%m-%d")):
        try:
            historicFile=open('historicData-'+data+'.csv','r')
        except:
            return
        lines=historicFile.read().split('\n')
        for i in range(len(lines)-1):
            params=lines[i].split(',')
            self.storedData.append([datetime.strptime(params[0], "%Y-%m-%d %H:%M:%S"),float(params[1]),float(params[2]),float(params[3])])
        historicFile.close()

    def storeData(self):
        try:
            data=self.compressData[0][0].strftime("%Y-%m-%d")
        except:
            return
        dataFinish=self.compressData[len(self.compressData)-1][0].strftime("%Y-%m-%d")
        historicFile=open('historicData-'+data+'.csv','a+')
        if(data==dataFinish):
            for i in range(len(self.compressData)):
                historicFile.write(self.compressData[i][0].strftime("%Y-%m-%d %H:%M:%S"))
                historicFile.write(',')
                historicFile.write(str(self.compressData[i][1]))
                historicFile.write(',')
                historicFile.write(str(self.compressData[i][2]))
                historicFile.write(',')
                historicFile.write(str(self.compressData[i][3]))
                historicFile.write('\n')
            historicFile.close()
            if(len(self.storedData)>0):
                if(self.storedData[len(self.storedData)-1][0].strftime("%Y-%m-%d")==dataFinish):
                    self.storedData=self.storedData+self.compressData
                else:
                    self.storedData=self.compressData
            else:
                self.storedData=self.compressData
        else:
            for i in range(len(self.compressData)):
                if(data!=self.compressData[i][0].strftime("%Y-%m-%d")):
                    data=self.compressData[i][0].strftime("%Y-%m-%d")
                    historicFile.close()
                    historicFile=open('historicData-'+data+'.csv','a+')
                    lastDate=i
                historicFile=open('historicData.csv'+self.compressData[i][0].strftime("%Y-%m-%d"),'a+')
                historicFile.write(self.compressData[i][0].strftime("%Y-%m-%d %H:%M:%S"))
                historicFile.write(',')
                historicFile.write(str(self.compressData[i][1]))
                historicFile.write(',')
                historicFile.write(str(self.compressData[i][2]))
                historicFile.write(',')
                historicFile.write(str(self.compressData[i][3]))
                historicFile.write('\n')
                historicFile.close()   
            self.storedData=self.compressData[i:(len(self.compressData)-1)]
        self.compressData=[]
      
    def extractHistoricData(self,num):
        history=self.storedData+self.compressData+self.historicData
        data=[]
        for i in range(len(history)):
            data.append(history[i][num])
        return data
             
    def updateFake(self):
        for i in range(20):
            self.historicData.append([datetime.now()+timedelta(hours=i)+timedelta(hours=20*self.fakecounter),20+random.gauss(-4,4),20+random.gauss(0,2),50+random.gauss(-50,50)])
        self.fakecounter = self.fakecounter+1 