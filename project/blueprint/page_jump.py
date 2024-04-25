import csv
import os
from flask import Blueprint, render_template, redirect, request, jsonify, url_for, session, current_app, flash, render_template_string
from flask_mail import Message

from itsdangerous import json

import random
import string


page_jump = Blueprint('page_jump', __name__, url_prefix='/jump')
@page_jump.route('/')
def home():
    return render_template('home2.html')

@page_jump.route('/analyse')
def analyse():
    return render_template('analyse.html')

@page_jump.route('/history')
def history():
    return redirect(url_for('historyloggor.show_table'))

@page_jump.route('/view')
def view():
    return render_template('view.html')

@page_jump.route('/load_forecasting')
def load_forecasting():
    return render_template('load_forecasting.html')
