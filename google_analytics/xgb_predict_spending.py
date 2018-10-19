import pandas as pd
import numpy as np

import xgboost as xgb



#X_train = np.load('X_train.dat')
#y_train = np.load('y_train.dat')
#X_test = np.load('X_test.dat')


#try a subset and make sure it works
sub_X_train = X_train[:1000,]
sub_y_train = y_train[:1000]


sub_dtrain = xgb.DMatrix(X_train, y_train)

y_median = np.median(y_train) #this is the baseline prediction, the mean

np.mean(y_train)
len([x for x in y_train if x > 0])

#possibly switch this to the median

xgb_params = {'eta' :  0.05,
                'max_depth' :  8,
                'subsample' : 0.80, 
                'objective' :  'reg:linear',
                'eval_metric' : 'rmse',
                'base_score' :  y_median,}


#before cv, can try with just a super simple train to make sure it is working
test_model = xgb.train(xgb_params, sub_dtrain, 
                  num_boost_round = 200,
                  verbose_eval=10)



#####
#
# put the model training here
#
#####


#tried to bring x train and y train down to a more reasonable size
#or use batches - did this and the model ran.. so its a scale things

#ideas:
# set xgb up for a batch workflow
# run it on kaggle and use their ram/cpu
# downsample the 0s, so only the rows that led to revenue and maybe 5% of 1s


dtrain = xgb.DMatrix(X_train, y_train)
dtest = xgb.DMatrix(X_test)

y_mean = np.mean(y_train) #this is the baseline prediction, the mean
y_median = np.median(y_train) #this is the baseline prediction, the mean

#possibly switch this to the median

xgb_params = {'eta' :  0.05,
                'max_depth' :  8,
                'subsample' : 0.80, 
                'objective' :  'reg:linear',
                'eval_metric' : 'rmse',
                'base_score' :  y_median,}











########################################################
# model work - need to scale with the data
#before cv, can try with just a super simple train to make sure it is working
test_model = xgb.train(xgb_params, dtrain, 
                  num_boost_round = 200,
                  verbose_eval=1)


cv_result = xgb.cv(xgb_params, dtrain, 
					nfold=5, 
					num_boost_round=10, 
					#early_stopping_rounds=50, 
					verbose_eval=1, show_stdv=False)

#if works, swtict to

cv_result = xgb.cv(xgb_params, dtrain, 
					nfold=5, 
					num_boost_round=2000, 
					early_stopping_rounds=50, 
					verbose_eval=0, show_stdv=False)


num_boost_rounds = len(cv_result)

#traing the model on the full all_train dataset
model = xgb.train(xgb_params, dtrain, 
                  num_boost_round = num_boost_rounds)


#####################################################################

#make predictions on the test data

test_y = model.predict(X_test)

# sum the predictions using the defined formula to get a revenue by user metric
# aggregate on 'fullVisitorId' 
# final_test['fullVisitorId' ]


#group by id
final_by_ind =  final_pred.groupby(['fullVisitorId']).sum()
#move index to a col
final_by_ind = final_by_ind.reset_index()

#merge the predictions with the sample sub
submission = submission.merge(final_by_ind, on = 'fullVisitorId', how = 'left')
#fill nas and move to right column name
submission['PredictedLogRevenue'] = submission['test_pred'].fillna(0.0)
submission = submission.drop(['test_pred'], axis = 1)

#submit the output
submission.to_csv('cam_lightgbm_pred2.csv', index = False)
#1.78 first go


