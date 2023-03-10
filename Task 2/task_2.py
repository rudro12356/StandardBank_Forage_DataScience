# -*- coding: utf-8 -*-
"""Task_2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1aY6ikdibJGUAxQ_K-veeV7hae1iGfw9I

# Task 2 

## Credit / Home Loans - AutoML vs Bespoke ML

Standard Bank is embracing the digital transformation wave and intends to use new and exciting technologies to give their customers a complete set of services from the convenience of their mobile devices.
As Africa’s biggest lender by assets, the bank aims to improve the current process in which potential borrowers apply for a home loan. The current process involves loan officers having to manually process home loan applications. This process takes 2 to 3 days to process upon which the applicant will receive communication on whether or not they have been granted the loan for the requested amount.
To improve the process Standard Bank wants to make use of machine learning to assess the credit worthiness of an applicant by implementing a model that will predict if the potential borrower will default on his/her loan or not, and do this such that the applicant receives a response immediately after completing their application. 

You will be required to follow the data science lifecycle to fulfill the objective. The data science lifecycle (https://www.datascience-pm.com/crisp-dm-2/) includes:

- Business Understanding
- Data Understanding
- Data Preparation
- Modelling
- Evaluation
- Deployment.

You now know the CRoss Industry Standard Process for Data Mining (CRISP-DM), have an idea of the business needs and objectivess, and understand the data. Next is the tedious task of preparing the data for modeling, modeling and evaluating the model. Luckily, just like EDA the first of the two phases can be automated. But also, just like EDA this is not always best. 


In this task you will be get a taste of AutoML and Bespoke ML. In the notebook we make use of the library auto-sklearn/autosklearn (https://www.automl.org/automl/auto-sklearn/) for AutoML and sklearn for ML. We will use train one machine for the traditional approach and you will be required to change this model to any of the models that exist in sklearn. The model we will train will be a Logistic Regression. Parts of the data preparation will be omitted for you to do, but we will provide hints to lead you in the right direction.

The data provided can be found in the Resources folder as well as (https://www.kaggle.com/datasets/altruistdelhite04/loan-prediction-problem-dataset).

- train will serve as the historical dataset that the model will be trained on and,
- test will serve as unseen data we will predict on, i.e. new ('future') applicants.

### Part One

There are many AutoEDA Python libraries out there which include:

- dtale (https://dtale.readthedocs.io/en/latest/)
- pandas profiling (https://pandas-profiling.ydata.ai/docs/master/index.html)
- autoviz (https://readthedocs.org/projects/autoviz/)
- sweetviz (https://pypi.org/project/sweetviz/)

and many more. In this task we will use Sweetviz.. You may be required to use bespoke EDA methods.

The Home Loans Department manager wants to know the following:

1. An overview of the data. (HINT: Provide the number of records, fields and their data types. Do for both).

2. What data quality issues exist in both train and test? (HINT: Comment any missing values and duplicates)

3. How do the the loan statuses compare? i.e. what is the distrubition of each?

4. How do women and men compare when it comes to defaulting on loans in the historical dataset?

5. How many of the loan applicants have dependents based on the historical dataset?

6. How do the incomes of those who are employed compare to those who are self employed based on the historical dataset? 

7. Are applicants with a credit history more likely to default than those who do not have one?

8. Is there a correlation between the applicant's income and the loan amount they applied for? 

### Part Two

Run the AutoML section and then fill in code for the traditional ML section for the the omitted cells.

Please note that the notebook you submit must include the analysis you did in Task 2.

## Import Libraries
"""

!pip3 install sweetviz 
# uncomment the above if you need to install the library 
!pip3 install auto-sklearn
# uncomment the above if you need to install the library

!pip install --upgrade scipy

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sweetviz 
import autosklearn.classification
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.impute import SimpleImputer

"""## Import Datasets"""

train = pd.read_csv('train.csv')
test = pd.read_csv('test.csv')

