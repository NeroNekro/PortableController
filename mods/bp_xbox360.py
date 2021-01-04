from flask import Blueprint, render_template, request, redirect, url_for, session, current_app, flash
import os
import configparser
import werkzeug

bp_xbox360 = Blueprint("bp_xbox360", __name__)

@bp_xbox360.route('/')
def index():


    return