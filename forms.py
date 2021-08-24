from flask_wtf import FlaskForm
from wtforms import SubmitField,SelectField,validators,IntegerField


class SignUpForm(FlaskForm):
    workclass_val = [' State-gov', ' Self-emp-not-inc', ' Private', ' Federal-gov', ' Local-gov', ' Self-emp-inc', ' Without-pay']
    education_val = [' Bachelors', ' HS-grad', ' 11th', ' Masters', ' 9th', ' Some-college', ' Assoc-acdm', ' 7th-8th', ' Doctorate', ' Assoc-voc', ' Prof-school', ' 5th-6th', ' 10th', ' Preschool', ' 12th', ' 1st-4th']
    martial_status_val = [' Never-married', ' Married-civ-spouse', ' Divorced', ' Married-spouse-absent', ' Separated', ' Married-AF-spouse', ' Widowed']
    occupation_val = [' Adm-clerical', ' Exec-managerial', ' Handlers-cleaners', ' Prof-specialty', ' Other-service', ' Sales', ' Transport-moving', ' Farming-fishing', ' Machine-op-inspct', ' Tech-support', ' Craft-repair', ' Protective-serv', ' Armed-Forces', ' Priv-house-serv']
    relationship_val = [' Not-in-family', ' Husband', ' Wife', ' Own-child', ' Unmarried', ' Other-relative']
    race_val = [' White', ' Black', ' Asian-Pac-Islander', ' Amer-Indian-Eskimo', ' Other']
    sex_val = [' Male', ' Female']
    country_val = [' United-States', ' Cuba', ' Jamaica', ' India', ' Mexico', ' Puerto-Rico', ' Honduras', ' England', ' Canada', ' Germany', ' Iran', ' Philippines', ' Poland', ' Columbia', ' Cambodia', ' Thailand', ' Ecuador', ' Laos', ' Taiwan', ' Haiti', ' Portugal', ' Dominican-Republic', ' El-Salvador', ' France', ' Guatemala', ' Italy', ' China', ' South', ' Japan', ' Yugoslavia', ' Peru', ' Outlying-US(Guam-USVI-etc)', ' Scotland', ' Trinadad&Tobago', ' Greece', ' Nicaragua', ' Vietnam', ' Hong', ' Ireland', ' Hungary', ' Holand-Netherlands']

    Workclass = SelectField('WorkClass', choices=workclass_val)
    Education = SelectField('Education', choices=education_val)
    Martial_Status = SelectField('Martial-Status', choices=martial_status_val)
    Occupation = SelectField('Occupation', choices=occupation_val)
    Relationship = SelectField('Relationship', choices=relationship_val)
    Race = SelectField('Race', choices=race_val)
    Sex = SelectField('Sex', choices=sex_val)
    Country = SelectField('Country', choices=country_val)
    Age = IntegerField("Age", validators=[validators.DataRequired()])
    Final_Weight = IntegerField("Final-weight", validators=[validators.DataRequired()])
    Capital_Gain = IntegerField("Capital-Gain", validators=[validators.DataRequired()])
    Capital_Loss = IntegerField("Capital-Loss", validators=[validators.DataRequired()])
    Hours_Per_Week = IntegerField("Hours-Per-Week", validators=[validators.DataRequired()])

    submit = SubmitField(' Check Income! ')