"""# Part One

## EDA
"""

train.head()

test.head()

# we concat for easy analysis
n = train.shape[0] # we set this to be able to separate the
df = pd.concat([train, test], axis=0)
df.head()

"""### Sweetviz"""

autoEDA = sweetviz.analyze(train)
autoEDA.show_notebook()

"""### Your Own EDA 

"""

autoEDA = sweetviz.analyze(test)
autoEDA.show_notebook()

df.describe()

"""## 1. Answer:"""

df.info()

"""## 2. Answer:

### There's only missing values for some of the columns such as Gender, Married, Dependants ...
### There's no duplicate
"""

df.isnull().sum()

df.duplicated().sum()

"""## 3. Answer: Let's do a plot to see the distribution of the loan status column

### The number of people getting Loan is significantly higher than the ones being rejected as per the bar chart.
"""

df['Loan_Status'].value_counts().plot.bar(rot=0)

"""## 4.Answer:"""

df

# Create the bar chart
sns.countplot(x='Gender', hue='Loan_Status', data=df)
plt.legend(title='Loan_Status')

# Show the plot
import matplotlib.pyplot as plt
plt.show()

df.dtypes

"""### It seems men have more positive loan status than women.

### 5. Answer
"""

df['Dependents'].isnull().sum()

df['Dependents'].value_counts().plot.bar(rot=0)

"""### It seems roughly 150 applicants have 1 dependent, another batch of 150 people have 2 dependents, and roughly 90 of the applicants have more than 3 dependents. Therefore, 390 applicants have dependents. We also need to consider that there are 25 missing values in the Dependents column.

## 6.Answer:
"""

df

# df.dtypes
# Let's see a plot between the Self_employed column and the ApplicantIncome column

# Group by 'Self_Employed' and sum the income values
grouped = df.groupby('Self_Employed')['ApplicantIncome'].sum()

plt.xlabel('Self Employed')
plt.ylabel('Income')
plt.title('Income by Employment')

# Plot the grouped data
grouped.plot(kind='bar')
plt.show()

"""### As we can see, using groupby menthod helped us to get an insight which shows that people who are not self employed have a significantly higher income.

## 7.Answer:
"""

# let's check for missing values
df['Credit_History'].isnull().sum()

# it seems 1.0 and 0.0 are default credit history values
df['Credit_History'].unique()

# Create the bar chart
sns.countplot(x='Credit_History', hue='Loan_Status', data=df)
plt.legend(title='Credit history vs Loan Status')

# Show the plot
import matplotlib.pyplot as plt
plt.show()

"""### It seems applicants who have a credit history of 1.0 have higher No loan status.

## Auto ML wth autosklearn
"""

df.dtypes

# Matrix of features

X = train[['Gender',
'Married',
'Dependents',
'Education',
'Self_Employed',
'ApplicantIncome',
'CoapplicantIncome',
'LoanAmount',
'Loan_Amount_Term',
'Credit_History',
'Property_Area']]

# convert string(text) to categorical
X['Gender'] = X['Gender'].astype('category')
X['Married'] = X['Married'].astype('category')
X['Education'] = X['Education'].astype('category')
X['Dependents'] = X['Dependents'].astype('category')
X['Self_Employed'] = X['Self_Employed'].astype('category')
X['Property_Area'] = X['Property_Area'].astype('category')


# label encode target
y = train['Loan_Status'].map({'N':0,'Y':1}).astype(int)


# # train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# train
autoML = autosklearn.classification.AutoSklearnClassifier(time_left_for_this_task=2*30, per_run_time_limit=30, n_jobs=8) # imposing a 1 minute time limit on this
autoML.fit(X_train, y_train)

# predict
predictions_autoML = autoML.predict(X_test)

print('Model Accuracy:', accuracy_score(predictions_autoML, y_test))

print(confusion_matrix(predictions_autoML, y_test))

predictions_autoML.shape

y_test.shape

