from flask import Flask, render_template, request, redirect, session, flash
app = Flask(__name__)
app.secret_key = 'keep it secret, keep it safe'
app.config["UPLOAD_PATH"] = "static/img"