from flask import Flask
from flask import request, jsonify, json
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
# import airflow
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='postgresql://DSPDB:PAUcwKtYQ2j0Tt0f16pe@dspdb.c7yyz4ccfsai.eu-west-2.rds.amazonaws.com/DSP_Tweeter'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Tweet(db.Model):
  __tablename__='Tweets'
  id=db.Column(db.Integer,primary_key=True)
  Email=db.Column(db.String(255))
  Emergency_Email=db.Column(db.String(80))
  Msg=db.Column(db.String(255))
  Prediction=db.Column(db.String(15))

  def __init__(self,YourEmail,EmeEmail,Msg,Prediction):
    self.Email=YourEmail
    self.Emergency_Email=EmeEmail
    self.Msg=Msg
    self.Prediction = Prediction


def make_predictions():
    # We add here our model code
    return 'Danger'


@app.route("/Submit", methods=['GET'])
def submit():
    data = json.loads(request.data)
    YourEmail= data['YourEmail']
    EmeEmail=data['EmeEmail']
    Msg=data['Msg']
    Prediction = make_predictions() # Pass my data to the model
    tweet = Tweet(YourEmail, EmeEmail, Msg, Prediction)
    db.session.add(tweet)
    db.session.commit()
    print(data)
    return {
    "YourEmail": YourEmail,
    "EmeEmail": EmeEmail,
    "Msg": Msg,
    "Prediction": Prediction
    }


@app.route('/SubmitFile', methods=["GET"])
def index():
    if request.method == 'GET':
        saved_file = request.files['data_file']
        df = pd.read_csv(saved_file)
        for index, row in df.iterrows():
            print(row)
            print(type(row))
            break
    return "Hello"


if __name__ == '__main__':
    app.run(debug=True)