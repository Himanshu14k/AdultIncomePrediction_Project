from joblib import load
from pandas import DataFrame
import pickle 

class FeatureScaling:
    def __init__(self, user_input, logger_obj, file_obj):
        try:
            self.logger_obj = logger_obj
            self.file_obj = file_obj
            self.logger_obj.log("INFO", 'Different user input value assign process started')
            self.user_input = user_input
            self.Education = self.user_input['Education']
            self.logger_obj.log("INFO", 'stated done')
            self.Workclass =  self.user_input['Workclass']
            self.Age = self.user_input['Age']
            self.Martial_Status = self.user_input['Martial_Status']
            self.Occupation = self.user_input['Occupation']
            self.Relationship = self.user_input['Relationship']
            self.Race = self.user_input['Race']

            self.Sex = self.user_input['Sex']
            self.Final_Weight = self.user_input['Final_Weight']
            self.Capital_Gain = self.user_input['Capital_Gain']
            self.Capital_Loss = self.user_input['Capital_Loss']
            self.Hours_Per_Week = self.user_input['Hours_Per_Week']
            self.Country = self.user_input['Country']
            self.X = [[self.Sex, self.Age, self.Final_Weight,
                      self.Education, self.Capital_Gain, self.Capital_Loss,
                      self.Hours_Per_Week, self.Workclass, self.Martial_Status, self.Occupation,
                      self.Relationship, self.Race, self.Country]]
            self.logger_obj.log("INFO", 'Different user input value assign process Finished')
        except Exception as e:
            self.logger_obj.log('INFO',"Exception Occurred during variable creation of user input to store scale data in dictionary format!  Exception Message: " + str(e))
            self.logger_obj.log('INFO',"Process to create variable and store user input in that variable failed.")

    def Scaling(self):
        try:
            self.logger_obj.log("INFO", 'Feature Scaling process started')
            self.X = DataFrame(self.X)
            sc = pickle.load(open("FeatureTransformation/scale.pickle", "rb"))
            self.X.iloc[:, 1:] = sc.transform(self.X.iloc[:, 1:])
            self.logger_obj.log("INFO", 'Feature scaling process successfully executed!')
            return self.X
        except Exception as e:
            self.logger_obj.log('INFO',"Exception Occurred during Process of Feature Scaling!  Exception Message: " + str(e))
            self.logger_obj.log('INFO',"Process of Feature scaling Failed. Exited from Scaling function of FeatureScalling class")