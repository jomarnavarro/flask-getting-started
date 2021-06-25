from flask import Flask, render_template, abort,jsonify, request, redirect, url_for
from datetime import datetime

from model import db, save_db

app = Flask(__name__)

times_viewed = 0;

@app.route('/')
def welcome():
    return render_template('welcome.html',
        message='Some Message', cards=db
    )

@app.route('/card/<int:index>')
def card_view(index):
    if index >= len(db):
        return render_template('error.html', error=f"Card {index} does not exist.")
    return render_template('card.html', card=db[index], index=index, max_index = len(db) - 1)

@app.route('/card/new', methods=["GET", "POST"])
def add_card():
    if request.method == "POST":
        q = request.form['question']
        a = request.form['answer']
        db.append({'question': q, 'answer': a})
        save_db()
        return redirect(url_for('card_view', index=len(db) - 1))
    return render_template('add_card.html')


@app.route('/api/card')
def api_card_list():
    return jsonify(db)

@app.route('/api/card/<int:index>')
def api_card_detail(index):
    if index >=0 and index < len(db):
        return jsonify(db[index])
    return jsonify({"error": "Invalid index"})