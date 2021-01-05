from flask import Blueprint, render_template, request, redirect, url_for, session, current_app, flash
import pyvjoy
import time

bp_joystick = Blueprint("bp_joystick", __name__)


@bp_joystick.route('/button', methods=["POST"])
def button():
    button = int(request.form.get("button"))
    device = int(request.form.get("device"))
    j = pyvjoy.VJoyDevice(1)

    # turn button number 15 on
    j.set_button(button, 1)
    time.sleep(5)
    j.set_button(button, 0)

    return

@bp_joystick.route('/axis', methods=["POST"])
def axis():
    axis = request.form.get("axis")
    axis_level_in_percent = float(request.form.get("percent"))
    device = int(request.form.get("device"))
    j = pyvjoy.VJoyDevice(1)

    if axis_level_in_percent > 100:
        axis_level_in_percent = 100.00

    axis_level = hex((100/32768)* axis_level_in_percent)

    if axis == x:
        j.set_axis(pyvjoy.HID_USAGE_X, axis_level)
    elif axis == y:
        j.set_axis(pyvjoy.HID_USAGE_Y, axis_level)
    elif axis == z:
        j.set_axis(pyvjoy.HID_USAGE_Z, axis_level)
    elif axis == rx:
        j.set_axis(pyvjoy.HID_USAGE_RX, axis_level)
    elif axis == ry:
        j.set_axis(pyvjoy.HID_USAGE_RY, axis_level)
    elif axis == rz:
        j.set_axis(pyvjoy.HID_USAGE_RZ, axis_level)

    return