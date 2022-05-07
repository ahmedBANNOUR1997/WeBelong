
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from keras.callbacks import EarlyStopping
from sklearn.metrics import accuracy_score

df = pd.read_csv("bully_dataset_final.csv", encoding = "ISO-8859-1")


def bq1_to_numeric(x):
    if x == 'a loser, he doesnt know how to defend himself': return 1
    if x == 'i dont wanna be in his place':   return 2
    if x == 'it s not my business':   return 3
    if x == 'he is not feeling ok':   return 4


def bq2_to_numeric(x):
    if x == 'nothing': return 1
    if x == 'funny':   return 2
    if x == 'i pitty him':   return 3
    if x == 'angry towards the aggressor':   return 4
    if x == 'sad, reminded me of myself':   return 5
    if x == 'enjoying his suffering':   return 6


def bq3_to_numeric(x):
    if x == 'nothing': return 1
    if x == 'complain to the dean':   return 2
    if x == 'stand up to the bully':   return 3
    if x == 'talk to the parents':   return 4
    if x == 'join the bully':   return 5


def q1_to_numeric(x):
    if x == 'the victim is so weak': return 1
    if x == 'nothing, its not my problem':   return 2
    if x == 'i shouldnt have let this go this far':   return 3
    if x == 'i think i did good':   return 4
    if x == 'bullying is a bad thing':   return 5
    if x == 'weak people need help and protection from bullying':   return 6


def q2_to_numeric(x):
    if x == 'Still having fun': return 1
    if x == 'i feel regret and shame':   return 2
    if x == 'Nothing at all':   return 3
    if x == 'Im proud of myself':   return 4
    if x == 'i feel that ive accomplished something':   return 5
    if x == 'i feel like a hero':   return 6


def q3_to_numeric(x):
    if x == 'act like nothing ever happened': return 1
    if x == 'ask for forgiveness for not being able to stop it':   return 2
    if x == 'continue having fun and bullying mohamed and other people as well':   return 3
    if x == 'From now on, help weak people against aggressors ':   return 4
    if x == 'Bully anyone whos different than me':   return 5
    if x == 'do nothing, its not my business to begin with':   return 6


def r_to_numeric(x):
    if x == 'Supportive': return 1
    if x == 'AGRESSIVE':   return 2
    if x == 'Passive':   return 3
    if x == 'HasExperiencedBullying +Supportive':   return 4
    if x == 'HasExperiencedBullying + AGRESSIVE':   return 5
    if x == 'HasExperiencedBullying + Passive':   return 6
    if x == 'Empathetic':   return 7
    if x == 'HasExperiencedBullying':   return 8


results_array = ['Supportive', 'AGRESSIVE', 'Passive', 'HasExperiencedBullying +Supportive',
                 'HasExperiencedBullying + AGRESSIVE', 'HasExperiencedBullying + Passive', 'Empathetic',
                 'HasExperiencedBullying']

# prepare dataset
df['bq1_num'] = df['What did you think ?'].apply(bq1_to_numeric)
df['bq2_num'] = df['How do you feel  ?'].apply(bq2_to_numeric)
df['bq3_num'] = df['What should you do ?'].apply(bq3_to_numeric)
df['q1_num'] = df['Question 1'].apply(q1_to_numeric)
df['q2_num'] = df['Question 2'].apply(q2_to_numeric)
df['q3_num'] = df['Question 3'].apply(q3_to_numeric)
df['r_num'] = df['Result'].apply(r_to_numeric)

#split dataset
X = df[['bq1_num','bq2_num','bq3_num','q1_num','q2_num','q3_num']]
Y = df['r_num']
#split between training and validation
x_train, x_test, y_train, y_test = train_test_split(X,Y, test_size=0.20,random_state=30)

#first model
lr = LogisticRegression(max_iter=5000)
lr.fit(x_train , y_train)
y_pred_lr=lr.predict(x_test)
accuracy_score(y_test, y_pred_lr, normalize=True, sample_weight=None)

#second model
dt = DecisionTreeClassifier(max_depth=4, max_features=None, min_samples_leaf = 3)
dt.fit(x_train,y_train)
y_pred_dt=dt.predict(x_test)
accuracy_score(y_test, y_pred_dt, normalize=True, sample_weight=None)

#Test
my_answers=[[4,2,3,2,4,3]]
columns=['bq1_num','bq2_num','bq3_num','q1_num','q2_num','q3_num']
myrep=pd.DataFrame(my_answers,columns=columns)
print(results_array)
print('prediction of first model')
print(results_array[lr.predict(myrep)[0]-1])
print(lr.predict_proba(myrep))
print('prediction of second model')
print(results_array[dt.predict(myrep)[0]-1])
print(dt.predict_proba(myrep))


