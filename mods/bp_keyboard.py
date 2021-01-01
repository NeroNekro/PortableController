from flask import Blueprint, render_template, request, redirect, url_for, session, current_app, flash, jsonify
import keyboard
import time
import threading


bp_keyboard = Blueprint("bp_keyboard", __name__)


@bp_keyboard.route('/single', methods=["POST"])
def single():
    key = request.form.get("key")
    try:
        th = threading.Thread(target=single_button, args=(key,))
        th.start()
    except:
        print ("Error: unable to start thread")

@bp_keyboard.route('/multiple', methods=["POST"])
def multiple():
    key = request.form.get("key")
    keys = key.split("%")
    for key in keys:
        try:
            th = threading.Thread(target=single_button, args=(key,))
            th.start()
        except:
            print("Error: unable to start thread")
        time.sleep(1)



@bp_keyboard.route('/custom', methods=["POST"])
def custom():
    data = request.get_json()
    data = jsonify(data)
    for key in data:
        for i in range(0, key["counter"], 1):
            try:
                th = threading.Thread(target=single_button, args=(key["key"],))
                th.start()
            except:
                print("Error: unable to start thread")
            time.sleep(key["timer"])


def single_button(key):
    keyboard.press_and_release(key)
    return

def text(chatOpen, chatText, chatSend):
    keyboard.press_and_release(chatOpen)
    text = map(lambda x: x, chatText)

    for char in text:
        if char == " " or char == "":
            keyboard.press_and_release("space")
        else:
            keyboard.press_and_release(char)
        print(char)
    keyboard.press_and_release(chatSend)
    return "success"