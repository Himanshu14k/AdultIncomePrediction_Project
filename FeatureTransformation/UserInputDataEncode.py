from forms import SignUpForm
from flask import request
from DatabaseOperation.Database import CassandraDB

class FeatureTransform:
    def __init__(self, logger_obj, logger_obj_db):
        self.logger_obj = logger_obj
        self.logger_obj_db = logger_obj_db
        try:
            self.form = SignUpForm()
            self.input_data = request.form.to_dict()
        except Exception as e:
            self.logger_obj.log('INFO', "Exception Occurred during form object creation and during user input storing in dictionary format!  Exception Message: " + str(e))
            self.logger_obj.log('INFO', "Process to create form variable and store user input in dictionary format Unsuccessful. Exited the input_Limit method of the FeatureTransform class")

        self.val_encode = {
            'Workclass': {' Private': 22264, ' Self-emp-not-inc': 2498, ' Local-gov': 2067, ' State-gov': 1279,
                          ' Self-emp-inc': 1074, ' Federal-gov': 943, ' Without-pay': 14},
            'Martial_Status': {' Married-civ-spouse': 14059, ' Never-married': 9711, ' Divorced': 4212,
                               ' Separated': 939, ' Widowed': 827, ' Married-spouse-absent': 370,
                               ' Married-AF-spouse': 21},
            'Education': {' Bachelors': 13, ' HS-grad': 9, ' 11th': 7, ' Masters': 14, ' 9th': 5,
                          ' Some-college': 10, ' Assoc-acdm': 12, ' 7th-8th': 4, ' Doctorate': 16,
                          ' Assoc-voc': 11, ' Prof-school': 15, ' 5th-6th': 3, ' 10th': 6, ' Preschool': 1,
                          ' 12th': 8, ' 1st-4th': 2},
            'Occupation': {' Prof-specialty': 4034, ' Craft-repair': 4025, ' Exec-managerial': 3991,
                           ' Adm-clerical': 3719, ' Sales': 3584, ' Other-service': 3209, ' Machine-op-inspct': 1964,
                           ' Transport-moving': 1572, ' Handlers-cleaners': 1349, ' Farming-fishing': 987,
                           ' Tech-support': 911, ' Protective-serv': 644, ' Priv-house-serv': 141, ' Armed-Forces': 9},
            'Relationship': {' Husband': 12457, ' Not-in-family': 7714, ' Own-child': 4462, ' Unmarried': 3211,
                             ' Wife': 1406, ' Other-relative': 889},
            'Race': {' White': 25912, ' Black': 2816, ' Asian-Pac-Islander': 894, ' Amer-Indian-Eskimo': 286,
                     ' Other': 231},
            'Country': {'north_America': 27608, 'central_America': 1220, 'east_Asia': 492, 'west_Europe': 408,
                        'central_Asia': 142, 'south_America': 113, 'east_Europe': 85, 'south_Asia': 71},
            'Sex': {' Male': 0, ' Female': 1}
        }
        self.Continents_encode = {
            'east_Asia': [" Cambodia", " Philippines", " China", " Hong", " Laos", " Thailand", " Japan", " Taiwan",
                          " Vietnam"],
            'central_America': [" Cuba", " Guatemala", " Jamaica", " Nicaragua", " Puerto-Rico", " Dominican-Republic",
                                " El-Salvador", " Haiti", " Honduras", " Mexico", " Trinadad&Tobago"],
            'west_Europe': [" England", " Germany", " Holand-Netherlands", " Ireland", " France", " Greece", " Italy",
                            " Portugal", " Scotland"],
            'central_Asia': [" India", " Iran"],
            'south_America': [" Ecuador", " Peru", " Columbia"],
            'north_America': [' United-States', ' Canada', ' Outlying-US(Guam-USVI-etc)'],
            'east_Europe': [" Poland", " Yugoslavia", " Hungary"],
            'south_Asia': [' South']
        }
        self.num_feature = ['Age', 'Final_Weight', 'Capital_Gain', 'Capital_Loss', 'Hours_Per_Week']
        self.dropDown_feature = ['Workclass', 'Education', "Martial_Status", 'Occupation', 'Relationship', 'Race', 'Sex', 'Country']

    def DB_Operation(self):
        self.logger_obj.log('INFO', 'Database Operation has been started')
        self.logger_obj.log('INFO', 'Creating Cassandra database object.')
        db_Object = CassandraDB(self.logger_obj_db)
        self.logger_obj.log('INFO', 'Cassandra database object created Successfully!')
        try:
            db_Object.useDB()
            self.logger_obj.log('INFO', 'Inserting user input value in database.')
            db_Object.insertData(self.input_data)
        except:
            self.logger_obj.log('INFO', 'Inserting user input value in database.')
            db_Object.insertData(self.input_data)
        finally:
            self.logger_obj.log('INFO', 'User input Inserted in Database Successfully!')


    def feature_Encoding(self):
        try:
            self.logger_obj.log('INFO', 'Feature Encoding Started.')
            for data in self.input_data:
                if data in self.num_feature:
                    try:
                        self.input_data[data] = int(self.input_data[data])
                    except ValueError:
                        return False
                elif (data in self.dropDown_feature) and (data == 'Country'):
                    val = self.input_data[data]
                    for continent, country in self.Continents_encode.items():
                        if val in country:
                            self.input_data[data] = int(self.val_encode[data][continent])
                            break
                elif (data in self.dropDown_feature) and (data != 'submit'):
                    try:
                        val = self.input_data[data]
                        self.input_data[data] = int(self.val_encode[data][val])
                    except Exception as e:
                        continue
                else:
                    continue
            self.input_data.pop('submit')
            self.logger_obj.log('INFO', 'Feature Encoding Completed')
            self.DB_Operation()
            return self.input_data
        except Exception as e:
            self.logger_obj.log('INFO', "Here Some Exception Occurred!  Exception Message: " + str(e))
            self.logger_obj.log('INFO', "Process to encode categorical user input Unsuccessful. Exited the feature_Encoding of the FeatureTransform class")

    def input_Limit(self):
        try:
            self.logger_obj.log('INFO', 'Checking the range of Numerical Input field Started!')
            flag = True
            msg = "!!!  RANGE ERROR  !!!  "
            if (self.input_data['Age'] <= 95) and (self.input_data['Age'] >= 15):
                pass
            else:
                flag = False
                temp = "Age must be in range between 15 to 95. "
                msg = "".join((msg, temp))

            if (self.input_data['Final_Weight'] <= 650000) and (self.input_data['Final_Weight'] >= 13000):
                pass
            else:
                flag = False
                temp = "Final_Weight must be in range between 13000 to 650000. "
                msg = "".join((msg, temp))

            if (self.input_data['Capital_Gain'] <= 100000) and (self.input_data['Capital_Gain'] >= 0):
                pass
            else:
                flag = False
                temp = "Capital_Gain must be in range between 0 to 100000. "
                msg = "".join((msg, temp))


            if (self.input_data['Capital_Loss'] <= 4500) and (self.input_data['Capital_Loss'] >= 0):
                pass
            else:
                flag = False
                temp = "Capital_Loss must be in range between 0 to 4500. "
                msg = "".join((msg, temp))

            if (self.input_data['Hours_Per_Week'] <= 100) and (self.input_data['Hours_Per_Week'] >= 1):
                pass
            else:
                flag = False
                temp = "Hours_Per_Week must be in range between 1 to 100. "
                msg = "".join((msg, temp))

            self.logger_obj.log('INFO', 'Done range Checking of Numerical user input')
            return flag, msg
        except Exception as e:
            self.logger_obj.log('INFO' "Here Some Exception Occurred!  Exception Message: "+str(e))
            self.logger_obj.log('INFO', "Process to check the range of User Input value Unsuccessful. Exited the input_Limit method of the FeatureTransform class")

    '''def Encode(self):

        self.logger_obj.log('INFO', 'Process to Store and to Encode user data is going to start Now.')
        self.logger_obj.log('INFO', 'Threading called!')
        self.logger_obj.log('INFO', 'Creating Copy of user input.')
        arg1 = self.input_data
        arg2 = self.input_data
        self.logger_obj.log('INFO', 'Copy Created!')

        self.logger_obj.log('INFO', 'Threading Object Creating.')
        thread1 = Threading(target=self.feature_Encoding(), args=(arg1,))
        thread2 = Threading(target=self.DB_Operation(), args=(arg2,))
        self.logger_obj.log('INFO', 'Threading Object Created!.')

        self.logger_obj.log('INFO', 'Starting the feature_Encoding Thread.')
        thread1.start()
        self.logger_obj.log('INFO', 'Starting the DB_Operation Thread.')
        thread2.start()

        self.logger_obj.log('INFO', 'Joining the feature_Encoding Thread.')
        thread1.join()
        thread2.sl
        self.logger_obj.log('INFO', 'Joining the feature_Encoding Thread.')
        thread2.join()
        return thread1.result'''

    '''def Encode(self):
        self.DB_Operation()
        self.feature_Encoding()
        return self.input_data'''