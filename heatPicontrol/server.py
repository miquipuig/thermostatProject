# thermostatProject
# Copyright (C) 2020  Miquel Puig Gibert @miquipuig
 
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
 
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
 
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

from flask import Flask
from flask import json
from flask import jsonify
from flask import request
import threading
from .dataService import ts

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