conf_mat = confusion_matrix(predictions_autoML, y_test)

sns.heatmap(conf_mat, annot=True)
plt.show()

"""## Bespoke ML sklearn

### Data Preparation
"""

df.dtypes
df.isnull().sum()

df_new = df.drop(columns=['Loan_ID'])
df_new.info()

df_new.dropna()

# Matrix of features

df = train[['Gender',
'Married',
'Education',
'Self_Employed',
'ApplicantIncome',
'CoapplicantIncome',
'LoanAmount',
'Loan_Amount_Term',
'Credit_History']]


# imputing the missing values:
df['Gender'].fillna(df['Gender'].mode()[0], inplace = True)
df['Married'].fillna(df['Married'].mode()[0], inplace = True)
df['Self_Employed'].fillna(df['Self_Employed'].mode()[0], inplace = True)
df['Credit_History'].fillna(df['Credit_History'].mode()[0], inplace = True)

# encoding categorical features
df['Gender'] = df['Gender'].map({'Male':0,'Female':1}).astype(int)
df['Married'] = df['Married'].map({'No':0,'Yes':1}).astype(int)
df['Education'] = df['Education'].map({'Not Graduate':0,'Graduate':1}).astype(int)
df['Self_Employed'] = df['Self_Employed'].map({'No':0,'Yes':1}).astype(int)
df['Credit_History'] = df['Credit_History'].astype(int)


df['LoanAmount'].fillna(df['LoanAmount'].mean(), inplace = True)
df['Loan_Amount_Term'].fillna(df['Loan_Amount_Term'].mean(), inplace = True)
 
X = df.copy()

# label encode target
y = train['Loan_Status'].map({'N':0,'Y':1}).astype(int)


# train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

!pip install scikit-learn-pipeline-utils

# train
from sklearn.ensemble import RandomForestClassifier
clf_1 = RandomForestClassifier() #change model here
clf_1.fit(X_train, y_train)

# predict
predictions_clf = clf_1.predict(X_test)

print('Model Accuracy:', accuracy_score(predictions_clf, y_test))

print(classification_report(predictions_clf, y_test))

print(confusion_matrix(predictions_clf, y_test))

from sklearn.metrics import roc_auc_score

r_auc = roc_auc_score(predictions_clf, y_test)
print("AUC score is ", r_auc)

from sklearn.neighbors import KNeighborsClassifier
clf_2 = KNeighborsClassifier(n_neighbors=3)
clf_2.fit(X_train, y_train)

# predict
predictions_clf_2 = clf_2.predict(X_test)

print('Model Accuracy:', accuracy_score(predictions_clf_2, y_test))

print(classification_report(predictions_clf_2, y_test))

print(confusion_matrix(predictions_clf_2, y_test))

from sklearn import tree
clf_3 = tree.DecisionTreeClassifier(criterion = "gini",
            random_state = 100,max_depth = 10)
clf_3.fit(X_train, y_train)

# predict
predictions_clf_3 = clf_3.predict(X_test)

print('Model Accuracy:', accuracy_score(predictions_clf_3, y_test))

print(classification_report(predictions_clf_3, y_test))

print(confusion_matrix(predictions_clf_3, y_test))

from sklearn.ensemble import VotingClassifier

eclf1 = VotingClassifier(estimators=[('rf', clf_1), ('knn', clf_2), ('dt', clf_3)], voting='soft')
eclf1.fit(X_train, y_train)
predictions_new = eclf1.predict(X_test)

print(classification_report(y_test, predictions_new))

from sklearn.model_selection import cross_val_score
c = []
c.append(cross_val_score(clf_1,X_train,y_train,scoring='accuracy',cv=10).mean())
c.append(cross_val_score(clf_2,X_train,y_train,scoring='accuracy',cv=10).mean())
c.append(cross_val_score(clf_3,X_train,y_train,scoring='accuracy',cv=10).mean())

print(c)

# class 1 should be the winner with the better accuracy!