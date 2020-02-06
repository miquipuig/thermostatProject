from flask import Flask
from flask import json
from flask import jsonify
from flask import request
import threading
from thermostatService import ts



class ThermostatServer(object):

    app = Flask(__name__)
    
    @app.route('/')
    def hello():
        return "ThermostatProject"

    # @app.route('/<name>')
    # def hello_name(name):
    #     return "This service don't exist: {}!".format(name)
    @app.route('/tasks', methods=['GET'])
    def get_tasks():
        return jsonify({'tasks': tasks})

    @app.route('/get_data')
    def get_data():
        return jsonify({'tasks': ts.getData()})

    @app.route('/set_data', methods=['POST'])
    def set_data(): 
        ts.desiredT = int(request.args.get('temp'))
        ts.power = request.args.get('power')=='True'
        print(ts.power)
        return 'ok'

    def initServer(self):
        self.app.run(host= '0.0.0.0')
    
    def __init__(self):
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        self.initServer()


if __name__ == '__main__':
    ts =ThermostatServer()
    while True:
         print('Server running...')
         time.sleep(1)
