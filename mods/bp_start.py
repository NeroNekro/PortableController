from flask import Blueprint, render_template, request, redirect, url_for, session, current_app, flash
import os
import configparser
import werkzeug

bp_start = Blueprint("bp_start", __name__)


@bp_start.route('/')
def index():
    folder = scanDir()
    ip = current_app.config["IP"]
    port = current_app.config["PORT"]

    data = []
    for dir in folder:
        data.append(readMeta(dir))

    return render_template("main.html", ip=ip, port=port, data=data)


@bp_start.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'



def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

def scanDir():
    dir = "www"

    listDir = []
    obj = os.scandir(dir)
    for entry in obj:
        if entry.is_dir():
             listDir.append(entry.name)


    return listDir

def readMeta(path):
    metaPath = f"www/{path}/meta.ini"
    config = configparser.ConfigParser()
    config.read(metaPath)
    meta = {
        "author": config['Info']['author'],
        "release": config['Info']['release'],
        "version": config['Info']['version'],
        "game": config['Info']['game'],
        "gameversion": config['Info']['gameversion'],
        "description": config['Info']['description'],
        "url": config['Info']['url'],
        "devices": config['Info']['devices'],
        "dir": path
    }
    return meta