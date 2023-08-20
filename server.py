from flask import Flask, render_template, request, flash, session, redirect

from model import connect_to_db, db


from jinja2 import StrictUndefined

app = Flask(__name__)