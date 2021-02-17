from PIL import Image, ImageSequence
import glob
import numpy as np
import os
from sklearn.model_selection import GridSearchCV,TimeSeriesSplit, RandomizedSearchCV
from sklearn.svm import SVR
from sklearn import decomposition
from sklearn.ensemble import RandomForestRegressor
import time
from sklearn.metrics import *
from skopt.space import Real, Integer, Categorical
from skopt.utils import use_named_args
from skopt import gp_minimize
from skopt import BayesSearchCV

#########################################################################
#########################################################################


# rain  = "C:/Users/Admin/Documents/Work/2020-Masters/data/seasonal/pre_processed/rainF_mad/*.png"
# evap  = "C:/Users/Admin/Documents/Work/2020-Masters/data/seasonal/pre_processed/evap_mad/*.png"
# humid = "C:/Users/Admin/Documents/Work/2020-Masters/data/seasonal/pre_processed/humid_mad/*.png"
# temp  = "C:/Users/Admin/Documents/Work/2020-Masters/data/seasonal/pre_processed/temp_mad/*.png"
# wind  = "C:/Users/Admin/Documents/Work/2020-Masters/data/seasonal/pre_processed/wind_mad/*.png"

# rain  = "C:/Users/Admin/Documents/Work/2020-Masters/data/seasonal/monthlyAve/rainF_madAve/*.png"
# evap  = "C:/Users/Admin/Documents/Work/2020-Masters/data/seasonal/monthlyAve/rainF_madAve/*.png"
# humid = "C:/Users/Admin/Documents/Work/2020-Masters/data/seasonal/monthlyAve/rainF_madAve/*.png"
# temp  = "C:/Users/Admin/Documents/Work/2020-Masters/data/seasonal/monthlyAve/rainF_madAve/*.png"
# wind  = "C:/Users/Admin/Documents/Work/2020-Masters/data/seasonal/monthlyAve/rainF_madAve/*.png"

# rain  = "/share/people/3400693/data/seasonal/pre_processed/rainF_mad/*.png"
# evap  = "/share/people/3400693/data/seasonal/pre_processed/evap_mad/*.png"
# humid = "/share/people/3400693/data/seasonal/pre_processed/humid_mad/*.png"
# temp  = "/share/people/3400693/data/seasonal/pre_processed/temp_mad/*.png"
# wind  = "/share/people/3400693/data/seasonal/pre_processed/wind_mad/*.png"

rain  = "/share/people/3400693/data/seasonal/monthlyAve/rainF_madAve/*.png"
evap  = "/share/people/3400693/data/seasonal/monthlyAve/evap_madAve/*.png"
humid = "/share/people/3400693/data/seasonal/monthlyAve/humid_madAve/*.png"
temp  = "/share/people/3400693/data/seasonal/monthlyAve/temp_madAve/*.png"
wind  = "/share/people/3400693/data/seasonal/monthlyAve/wind_madAve/*.png"

dirArray = [[rain,"Rain"], [evap,"Evap"], [humid,"Humid"], [temp, "Temp"], [wind, "Wind"]]


########################################################################
########################################################################

def makingDataset (xPathArr, yPathArr,seqLen, numDayAhead):
    DataX = []
    DataY = []
    
    w,h = Image.open(xPathArr[0]).size
    totPixels = w*h
    
    for i in range(len(xPathArr)):
        try:
            nameY = os.path.basename(yPathArr[i+seqLen+numDayAhead]).split(".")
#             print(nameY[0][-1])
            if (nameY[0][-1] != "y"):
                DataX1 = []
                imgX0 = Image.open(xPathArr[i]).convert("L")
                imgXSeq_Numpy = np.array(imgX0)
                DataX1.append (imgXSeq_Numpy)  
                for j in range(seqLen-1):

                    imgX = Image.open(xPathArr[i+j+1]).convert("L")  # to open the image
                    imgX_Numpy = np.array(imgX)#to get the data f the next image in the sequence
                    DataX1.append (imgX_Numpy)

                imgY = Image.open(yPathArr[i+seqLen+numDayAhead]).convert("L")

                DataX.append(( DataX1 )) # append the features n for instance i into a list, this
#                 print(nameY[0][-2:])
                DataY.append([np.array(imgY), int(nameY[0][-2:])] )
                     
        except: # means out of range
            
            return DataX, DataY
        
    return DataX, DataY



# The following function takes the above tensor (array) fromat into a normal data sets with  (54320, 73)
    ## where the 54320 stands for the pixels, and 73 stands for the features, (72 pixels, and plus 1 feat = pixel index
