from flask import Flask, request, session, redirect, url_for, render_template, flash
from py2neo import Graph
from models import query_ymm, all_sorted, query_price
import json

app = Flask(__name__)
graph = Graph()


@app.route('/')
def index():
    results = all_sorted()
    return render_template('index.html', results=results)


@app.route('/car_model', methods=['GET', 'POST'])
def car_model():
    make = request.form['make']
    model = request.form['model']
    year = request.form['year']
    sortby = request.form['sortby']
    results = query_ymm(year, make, model, sortby)
    return render_template("list.html", results=results, make=make, model=model, year=year, sortby=sortby)


@app.route('/price_range', methods=['GET', 'POST'])
def price_range():
    price = request.form['price']
    sortby = request.form['sortby']
    results = query_price(price, sortby)
    return render_template("list.html", results=results, price=price, sortby=sortby)
if __name__ == '__main__':
    app.run()
