

import xgboost
import pickle

!gsutil cp gs://jaa-bucket2/quora/xgb_pickle /Users/jonahadler/Desktop/code/Quora
import os
gc_dir = "/quora/"
file = "y_test"
local_dir = "/Users/jonahadler/Desktop/code/Quora/"
def unpickle_gc(file, gc_dir,local_dir):
    os.system("gsutil cp gs://jaa-bucket2"+ gc_dir+file +" "+local_dir)
    with open(local_dir+file, 'rb') as f:
        content = pickle.load(f)
    return content

y_test = unpickle_gc("y_test","/quora/","/Users/jonahadler/Desktop/code/Quora/")
model = unpickle_gc("xgb_pickle","/quora/","/Users/jonahadler/Desktop/code/Quora/")
X_test = unpickle_gc("X_test","/quora/","/Users/jonahadler/Desktop/code/Quora/")
data = unpickle_gc("Quora_featured","/quora/","/Users/jonahadler/Desktop/code/Quora/")


joined = data.join(X_test, how="inner",lsuffix = "l")
test_questions = joined[["question1","question2"]]

X_test = X_test.dfet_index(drop=True)
y_test = y_test.dfet_index(drop=True)

y_hat = model.predict(X_test)
y_hat
df=  y_test.copy()

df.columns = ["Actual"]
df["Pred"] = y_hat
df["Correct"] = ((2*(df.Pred-.5))*(2*(df.Actual-.5))+1)/2

df = df.join(test_questions,how="inner")
df["prob"] = model.predict_proba(X_test)[:,0]


errors = df[df.Correct==0]

#need:
#1) convert text to predictor vector
#2) first (faster) (just word 2 vec) pass filtering algo? -> so that we dont have create interquestion features between new question and entire dataset
#3) predcit probabilities for those that made it through 2)
#4) create suggestion list based on predictied probabilites from 3)
