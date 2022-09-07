from pymongo import MongoClient
import certifi, requests, re
from urllib import parse

from bs4 import BeautifulSoup
from flask import Flask, render_template, request, jsonify

# db 연결
ca = certifi.where()
client = MongoClient('mongodb+srv://test:sparta@cluster0.2jrn8.mongodb.net/Cluster0?retryWrites=true&w=majority', tlsCAFile = ca)
db = client.searchingMovie

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/movie', methods=['GET'])
def favorite_get():
    favorite_list = list(db.favorite.find({}, {'_id': False}))
    return jsonify({'favorites': favorite_list})

@app.route('/movie', methods=['POST'])
def movie_post():
    search_receive = request.form['search_give']

    # 네이버 검색 url에 search_receive를 query문으로 변환 후 붙여주기
    url = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query='
    newUrl = url + parse.quote(search_receive)
    data = requests.get(newUrl, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    # 네이버 영화 검색 시 상단에 있는 영화정보 안 제목에 있는 '네이버 영화 정보 페이지' url 크롤링
    link = soup.find('strong', '_text')
    a_link = link.find('a')
    movie_link = a_link.attrs['href']

    # 기존 url을 '네이버 영화 정보 페이지' url로 바꿔준 후 meta tag 크롤링
    url = movie_link
    data = requests.get(url, headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    movie_title = soup.select_one('meta[property="og:title"]')['content']
    movie_desc = soup.select_one('meta[property="og:description"]')['content']
    movie_image = soup.select_one('meta[property="og:image"]')['content']

    # 점수는 str 이랑 int가 섞여 있어서 re.sub()을 이용해 문자열을 전부 제거한 후( '.' 까지 제거된다.) int로 변환해서 1/100을 곱해주면 기존의 점수가 나온다.
    rank = soup.select_one('#actualPointPersentBasic > div > span > span').text
    a = re.sub(r'[^0-9]', '', rank)
    movie_rank = int(a) * 1/100

    doc = {
        'movie_title' : movie_title,
        'movie_desc' : movie_desc,
        'movie_image' : movie_image,
        'movie_rank' : movie_rank
    }

    # 영화 정보 movie 컬렉션에 저장
    db.movie.insert_one(doc)

    return jsonify({'msg' : '검색 완료!'})

@app.route("/search", methods=["GET"])
def web_movies_get():
    movie_list = list(db.movie.find({}, {'_id': False}))
    return jsonify({'movies': movie_list})

@app.route("/review", methods=["GET"])
def web_reviews_get():
    review_list = list(db.reviews.find({}, {'_id': False}))
    return jsonify({'reviews': review_list})

@app.route('/movie/favorite', methods=['POST'])
def favorite_post():
    favorite_receive = request.form['favorite_give']
    user_receive = request.form['user_give']

    # 유저의 이름과 찜한 영화 묶어서 저장
    doc = {
        'user' : user_receive,
        'favorite' : favorite_receive
    }
    db.favorite.insert_one(doc)
    return jsonify({'msg' : '찜 POST 완료!'})

@app.route('/movie/remove', methods=['POST'])
def favorite_remove():
    remove_receive = request.form['remove_give']
    return jsonify({'msg' : '찜 삭제 POST 완료!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000)
