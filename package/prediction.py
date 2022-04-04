import csv
import datetime
import sys
import os
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

def predicted(area):
    #print(len(area))
    area=area+' '
    #print(area,len(area))
    now = datetime.datetime.now()
    month=now.month
    temp=[]
    temp_final=[]
    rain_fall=[]
    rainfall_final=[]
    prevtemp=0
    prevrainfall=0

    def conv(nutrient):
        nutrient_dict={'VL':1,'L':2,'M':3,'H':4,'VH':5 }
        return  nutrient_dict.__getitem__(nutrient)

    with open('./static/datasets/temprainfall.csv') as csvfile:
        #area=main()
        reader = csv.reader(csvfile)
        #print(area)
        flag=0
        for row in reader:
            if row[0] == area:
                if flag==0:
                    state=row[1]
                    flag=1
                    #print(state)
                temperature=(float(row[3])+float(row[4]))/2
                temp.append(round(temperature,2))
                rain_fall.append(float(row[5])) 
        csvfile.close 

    def rainfall(temp_final,rainfall_final,temp,rain_fall):    
        #print(temp)
        index=month-1
        prevtemp=0
        prevrainfall=0
        for i in range (1,13):
            prevtemp=prevtemp+temp[index]
            temp_final.append(round((prevtemp/i),2))
            prevrainfall=prevrainfall+rain_fall[index]
            rainfall_final.append(round(prevrainfall,2))
            index= index+1
            if index==12:
                index=0
        #print("final rain fall ",rainfall_final)

    def nutrients(state,rainfall_final,temp_final):
        narea=0
        parea=0
        karea=0
        try:
            with open('./static/datasets/soil-reports.csv', 'r') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if row[0] == state:
                        narea=conv(row[1])
                        parea=conv(row[2])
                        karea=conv(row[3])
                        ph=row[4]
        except IOError:
            print("No file exists named nutrientsarea.csv")               
        csvfile.close
        try:
            with open('./static/datasets/crop-database.csv', 'r') as csvfile, open('./static/datasets/metacrops.csv', 'w') as metacrops:
                reader = csv.reader(csvfile)
                writer=csv.writer(metacrops)
                metacrops.writelines("Crop, Rainfall, Temperature, pH \n")
                for row in reader:
                    ncrop=conv(row[8])
                    pcrop=conv(row[9])
                    kcrop=conv(row[10])
                    if(narea>=ncrop and parea>=pcrop and karea>=kcrop):
                        no_months=int(row[1])
                        total=row[0]+","+str(rainfall_final[no_months-1])+","+str(temp_final[no_months-1])+","+ph+"\n"
                        metacrops.writelines(total)
                    #print("total",total)
                    #print("metacrops",metacrops)
        except IOError:
            print("No file exists named cropDB.csv"),
        csvfile.close
        metacrops.close 

    def filewrite():
        n=1
        try:
            with open("./static/datasets/metacrops.csv",'r') as f:
                with open("./static/datasets/metacrops11.csv", "w") as f1:
                    for line in f:
                        if n==1:
                            n=n+1
                            continue
                        f1.write(line)
        except IOError as e:
            print("I/O error({0}): {1}".format(e.errno, e.strerror))
        f.close
        f1.close 

    def regression():
        n=0
        crop_Y_pred=[]
        crop_name=[]
        dataset=pd.read_csv('./static/datasets/regressiondb.csv')
        locbased=pd.read_csv('./static/datasets/metacrops.csv')
        try:
            with open('./static/datasets/metacrops11.csv', 'r') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    crop=row[0]
                    metadata=dataset.loc[dataset['Crop'] == crop]
                    X = metadata.iloc[:, :-2].values
                    Y = metadata.iloc[:, 4].values
                    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.1, random_state = 0)
                    regressor = LinearRegression()
                    regressor.fit(X_train, Y_train)  
                    X_locbased = locbased.loc[[n]].values 
                    X_locbased = X_locbased[:, 1:4]
                    Y_pred=regressor.predict(X_locbased)
                    if Y_pred>0:
                        crop_Y_pred.append(round(Y_pred[0],3))
                        crop_name.append(crop)
            sorted_crops=quicksort(crop_name,crop_Y_pred,0,len(crop_Y_pred)-1)                       
            csvfile.close
            return sorted_crops
        except IOError:
            print("No file exists named metacrops11.csv")
        os.remove('metacrops.csv')       
        os.remove('metacrops11.csv')

    def quicksort(crop_name,crop_Y_pred,start, end):
        if start < end:
            pivot = partition(crop_name,crop_Y_pred, start, end)
            quicksort(crop_name,crop_Y_pred, start, pivot-1)
            quicksort(crop_name,crop_Y_pred, pivot+1, end)
        return crop_name

    def partition(crop_name,crop_Y_pred, start, end):
        pivot = crop_Y_pred[start]
        left = start+1
        right = end
        done = False
        while not done:
            while left <= right and crop_Y_pred[left] >= pivot:
                left = left + 1
            while crop_Y_pred[right] <= pivot and right >=left:
                right = right -1
            if right<left:
                done= True
            else:
                temp=crop_Y_pred[left]
                crop_Y_pred[left]=crop_Y_pred[right]
                crop_Y_pred[right]=temp
                temp1=crop_name[left]
                crop_name[left]=crop_name[right]
                crop_name[right]=temp1
        temp=crop_Y_pred[start]
        crop_Y_pred[start]=crop_Y_pred[right]
        crop_Y_pred[right]=temp
        temp1=crop_name[start]
        crop_name[start]=crop_name[right]
        crop_name[right]=temp1
        return right    

    rainfall(temp_final,rainfall_final,temp,rain_fall)
    nutrients(state,rainfall_final,temp_final)
    filewrite()
    sorted_crop=regression()
    #print("final",sorted_crop)
    return sorted_crop
