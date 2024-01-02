import pandas as pd

data = pd.read_csv('./dataset/heart.csv')

data.head()

data.isnull().sum()

data.shape

data.dtypes

corrmat = data.corr()

import seaborn as sns

sns.heatmap(corrmat)

features = data.drop('output', axis = 1)
target = data['output']

from sklearn.model_selection import train_test_split

xTrain, xTest, yTrain, yTest = train_test_split(features, target)

from sklearn import linear_model

logreg = linear_model.LogisticRegression()

logreg.fit(xTrain,yTrain)

prediction = logreg.predict(xTest)

from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, f1_score

accuracy = accuracy_score(yTest, prediction)
print(accuracy)

confusion_matrix(yTest, prediction)

print(precision_score(yTest, prediction))
print(recall_score(yTest, prediction))
print(f1_score(yTest, prediction))

from sklearn.tree import DecisionTreeClassifier

treeModel = DecisionTreeClassifier()

treeModel.fit(xTrain, yTrain)

treePred = treeModel.predict(xTest)

accuracy_score(yTest,treePred)

confusion_matrix(yTest,treePred)

print(precision_score(yTest, treePred))
print(recall_score(yTest, treePred))
print(f1_score(yTest, treePred))

from sklearn.ensemble import RandomForestClassifier

forestModel = RandomForestClassifier()

forestModel.fit(xTrain, yTrain)

forestPred = forestModel.predict(xTest)
accuracy_score(yTest, forestPred)

confusion_matrix(yTest, forestPred)

print(precision_score(yTest, forestPred))
print(recall_score(yTest, forestPred))
print(f1_score(yTest, forestPred))

from sklearn.ensemble import AdaBoostClassifier
adaModel = AdaBoostClassifier()
adaModel.fit(xTrain,yTrain)

adaPred = adaModel.predict(xTest)

accuracy_score(yTest, adaPred)


# In[36]:


confusion_matrix(yTest, adaPred)


# In[50]:


print(precision_score(yTest, adaPred))
print(recall_score(yTest, adaPred))
print(f1_score(yTest, adaPred))


# In[58]:


#hyperparameter tuning...
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.model_selection import GridSearchCV
tuneLogreg = linear_model.LogisticRegression()
solvers = ['newton-cg', 'lbfgs', 'liblinear']
penalty = ['l2']
c_values = [100, 10, 1.0, 0.1, 0.01]
# define grid search
grid = dict(solver=solvers, penalty=penalty, C=c_values)
cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=1)
grid_search = GridSearchCV(estimator=tuneLogreg, param_grid=grid,
                           n_jobs=-1, cv=cv, scoring='accuracy', error_score=0)
grid_result = grid_search.fit(xTrain, yTrain)
# summarize results
print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))
means = grid_result.cv_results_['mean_test_score']
stds = grid_result.cv_results_['std_test_score']
params = grid_result.cv_results_['params']
for mean, stdev, param in zip(means, stds, params):
    print("%f (%f) with: %r" % (mean, stdev, param))


# In[ ]:


tunedModel = linear_model.LogisticRegression(penalty='l2',solver='lbfgs', C = 0.1)
tunedModel.fit(xTrain,yTrain)
prediction = tunedModel.predict(xTest)

print(accuracy_score(yTest, prediction))
print(precision_score(yTest, prediction))
print(recall_score(yTest, prediction))
print(f1_score(yTest, prediction))


# In[2]:


get_ipython().system('jupyter nbconvert --to script pipeline.ipynb')


# In[ ]:




