import cherrypy
import os
import json
from serial_control import SerialControl


baudrate = 115200  # this should match the baudrate set in the arduino firmware
controller = SerialControl(baudrate)


class RootServer(object):
    @cherrypy.expose
    def index(self, **params):
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'  # CORS
        return 'Welcome!'

    @cherrypy.expose
    def stop_server(self, **params):
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'  # CORS
        controller.kill()
        cherrypy.engine.exit()

    @cherrypy.expose
    def set_led_intensity(self, **params):
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'  # CORS
        return 'yay'

    @cherrypy.expose
    def get_led_intensity(self, **params):
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'  # CORS
        return 'yay'

    @cherrypy.expose
    def toggle(self, **params):
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'  # CORS
        print('toggling...')
        # get state
        controller.flushin()
        controller.send('get blue_light_int')
        if controller.wait_for_response():
            response = controller.readlines()
            light_int = 0
            if len(response) > 0:
                light_int = float(response[0])
            # set state
            if light_int > 50:
                controller.send('set blue_light_int 0')
            else:
                controller.send('set blue_light_int 100')
        return 'toggled'


if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        }
    }
    cherrypy.config.update({
        'server.socket_host': 'localhost',
        'global': {
            # 'environment': 'test_suite'
            'engine.autoreload.on': False
        }
    })
    cherrypy.quickstart(RootServer(), '/', conf)