def makingDataset2 (dataX, dataY, feat):

    Data = []
    DataX1 = []
    DataY1 = []
    pixInd_X = []
    pixInd_Y = []
    
    for seq in range (len(dataX)):
        for pixel_i in range (len(dataX[0][0])):
            for pixel_j in range (len(dataX[0][0][0])):
                Data = []
                if (dataY[seq][0][pixel_i][pixel_j] != 0):

                    for time in feat:                    
                        Data.append(np.sqrt(dataX[seq][time][pixel_i][pixel_j]))

                    Data = np.append(Data, [pixel_i , pixel_j, dataY[seq][1]])
                    #Data = np.append(Data, [pixel_i , pixel_j])
                    pixInd_X.append(pixel_i)
                    pixInd_Y.append(pixel_j)
    
                    DataX1.append(Data)
                    DataY1.append(dataY[seq][0][pixel_i][pixel_j])
                    
    return DataX1, DataY1,pixInd_X
        
#########################################################################################        
##########################################################################################

seqLengthArr = [12]
monthAhead = [ 0]
features = [[11], [0], [0, 11], [10, 11], [0, 11, 1,2], [0, 11, 1, 10] ]
     
# features = [[0, 11]]
scv = TimeSeriesSplit(n_splits = 3)
#######################################

n_estimators = [10, 20, 40, 80, 160]
max_features = ['auto','sqrt']
max_depth = [5, 10, 15, 30, None]
min_samples_split = [2, 5, 10, 15]
min_samples_leaf = [1, 2, 5, 10]
# bootstrap = [True]


# param_grid = {
#     'n_estimators':Integer (200, 2000),
#     'max_features': max_features,
#     'max_depth': Integer(2,100),
#     'min_samples_split': min_samples_split,
#     'min_samples_leaf': min_samples_leaf,
# }

param_grid = {
    'n_estimators': n_estimators,
    'max_features': max_features,
    'max_depth': max_depth,
    'min_samples_split': min_samples_split,
    'min_samples_leaf': min_samples_leaf,
}


##########################################

#scorer = make_scorer(mean_squared_error, greater_is_better=False)


estimator = RandomForestRegressor(n_jobs = -1)
#############################################################

for dataInd in range (5):    
    for lag in seqLengthArr:
        for month in monthAhead:
            for feat in features:
                
                yFiles = sorted(glob.glob (dirArray[dataInd][0])) # Change Cell
                xFiles = sorted(glob.glob (dirArray[dataInd][0])) # Change Cell
                
                DataX, DataY = makingDataset(xFiles, yFiles, lag, month)
                print(dirArray[dataInd][1])
                print()
                DataX = np.array(DataX)
                DataY = np.array(DataY)
                print(DataX.shape)
                print(DataY.shape)
                DataXX, DataYY, pixelPOS = makingDataset2(DataX, DataY, feat) 

                DataXX = np.float64(np.array(DataXX))
                DataYY = np.sqrt(np.float64(np.array(DataYY)))

            ################################## splitting the Data #####################################
                XtestImg = DataXX[ -(70*40*60) : ]
                YtestImg = DataYY[  -(70*40*60) : ]
                indexImg = pixelPOS[  -(70*40*60) : ]

                Xtrain = DataXX[0: -(70*40*60)  ]
                Ytrain = DataYY[0: -(70*40*60)  ]
            ###################################################################
                print(DataXX.shape)
                print(DataYY.shape)
                print(Xtrain.shape)
                print(Ytrain.shape)
                print(XtestImg.shape)
        ################################################################################
                print()
                print("Heloo every one,this is a grid search on ("+str(feat)+") features, Month Ahead: "+str(month+1))
                print()

                start_time = time.time()
                reg =  GridSearchCV(estimator, param_grid, cv=scv, scoring = 'neg_mean_absolute_error' ,n_jobs=1, verbose = 1)
                print(reg)
                reg.fit(Xtrain, Ytrain)
                y_predImg = reg.predict(XtestImg)

            ###################################################################################
                print("Best parameters & score set found on development set:")
                print()
                print(reg.best_score_)
                print(reg.best_params_)
                print()
                print("Grid scores on development set:")
                print()
            ##################################################################################
                mae = mean_absolute_error(YtestImg**2, y_predImg**2)
                mse = mean_squared_error(YtestImg**2, y_predImg**2)
                rmse = np.sqrt(mean_squared_error(YtestImg**2, y_predImg**2))
                r2 = r2_score(YtestImg**2, y_predImg**2)
                print()
                print("Testing Set: ")
                print("MAE: " + str(mae))
                print("MSE: " + str(mse))
                print("RMSE: " + str(rmse))
                print("r2score: " + str(r2))
                print()    
                print("--- %s seconds ---" % (time.time() - start_time))    
                print()




