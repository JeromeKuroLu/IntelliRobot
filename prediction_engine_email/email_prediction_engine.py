import json
from flask import Flask, request
import prediction
import prediction_enhance

# ============================ MAIN ===========================================
if __name__ == "__main__":
    print('Staring email prediction engine')
    app = Flask(__name__)  # , root_path="/test", root_path ready in 0.11 but conda only provide 0.10


    # '/training  GET   param: phrase'
    @app.route('/verify', methods=['GET'])
    def verify():
        print('Verified')
        return "positive"


    # '/predict   POST   param: phrase'
    @app.route('/pyt_dom_emr/predict', methods=['POST'])
    def predictIntension():
        print('Start: Predict')

        email = request.form.get('subject')
        print(email)

        try:
            return obj2json(prediction.predict_subject(email))
            # serverRes.intention = 
            # serverRes.status = 'completed'
            # serverRes.followup = 'origin and destination?'
        except Exception as e:
            print(e)
            return 'exception'


    @app.route('/pyt_dom_emr/predict/enhance', methods=['POST'])
    def predict_enhance():
        content_type = request.form.get('type')
        content = request.form.get('content')
        algorithm = request.form.get('algorithm')
        try:
            predict_label, property_result = prediction_enhance.predict_email(content, target=content_type,
                                                                              algorithm=algorithm)
            property_result['bkg_creation'] = property_result['bkg creation']
            property_result['bkg_amendment'] = property_result['bkg amendment']
            property_result.pop('bkg creation')
            property_result.pop('bkg amendment')
            response = {
                'predict_label': predict_label,
                'property_result': property_result
            }
            return obj2json(response)
            # serverRes.intention =
            # serverRes.status = 'completed'
            # serverRes.followup = 'origin and destination?'
        except Exception as e:
            print(e)
            return 'exception'


    def obj2json(obj):
        return json.dumps(obj, default=lambda o: o.__dict__)


    app.run(host='0.0.0.0', port=8082, debug=True)
