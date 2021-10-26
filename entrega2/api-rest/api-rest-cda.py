from flask import Flask,request, jsonify
from flask_restful import reqparse, abort, Api, Resource
import pickle
import pandas as pd
app = Flask(__name__)
api = Api(app)


required_fields = ["avgAnnCount","avgDeathsPerYear","incidenceRate","medIncome"]

@app.route("/")
def home():
    return "CDA - Rest API-Grupo 9!"

class PredictValue(Resource):
    # @app.route('/predict', methods=['POST'])

    def __init__(self):
        self.params = request.get_json()

    def post(self):
        # print("POST")

        # print(self.params)

        df = pd.DataFrame(self.params)

        missing_fields = self.__compare_fields(list(df.columns))
        q_missing_fields = len(missing_fields)
        if q_missing_fields != 0:
            missing_fields = ",".join(missing_fields)
            return f"Fields {missing_fields} are required",400
        else:
            predictions = model.predict(df)
            predictions = [pred[0] for pred in predictions]
            return list(predictions)

    def __compare_fields(self,columns):

        print("--- FUNCTION COMPARE FIELDS ---")
        print(f" Required Fields : {required_fields}")
        print(f" Received Columns : {columns}")
        check_field_required = set(required_fields) - set(columns)
        print(f" Difference Columns : {check_field_required}")
        return check_field_required

api.add_resource(PredictValue, '/predict')

if __name__ == '__main__':

    model = pickle.load( open( "regression_model.pkl", "rb" ) )
    app.run(debug=True,port=5050)


### Ejemplo POSTMAN
# [
#     {"avgAnnCount": 124,    "avgDeathsPerYear": 45,     "incidenceRate": 473, "medIncome": 57491},
#     {"avgAnnCount": 77,     "avgDeathsPerYear": 34,     "incidenceRate": 430, "medIncome": 37853},
#     {"avgAnnCount": 8954,   "avgDeathsPerYear": 3397,   "incidenceRate": 438, "medIncome": 51485},
#     {"avgAnnCount": 13,     "avgDeathsPerYear": 4,      "incidenceRate": 351, "medIncome": 42907}
# ]


### Ejemplo POSTMAN ERROR
# [
#     {"avgAnnCount": 124,    "avgDeathsPerYear": 45,     "incidenceRate": 473},
#     {"avgAnnCount": 77,     "avgDeathsPerYear": 34,     "incidenceRate": 430},
#     {"avgAnnCount": 8954,   "avgDeathsPerYear": 3397,   "incidenceRate": 438},
#     {"avgAnnCount": 13,     "avgDeathsPerYear": 4,      "incidenceRate": 351}
# ]
