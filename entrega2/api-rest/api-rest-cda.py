from flask import Flask,request, jsonify
from flask_restful import reqparse, abort, Api, Resource
import pickle
import pandas as pd
from logger import LOGGER
app = Flask(__name__)
api = Api(app)


required_fields = ['cant_prods_orden', 'prom_score_vendedor','prom_score_producto', 'tiempo_entrega_dias','entrega_a_transportador_atrasada', 'entrega_a_cliente_atrasada','mejor_producto_respecto_a_categ']

from warnings import filterwarnings
filterwarnings("ignore")
@app.route("/")
def home():
    return "CDA - Rest API-Grupo 9!"

class PredictValue(Resource):

    def __init__(self):
        self.params = request.get_json()
        LOGGER.debug(self.params)

    def post(self):

        df = pd.DataFrame(self.params)

        missing_fields = self.__compare_fields(list(df.columns))
        q_missing_fields = len(missing_fields)
        if q_missing_fields != 0:
            missing_fields = ",".join(missing_fields)
            LOGGER.error(f"Fields {missing_fields} are required")
            return f"Field {missing_fields} are required",400
        else:
            predictions = model.predict(df)
            return(str(predictions))

    def __compare_fields(self,columns):

        LOGGER.info("--- FUNCTION COMPARE FIELDS ---")
        LOGGER.info(f" Required Fields : {required_fields}")
        LOGGER.info(f" Received Columns : {columns}")
        check_field_required = set(required_fields) - set(columns)
        LOGGER.info(f" Difference Columns : {check_field_required}")
        return check_field_required

api.add_resource(PredictValue, '/predict')

if __name__ == '__main__':

    model = pickle.load( open( "modelo_entrega2.pkl", "rb" ) )
    app.run(debug=True,port=5050,host="0.0.0.0")


### Ejemplo POSTMAN
# [
# {"cant_prods_orden": 2.00,  "prom_score_vendedor": 4.28,  "prom_score_producto": 4.50,  "tiempo_entrega_dias": 4.00,  "entrega_a_transportador_atrasada": 0, "entrega_a_cliente_atrasada": 0, "mejor_producto_respecto_a_categ": 1.00 },
# {"cant_prods_orden": 1.00,  "prom_score_vendedor": 4.28,  "prom_score_producto": 4.50,  "tiempo_entrega_dias": 13.00, "entrega_a_transportador_atrasada": 0, "entrega_a_cliente_atrasada": 0, "mejor_producto_respecto_a_categ": 1.00 },
# {"cant_prods_orden": 1.00,  "prom_score_vendedor": 4.28,  "prom_score_producto": 4.25,  "tiempo_entrega_dias": 5.00,  "entrega_a_transportador_atrasada": 0, "entrega_a_cliente_atrasada": 0, "mejor_producto_respecto_a_categ": 1.00 }
# ]


### Ejemplo POSTMAN ERROR
# [
# {"prom_score_vendedor": 4.28,  "prom_score_producto": 4.50,  "tiempo_entrega_dias": 4.00,  "entrega_a_transportador_atrasada": 0, "entrega_a_cliente_atrasada": 0, "mejor_producto_respecto_a_categ": 1.00 },
# {"prom_score_vendedor": 4.28,  "prom_score_producto": 4.50,  "tiempo_entrega_dias": 13.00, "entrega_a_transportador_atrasada": 0, "entrega_a_cliente_atrasada": 0, "mejor_producto_respecto_a_categ": 1.00 },
# {"prom_score_vendedor": 4.28,  "prom_score_producto": 4.25,  "tiempo_entrega_dias": 5.00,  "entrega_a_transportador_atrasada": 0, "entrega_a_cliente_atrasada": 0, "mejor_producto_respecto_a_categ": 1.00 }
# ]