import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score
from sklearn.metrics import recall_score, f1_score, classification_report
from sklearn.metrics import confusion_matrix, precision_recall_fscore_support

from imblearn.over_sampling import RandomOverSampler, SMOTE, ADASYN

from sklearn import tree
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score

import preparing_data
import pca_func
import common
from trees_classifiers import model_RandomForest_fit, model_tree_fit
from nn_classifier import get_nn_model, loss_graph, fit_nn_model
from regression import model_logistic_regression, Logic_regression_graph
from grad_boost import model_GradBoost

#  -------  Read data from CSV --------
train_data = pd.read_csv('finance_train.csv')
test_data = pd.read_csv('finance_test.csv')

#  ------- Cutting outliers for real features  --------
train_data, test_data = preparing_data.features_cut(train_data,test_data,\
                                                    plot=False)
#  ------- Separate data on X,y  --------
X,y,X_test,y_test,y_ini,y_test_ini,y_pos,y_test_pos = \
    preparing_data.X_y_data(train_data,test_data,\
                            y_lab = 'negative')

#  ------- Norm X - for real and catecorical features  --------
X_norm, X_test_norm = preparing_data.norm_data(X,X_test,y_pos,y_test_pos,\
                                               real='standart',\
                                               categ='target',\
                                               all = True)
#  ------- Used it for cros-val  --------
#X_train, X_dev, y_train, y_dev = train_test_split(X_norm,y, random_state = 228)

#  ------- Used it for study influence of sampling  --------
#X_replaced, y_replaced  = RandomOverSampler(random_state=228).fit_resample(X_train, y_train)
X_replaced, y_replaced = SMOTE(random_state=228, k_neighbors=5).fit_resample(X_train, y_train)
#X_replaced, y_replaced = ADASYN(random_state=228, n_neighbors=4).fit_resample(X_norm, y_train)X_train = X_replaced

X_train = X_replaced
y_train = y_replaced

#  ------- Used it for study influence of pca  --------
X_pca, X_test_pca = pca_func.pca(X_train,X_test, 55)
X_train = X_pca
X_test = X_test_pca


def main_body (X_train,y_train,X_test, y_test, \
               X_dev = None, y_dev = None):
    file_out = open('result.res', 'w')

    # ------- Descision Tree -------
    '''
    dtc = tree.DecisionTreeClassifier(random_state=228, max_depth =5)
    file_out.write ('Tree\n')
    file_out.write(str(cross_val_score(dtc, X_train, y_train, scoring='recall',\
                                       cv =5).mean()))

    file_out.write ('\n')
    '''
    # ------- Random Forest -------
    '''
    rf = RandomForestClassifier(n_estimators=32, max_depth=5, random_state=228)
    file_out.write ('Random Forest\n')
    file_out.write(str(cross_val_score(rf, X_train, y_train, scoring='recall',\
                                       cv =5).mean()))
    file_out.write ('\n')
    '''

    # ------- Neural Network -------
    '''
    nn = get_nn_model(X_train.shape[1])
    print(cross_val_score(rf, X_train, y_train, scoring='recall',fit_params =).mean())
    '''

    # ------- Logistic Regression -------
    '''
    lr =LogisticRegression(C=1, class_weight=None,\
                           penalty = 'l2',random_state=228)
    file_out.write('Logistic Regression\n')
    file_out.write(str(cross_val_score(lr, X_train, y_train, scoring='recall',\
                                       cv =5).mean()))
    file_out.write ('\n')
    '''

    # ------- Gradint Boosting -------
    '''
    gb = GradientBoostingClassifier(n_estimators=64, max_depth=1,
                                 random_state=228)
    file_out.write('Gradient Boosting\n')
    file_out.write(str(cross_val_score(gb, X_train, y_train, scoring='recall',\
                                       cv =5).mean()))
    file_out.write ('\n')
    '''
    
    file_out.write('----AdaBoost----\n')
    abdt = model_Ada(X_train,y_train,X_dev, y_dev,file_out,n_estimators=64,depth=1)
    
    
    file_out.write('----CatBoost----\n')
    cb = model_CatBoost(X_train,y_train,X_test, y_test,file_out, iterations=232, \
                        learn_rate = 0.5, depth=5)
    #preparing_data.draw_objects(X_dev,y_dev,cb)
    '''
    

    #  -------------- Part with grapths for each model --------------
    #Tree_graph(X_train, y_train, X_test, y_test,file_out,'',\
    #           X_dev= None,y_dev=None,\
    #           max_depth=100)
    
    #RandomForest_graph(28,7,X_train,y_train, X_test, y_test,file_out, '')

    #Logic_regression_graph(X_train, y_train, X_test, y_test,file_out,'',\
    #                       X_dev= None,y_dev=None,\
    #                       flag_degree=False, degree=2, C=0.01)

    
    file_out.close()

####### X_test_norm, y_test   #X_test_pca, y_test
####### X_train_dev, y_train_dev
####### X_dev, y_dev

main_body(X_train,y_train,X_test, y_test)

