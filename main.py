import cherrypy
import os
import json
from serial_control import SerialControl
import cv2
import base64


baudrate = 115200  # this should match the baudrate set in the arduino firmware
controller = SerialControl(baudrate)

camera_01 = cv2.VideoCapture(1)


def get_image(camera):
    ret, frame = camera.read()
    return frame


def get_image_uri(img):
    img_str = cv2.imencode('.png', img)[1]
    data64 = base64.b64encode(img_str)
    data_uri = data64.decode('utf-8').replace("\n", "")
    return data_uri


class RootServer(object):
    @cherrypy.expose
    def index(self, **params):
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'  # CORS
        return 'Welcome!'

    @cherrypy.expose
    def stop_server(self, **params):
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'  # CORS
        controller.kill()
        camera_01.release()
        cherrypy.engine.exit()

    @cherrypy.expose
    def get_image(self, **params):
        cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'  # CORS
        img = get_image(camera_01)
        uri = get_image_uri(img)
        html = '<img src="data:image/png;base64,' + uri + '" />'
        return html

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