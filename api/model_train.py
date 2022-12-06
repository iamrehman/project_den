import pandas as pd
import pickle
from fastapi import APIRouter
from .request import ModelRequest

router = APIRouter()

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression

from sklearn.model_selection import train_test_split

from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score


@router.get(
    "/train_model",
    summary="Train ML model"
)
def train_model(request: ModelRequest):
    """Model Training API"""
    model = None
    if request.model == "DecisionTreeClassifier":
        model = DecisionTreeClassifier(**request.parameters)
    elif request.model == "RandomForestClassifier":
        model = GradientBoostingClassifier(**request.parameters)
    else:
        model = LogisticRegression(**request.parameters)

    #  load and split the dataset
    df = pd.read_csv("final_resume_data.csv")
    y = df.pop("Hired")
    X = df

    features = ['Hourly_Rate', 'Notice_Period', 'Operation_Mode', 'Test_Score',
                'Interview_Score']
    X_train, X_test, y_train, y_test = train_test_split(X[features], y, test_size=0.33, random_state=42, stratify=y)

    # Train the model
    print("*********Training ", request.model, " ****************")
    model = model.fit(X_train, y_train)

    # Save the trained model
    print("*********Saving the trained model ", request.model, " ****************")

    filename = 'trained_model.pkl'
    pickle.dump(model, open(filename, 'wb'))

    print("**********Calculating results on evaluation metrics**********")

    yhat = model.predict(X_test)

    # evaluate predictions
    precision = precision_score(y_test, yhat)
    recall = recall_score(y_test, yhat)
    f1 = f1_score(y_test, yhat)
    acc = accuracy_score(y_test, yhat)

    print('accuracy: %.3f' % acc)
    print('precision: %.3f' % precision)
    print('recall: %.3f' % recall)
    print('f1_score: %.3f' % f1)

    return {"accuracy": acc,
            "precision": precision,
            "recall": recall,
            "f1_score": f1
            }
