from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from Loggers.logger import ApplicationLogger

class CassandraDB:

    def __init__(self, logger_obj):
        self.logger_obj = logger_obj
        try:
            self.logger_obj.log('INFO', 'Authentication of Database Started.')
            self.CLIENT_ID = 'kaYZmIsBJbtuZJNqEkoxBhoe'
            self.CLIENT_SECRET = "N3CPCB0fB5m,ZZPWGJf3i_DNa1ScsOuFccdwwCk5fgOK0UtlHY,UNs2FhS,W6dEMIp_TB-NBSJAJli.kg7OWR.L65aW4gPZvvcwR4Q_eOUeLP2ZtRQInDUaC1qeuP95O"


            cloud_config = {
                'secure_connect_bundle': '/home/maverick14k/Files/Ineuron/Projects/Internship/AdultIncomePrediction_Project/secure-connect-ineuron.zip'
            }
            auth_provider = PlainTextAuthProvider(self.CLIENT_ID, self.CLIENT_SECRET)
            self.logger_obj.log('INFO', 'Database Authenticated Successfully.')

            self.logger_obj.log('INFO', 'Creating Cluster.')
            cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
            self.session = cluster.connect()
            self.logger_obj.log('INFO', 'Cluster Created Successfully!')

        except Exception as e:
            self.logger_obj.log('INFO', 'Exception Occurred during Database Authentication. Exception is : '+str(e))



    def useDB(self):
        try:
            self.logger_obj.log('INFO', 'Using AdultCensusPrediction')
            self.session.execute("use adultcensusprediction")
            self.session.execute("select release_version from system.local")
            self.logger_obj.log('INFO', 'Creating Table "InputData" in AdultCensusPrediction Database.')
            self.session.execute("CREATE TABLE userdata(id uuid PRIMARY KEY,Education text,Age int,WorkClass text,Final_Weight int,Occupation text,Capital_Loss int,Relationship text,Capital_Gain int,Martial_Status text,Sex text,Race text,Hours_Per_Week int,Country text);")
            self.logger_obj.log('INFO', 'Table Created Successfully!')
        except Exception as e:
            self.logger_obj.log('INFO', 'Some Exception Occurred during table creation in database. Exception is : '+str(e))




    def insertData(self, data):
        try:
            self.logger_obj.log('INFO', 'Insertion Process Started.')
            key = "id ,Education ,Age ,WorkClass ,Final_Weight ,Occupation ,Capital_Loss ,Relationship ,Capital_Gain ,Martial_Status ,Sex ,Race ,Hours_Per_Week ,Country"
            value = "{0}, '{1}', {2}, '{3}', {4}, '{5}', {6}, '{7}', {8}, '{9}', '{10}', '{11}', {12}, '{13}'".format('uuid()', data['Education'], data['Age'], data['Workclass'], data['Final_Weight'], data['Occupation'], data['Capital_Loss'], data['Relationship'], data['Capital_Gain'], data['Martial_Status'], data['Sex'], data['Race'], data['Hours_Per_Week'], data['Country'])
            self.session.execute("use adultcensusprediction")
            print("hello")
            userInput = "INSERT INTO userdata({}) VALUES({});".format(key, value)
            insertedData = self.session.execute(userInput)
            self.logger_obj.log('INFO', 'User Data inserted in Database Successfully!')
            self.logger_obj.log('INFO', 'Inserted Data in Database are : {}'.format(insertedData))
        except Exception as e:
            self.logger_obj.log('INFO', 'Some Exception Occurred during Data Insertion in database. Exception is : '+str(e))




    def showData(self):
        try:
            self.logger_obj.log('INFO', 'Process to show data from Database Started.')
            self.session.execute("use AdultCensusPrediction")
            data = self.session.execute("SELECT * FROM userdata;")
            allData = []

            for row in data:
                allData.append(tuple(row))
            self.logger_obj.log('INFO', 'Data Successfully stored in tuples. ')
            self.logger_obj.log('INFO', 'Retrived Data are : {} '.format(allData))
            return tuple(allData)
        except Exception as e:
            self.logger_obj.log('INFO', 'Some Exception Occurred during showing Data from database. Exception is : '+str(e))
