import csv
import os
import re
import scipy
import string
# import np
# import pandas as pd

from flask import Flask, request

import json

import ca_core_model
from server_response import Intention


# ============================ MAIN ===========================================
if __name__ == "__main__":
    print('Staring ca_core_web')
    app = Flask(__name__)
    
    # '/training  GET   param: phrase'
    @app.route('/verify', methods = ['GET'])
    def verify():
        print ('Verified')
        return 'Verified'

    # '/training  GET   param: phrase'
    @app.route('/training', methods = ['POST'])
    def training():
        print('Start: Trainig')
        if request.form.get('source') == None:
            exp = 'Missing source'
            print (exp)
            return exp
        try: 
            return ca_core_model.training(request.form.get('source'))
        except Exception as e:
            print (e)
            return 'exception'
    
    # '/predict   POST   param: phrase'
    @app.route('/predict', methods = ['POST'])
    def predictIntension():
        print('Start: Predict')
        # print('asd' + request.form.asd)
        if request.form.get('sessionId') == None:
            exp = 'Missing sessionId'
            print (exp)
            return exp
        if  request.form.get('phrase') == None:
            exp = 'Missing phrase'
            print (exp)
            return exp
        if  request.form.get('messageId') == None:
            exp = 'Missing messageId'
            print (exp)
            return exp

        phrase = request.form.get('phrase')
        # algorithm = request.form.get('algorithm')
        # serverRes = ChatRecognition()

        try :
            return obj2json(ca_core_model.predict('sgd', phrase))
            # serverRes.intention = 
            # serverRes.status = 'completed'
            # serverRes.followup = 'origin and destination?'
        except Exception as e:
            print (e)
            return 'exception'
        

    def obj2json(obj):
        return json.dumps(obj, default=lambda o: o.__dict__)
        
    #app.run(debug=True)
    # app.run(host='maed-w7.corp.oocl.com', port=4567)
    app.run(host='0.0.0.0', port=8080)