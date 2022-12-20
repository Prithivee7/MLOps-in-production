import os
from azureml.core.run import Run
import argparse
import re
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
import joblib



class TitanicSurvivalPrediction():
    def __init__(self, args):
        '''
            From the Run object we can get the context and from that we can get the workspace.
            This can be used to store runs, images, generated files and metrics.
        '''
        self.args = args
        self.run = Run.get_context()
        self.workspace = self.run.experiment.workspace
        os.makedirs('./model_metas', exist_ok=True)
    
    """
        Make an API call to get the data for training and testing.
        For production systems data can be from datastore, databases etc.,  
    """
    def get_data(self):
        # Enter your logic to get data.
        pass

    def preprocess_data(self,train_data,test_data):
        features_drop = ['PassengerId', 'Name', 'Cabin', 'Ticket']
        x_train = train_data.drop(features_drop, axis=1)
        y_train = train_data['Survived']
        x_train.drop('Survived', axis=1, inplace=True)
        x_test = test_data.drop(features_drop, axis=1)

        # Conversion of categorical values of sex feature to numerical values
        mapping = {'male': 1, 'female': 0}
        x_train['Sex'] = x_train['Sex'].map(mapping)
        x_test['Sex'] = x_test['Sex'].map(mapping)

        x_train.Age.fillna(x_train.Age.median(), inplace=True)
        x_test.Age.fillna(x_test.Age.median(), inplace=True)

        # Filling the missing values in Embarked feature with the most repeated value
        x_train.fillna(value='S', inplace=True)

        # Filling the missing values of Fare feature with the median in test data
        x_test.Fare.fillna(x_test.Fare.median(), inplace=True)

        mapping = {'S': 0, 'C': 1, 'Q': 2}
        x_train['Embarked'] = x_train['Embarked'].map(mapping)
        x_test['Embarked'] = x_test['Embarked'].map(mapping)
        return x_train,y_train,x_test



    def create_pipeline(self):
        train_data,test_data = self.get_data()      
        x_train,y_train,x_test = self.preprocess_data(train_data,test_data)

        # K-Fold Cross Validation
        k_fold = KFold(n_splits=10, shuffle=True, random_state=0)

        # Logistic Regression
        logistic_regression = LogisticRegression()
        lr_score = cross_val_score(
            logistic_regression, x_train, y_train, cv=k_fold)
        print(lr_score)

        # kNN
        knn = KNeighborsClassifier(n_neighbors=20)
        knn_score = cross_val_score(knn, x_train, y_train, cv=k_fold)
        print(knn_score)

        # Random Forest
        RF = RandomForestClassifier(n_estimators=100)
        rf_score = cross_val_score(RF, x_train, y_train, cv=k_fold)
        print(rf_score)

        # Let's say after comparing the scores, we observe that Random Forest performed better than other models.
        # So we upload the model to artifacts, for deployment.

        # Predicting on test data
        RF.fit(x_train, y_train)
        y_predicted = RF.predict(x_test)

        self.run.log('RF CV score', rf_score)
        joblib.dump(RF, self.args.model_path)
        match = re.search('([^\/]*)$', self.args.model_path)
        # Upload Model to Run artifacts
        self.run.upload_file(name=self.args.artifact_loc + match.group(1),
                             path_or_stream=self.args.model_path)
        self.run.complete()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Titanic Survival Prediction')
    parser.add_argument('--model_path', type=str, help='Path to store the model')
    parser.add_argument('--artifact_loc', type=str, 
                        help='Artifact location to store the model', default='')
    args = parser.parse_args()
    titanic_survival_prediction = TitanicSurvivalPrediction(args)
    titanic_survival_prediction.create_pipeline()