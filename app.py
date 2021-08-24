from flask import Flask, request, render_template
from forms import SignUpForm
from joblib import load
from FeatureTransformation.UserInputDataEncode import FeatureTransform
from FeatureTransformation.UserInputFeatureScalling import FeatureScaling
from Loggers.logger import ApplicationLogger
from DatabaseOperation.Database import CassandraDB
import os

app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

file_obj = "LogFiles/AdultIncomePrediction.log"
logging = ApplicationLogger(file_obj)

@app.route('/', methods=['POST', 'GET'])
def home():
    try:
        form = SignUpForm()

        if request.method == 'POST':
            logging.log('INFO', 'Requested Method : POST')

            if form.is_submitted():
                logging.log('INFO', 'Ready to take User Input.')
                encode = FeatureTransform(logging, file_obj)
                logging.log('INFO', 'User Input and some necessary variables with value are created!')
                result = encode.feature_Encoding()
                return render_template('index.html', form=form, value1="ExecutedS")
                if result:
                    logging.log('INFO',
                                'Exited from feature_Encoding function in FeatureTransform after successful encoding ')
                    logging.log('INFO', 'Range checking process is going to start now.')
                    flag, msg = encode.input_Limit()
                    return render_template('index.html', form=form, value1="ExecutedT")
                    if flag != False:
                        logging.log('INFO', 'Feature Scaling Process are going to start now.')
                        scale = FeatureScaling(result, logging, file_obj)
                        logging.log('INFO', 'Features assigned in different variables.')
                        result_lis = scale.Scaling()
                        logging.log('INFO', 'Successfully exited from Features Scaling Function')

                        logging.log('INFO', 'Model.pickle file Reading.....')
                        model = load("Models/finalized_model.pickle")
                        logging.log('INFO', 'Model successfully loaded!')
                        logging.log('INFO', 'Prediction Started.')
                        res = model.predict(result_lis)
                        logging.log('INFO', 'Prediction Successfully Completed!')

                        logging.log('INFO', "Transferring Predicted Result on Web Page.")
                        if res[0] == 1:
                            logging.log('INFO', 'Result shown on Web Page.')
                            return render_template('index.html', form=form,
                                                   value1="Predicted Salary of user is more than fifty (50) thousand")
                        else:
                            logging.log('INFO', 'Result shown on Web Page.')
                            return render_template('index.html', form=form,
                                                   value1="Predicted Salary of user is less than fifty (50) thousand")
                    else:
                        logging.log('INFO',
                                    'Due to out of the range user input scaling and user input process will not going to execute.')
                        return render_template('index.html', form=form, value1=msg)

                else:
                    return render_template('index.html', form=form, value1="Only Integer Value Accepted"+str(result))
        logging.log('INFO', 'Method is : Get')
        logging.log('INFO', 'Not any process executed.')
        logging.log('INFO', 'Showing None on Web page')
        return render_template('index.html', form=form, value1="")

    except Exception as e:
        logging.log(file_obj,"Some Exception Occurred in home Function!  Exception Message: " + str(e))
        logging.log(file_obj,"Process of Model Prediction Unsuccessful. Exited the home method of the app.py file")

@app.route("/DatabaseData", methods = ['GET','POST'])
def retriveFromDB():
    """
    :DESC: Th is is Hidden Api. It Retrieves Data from Database.
    :return: Render Databasedata.html Template
    """
    columna_Name = ("id", "Education", "Age", "WorkClass", "Final_Weight", "Occupation", "Capital_Loss", "Relationship", "Capital_Gain", "Martial_Status", "Sex", "Race", "Hours_Per_Week", "Country")
    db_obj = CassandraDB()
    return render_template('Databasedata.html', heading=columna_Name, data=db_obj.showData())



if __name__ == '__main__':
    app.run(port=8000,host='0.0.0.0')


