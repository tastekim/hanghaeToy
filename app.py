from pymongo import MongoClient
import certifi

from bs4 import BeautifulSoup
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/movie', methods=['GET'])
def movie_get():
    return jsonify({'msg' : 'GET 완료!'})

@app.route('/movie', methods=['POST'])
def movie_post():
    search_receive = request.form['search_give']
    return jsonify({'msg' : 'POST 완료!'})

@app.route('/favorite', methods=['GET'])
def favorite_get():
    return jsonify({'msg' : '찜 목록 GET 완료!'})

@app.route('/favorite', methods=['POST'])
def favorite_post():
    search_receive = request.form['search_give']
    return jsonify({'msg' : '찜 POST 완료!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000)
