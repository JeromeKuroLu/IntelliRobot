import json

from flask import Flask, request

from recognizer import recognize_context
from util import reshape_util

# ============================ MAIN ===========================================
if __name__ == "__main__":
    print('Staring recognition engine')
    app = Flask(__name__) #, root_path="/test", root_path ready in 0.11 but conda only provide 0.10
    
    # '/training  GET   param: phrase'
    @app.route('/verify', methods=['GET'])
    def verify():
        print('Verified')
        return "positive"


    @app.route('/extract', methods=['POST'])
    def extract():
        if request.form.get('message') is None:
            exp = 'Missing message'
            print(exp)
            return exp

        target_categories = [] # should get from request
        response = recognize_context(target_categories, request.form.get('message'))
        return obj2json(response)


    @app.route('/reshape', methods=['POST'])
    def replace():
        if request.form.get('message') is None:
            exp = 'Missing message'
            print(exp)
            return exp

        content, recognitions = reshape_util.reshape_content(request.form.get('message'))
        content = content.replace('\n', ' ')
        response = {
            'content': content,
            'recognitions': recognitions
        }
        return obj2json(response)

    def obj2json(obj):
        return json.dumps(obj, default=lambda o: o.__dict__)

    app.run(host='0.0.0.0', port=8083, debug=True)