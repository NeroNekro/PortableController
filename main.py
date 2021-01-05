from flask import Flask
import configparser
import logging
import socket
import threading
import multiprocessing as mp
import PySimpleGUI as sg
import PySimpleGUIQt as sgqt
import datetime
import os
from mods.bp_start import bp_start
from mods.bp_keyboard import bp_keyboard
from mods.bp_joystick import bp_joystick
from mods.bp_xbox360 import bp_xbox360
import requests
import webbrowser
import sys
serverRunning = []
serverD = False

class GUI ():
    def __init__(self):
        self.log = LOG()
        try:
            configPath = f"config.ini"
            conf = configparser.ConfigParser()
            conf.read(configPath)
        except Exception as e:
            self.log.write_log("ERROR", "Config doesn't exist or is wrong: " + str(e))

        self.config = {}
        self.config["autoIP"] = conf["SERVER"]["autoIP"]
        self.config["IP"] = conf["SERVER"]["ip"]
        self.config["uiFolder"] = conf["SERVER"]["uiFolder"]
        self.config["modFolder"] = conf["SERVER"]["modFolder"]
        self.config["debug"] = conf["SERVER"]["debug"]
        self.config["PORT"] = conf["SERVER"]["port"]
        self.config["TRAY"] = conf["SERVER"]["tray"]

        if self.config["autoIP"] == "true":
            hostname = socket.gethostname()
            self.config["IP"] = socket.gethostbyname(hostname)

        self.log.write_log("INFO", "Read Config SUCCESSFUL")
        self.SERVER = SERVER(self.config)

    def thread(self):
        global serverRunning
        global serverD

        if serverD == False:
            try:
                t = threading.Thread(target=self.SERVER.start, args=(self,))
                t.daemon = True
                t.start()
                serverRunning = t
                serverD = True
                print(self.getTime() + " - Server started")
                self.log.write_log("INFO", "Server started")
            except Exception as e:
                print(self.getTime() + " - Error: Server won't start")
                self.log.write_log("ERROR", "Server won't start: " + str(e))
        else:
            try:
                url = 'http://' + self.config["IP"] + ':' + self.config["PORT"] + "/shutdown"
                requests.post(url)
                serverD = False
                print(self.getTime() + " - INFO: Server stopped")
            except Exception as e:
                print(self.getTime() + " - Error: Server won't stop")
                self.log.write_log("ERROR", "Server won't stop: " + str(e))


    def start(self):
        global serverRunning
        global serverD
        if self.config["TRAY"] == "false":
            sg.theme('DarkBlue1')
            layout = [[sg.Text('Portable Controller')],
                      [sg.Output(background_color='#F7F3EC', text_color='black', size=(35, 7))],
                      [sg.Button("Server Start", key='-BUTTON-'), sg.Open("Open Browser"), sg.Exit()],
                      [sg.Text('TJ 2020 V1.0 https://portable-controller.de', click_submits=True, key="-LINK-")]]

            window = sg.Window('Portable Controller', layout, no_titlebar=True, size=(300, 220), resizable=False,
                               keep_on_top=False, alpha_channel=.95, grab_anywhere=True)
            while True:  # Event Loop
                event, values = window.Read()
                if event in (None, 'Exit'):
                    break
                if event == '-BUTTON-':
                    if serverD == False:
                        try:
                            self.thread()

                        except Exception as e:
                            self.log.write_log("ERROR", "Server dont start: " + str(e))
                        try:
                            port = self.config["PORT"]
                            os.popen(
                                f"netsh advfirewall firewall add rule name=PortableController dir=in action=allow protocol=TCP localport={port}")
                        except:
                            print(" - Firewall can't be open")
                            self.log.write_log("ERROR", "Firewall can't be open: " + str(e))
                        window['-BUTTON-'].Update("Server Stop")

                        #print(server.getBrowserData())
                    else:
                        self.thread()
                        window['-BUTTON-'].Update("Server Start")


                elif event == 'Open Browser':
                    url = f'http://{self.config["IP"]}:{self.config["PORT"]}/'
                    webbrowser.open_new(url)
                elif event == '-LINK-':
                    webbrowser.open_new("https://portable-controller.de")

            window.Close()
        else:

            menu_def = ['File', ['Start/Stop', 'Open', 'Exit']]

            tray = sgqt.SystemTray(menu=menu_def, filename='192.png')

            while True:
                menu_item = tray.Read()
                if menu_item is not None:
                    if menu_item == 'Exit':
                        break
                    if menu_item == 'Start/Stop':
                        if serverD == False:
                            try:
                                self.thread()
                                tray.show_message('Starting', 'Starting Server')
                            except Exception as e:
                                self.log.write_log("ERROR", "Server dont start: " + str(e))
                                tray.show_message('Error', 'Starting server not successfull')
                            try:
                                port = self.config["PORT"]
                                os.popen(
                                    f"netsh advfirewall firewall add rule name=PortableController dir=in action=allow protocol=TCP localport={port}")
                            except:
                                print(" - Firewall can't be open")
                                self.log.write_log("ERROR", "Firewall can't be open: " + str(e))
                        else:
                            self.thread()
                            tray.show_message('Stopping', 'Stopping Server')
                    if menu_item == 'Open':
                        url = f'http://{self.config["IP"]}:{self.config["PORT"]}/'
                        webbrowser.open_new(url)


    def getTime(self):
        now = datetime.datetime.now()
        return now.strftime('%H:%M:%S')

class SERVER ():
    def __init__(self, config):
        #cli = sys.modules['flask.cli']
        #cli.show_server_banner = lambda *x: None
        self.app = Flask(__name__, static_folder="www")
        self.app.config["IP"] = config["IP"]
        self.app.config["PORT"] = config["PORT"]
        self.app.config["uiFolder"] = config["uiFolder"]
        self.app.config["modFolder"] = config["modFolder"]
        self.app.logger.disabled = True
        self.app.register_blueprint(bp_start)
        self.app.register_blueprint(bp_keyboard, url_prefix="/keyboard")
        self.app.register_blueprint(bp_joystick, url_prefix="/joystick")
        self.app.register_blueprint(bp_xbox360, url_prefix="/xbox360")

    def start(self, gui):
        try:
            self.app.run(host=self.app.config["IP"], port=self.app.config["PORT"], debug=False, threaded=True)
        except Exception as e:
            gui.log.write_log("ERROR", "Server dont start: " + str(e))



class LOG():
    def __init__(self):
        logging.basicConfig(format='%(asctime)s %(message)s',
                            filename='error.log',
                            level=logging.DEBUG,
                            filemode='w')

    def write_log(self, type, message):
        logging.info(type + " -- " + message)


if __name__ == '__main__':
    gui = GUI()
    gui.start()