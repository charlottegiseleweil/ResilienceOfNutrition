import pandas as pd
import numpy as np
import os

import pickle
from sklearn.preprocessing import PolynomialFeatures
import sklearn.metrics

def make_polynomial(df, response_variable ='log_calories_per_ha',
                    degree = 2, interaction_terms = True):
    '''Returns a new dataFrame with added polynomial terms degree >= 2'''


    if interaction_terms == False:
        x = df.drop([response_variable], axis=1)
        y = df[response_variable]

        for deg in range(2,degree+1):
            for col in x.columns:
                x[str(col+'^'+str(deg))] = x[col].apply(lambda x:x**deg)
        
        Poly_df = x.merge(pd.DataFrame(y),right_index=True,left_index=True)

    if interaction_terms == True:
        x = df.drop([response_variable], axis=1)
        y = df[response_variable].reset_index()

        poly = PolynomialFeatures(degree=degree, include_bias=False)
        X2 = poly.fit_transform(x)

        Poly_df = pd.DataFrame(data = np.concatenate((y.as_matrix(),X2),axis=1),
                               columns = ['pixel_id',response_variable] +
                               poly.get_feature_names((df.drop([response_variable], axis=1)).columns))

        Poly_df = Poly_df.set_index('pixel_id')

    return Poly_df


def save_model(filename):
    '''Save the model to disk (once fitted)'''
    pickle.dump(regression, open(filename, 'wb'))

def load_regression(modelnm):
    model_filename = '../Data/intermediate/Models/'+modelnm+'.sav'
    regression = pickle.load(open(model_filename, 'rb'))
    return regression


def fit_n_save_model(DF_train,DF_test,
                     ###X_test,Y_test,
                     model,regression,
                     inputs,inputnm,
                     results_df=pd.DataFrame(columns=['Model','Validation_R2','Validation_MSE','inputs'])):
    '''Watch out, doesn't work  with subsets for Poly'''
    
    if model == 'Poly':
        print('Preparing polynomial dataset')
        DF_train = make_polynomial(DF_train)
        DF_test = make_polynomial(DF_test)    
    
    X_train = DF_train.drop(['log_calories_per_ha'], axis=1)
    y_train = DF_train['log_calories_per_ha']
    
    X_test = DF_test.drop(['log_calories_per_ha'], axis=1)
    Y_test = DF_test['log_calories_per_ha']
    
    print('Fitting model '+model)
    regression.fit(X_train, y_train)
    
    print('Saving model '+model)
    filename ='../Data/intermediate/Models/'+model+'_'+inputnm+'.sav'
    pickle.dump(regression, open(filename, 'wb'))
    
    print('Running model '+model+' on test set')
    if model == 'Poly':
        y_predicted = regression.predict(X_test)
    else:
        y_predicted = regression.predict(X_test[inputs])
    
    print('Save '+model+' scores')
    R2_validation = sklearn.metrics.r2_score(Y_test, y_predicted)
    MSE_validation = sklearn.metrics.mean_squared_error(Y_test, y_predicted)

    results_df = results_df.append({'Model':model,
                                          'Validation_R2':R2_validation,
                                          'Validation_MSE':MSE_validation,
                                         'inputs': inputs
                                         },ignore_index=True)
    return results_df

def fit_n_save_model2(DF_train,DF_test,
                     ###X_test,Y_test,
                     model,regression,
                     inputs,inputnm,
                     results_df=pd.DataFrame(columns=['Model','Validation_R2','Validation_MSE','inputs'])):
    '''Watch out, doesn't work  with subsets for Poly'''
    
    if model == 'Poly':
        print('Preparing polynomial dataset')
        DF_train = make_polynomial(DF_train)
        DF_test = make_polynomial(DF_test)    
    
    X_train = DF_train.drop(['log_calories_per_ha'], axis=1)
    y_train = DF_train['log_calories_per_ha']
    
    X_test = DF_test.drop(['log_calories_per_ha'], axis=1)
    Y_test = DF_test['log_calories_per_ha']
    
    print('Fitting model '+model)
    regression.fit(X_train, y_train)
    
    print('Saving model '+model)
    save_model('../Data/intermediate/Models/'+model+'_'+inputnm+'.sav')
    
    print('Running model '+model+' on test set')
    if model == 'Poly':
        y_predicted = regression.predict(X_test)
    else:
        y_predicted = regression.predict(X_test[inputs])
    
    print('Save '+model+' scores')
    R2_validation = sklearn.metrics.r2_score(Y_test, y_predicted)
    MSE_validation = sklearn.metrics.mean_squared_error(Y_test, y_predicted)

    results_df = results_df.append({'Model':model,
                                          'Validation_R2':R2_validation,
                                          'Validation_MSE':MSE_validation,
                                         'inputs': inputs
                                         },ignore_index=True)
    return results_df


def make_results_df(modelnm,X,y=None,y_2000=None):
    
    ## Check if exists already, just load the csv:
    if (modelnm+'.csv') in os.listdir('../Data/outputs/Model_results/2000'):
        compare = pd.read_csv('../Data/outputs/Model_results/2000/'+modelnm+'.csv')
        compare = compare.set_index('pixel_id')

    ## If not, make it and save it:
    else:
        print('Applying '+modelnm)
        regression = load_regression(modelnm)
        y_predicted = regression.predict(X)

        print('Saving model results for '+modelnm)
        compare = predictions_df(y_predicted,y,y_2000)
        compare.to_csv('../Data/outputs/Model_results/2000/'+modelnm+'.csv')
    
    return compare


def predictions_df(y_predicted,y=None,y_2000=None):
    '''ça a l'air compliqué mais ça l'est pas'''
    
    compare = pd.DataFrame()
    
    if type(y)==pd.core.series.Series:
        compare['log(cal_per_ha) measured'] = y
        compare['cal_per_ha measured'] = compare['log(cal_per_ha) measured'].apply(lambda x: np.exp(x))
    
    if type(y_2000)==pd.core.series.Series:
        compare['log(cal_per_ha) in 2000'] = y
        compare['cal_per_ha in 2000'] = y.apply(lambda x: np.exp(x))      
    
    compare['log(cal_per_ha) predicted'] = y_predicted
    compare['cal_per_ha predicted'] = compare['log(cal_per_ha) predicted'].apply(lambda x: np.exp(x))
    
    if type(y)==pd.core.series.Series:    
        compare['prediction error (log)'] = compare['log(cal_per_ha) predicted'] - compare['log(cal_per_ha) measured']
        compare['prediction diff (not log)'] = compare['cal_per_ha predicted'] - compare['cal_per_ha measured']
 
    if type(y_2000)==pd.core.series.Series:    
        compare['Δlog(cal_per_ha)'] = compare['log(cal_per_ha) predicted'] - compare['log(cal_per_ha) in 2000']
        compare['Δcal_per_ha'] = compare['cal_per_ha predicted'] - compare['cal_per_ha in 2000']

    return compare
