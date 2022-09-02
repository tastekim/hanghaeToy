<!--  form의 id값을 셀렉트해서 DOM 제어  -->
const searchMovie = document.querySelector('#search');
const favorite = document.querySelector('#register-favorite')
const removeFavorite = document.querySelector('#remove-favorite')

$(document).ready(function () {
    showMovie();
});

function showMovie() {
    $.ajax({
        type: "GET",
        url: "/movie",
        data: {},
        success: function (response) {
            alert(response["msg"]);
        }
    });
};

function onSearchMovie(event) {
    // submit 되면 새로고침 되는게 defalt여서 ajax 실행 전에 새로고침 되는걸 방지.
    event.preventDefault();

    let search = event.target[0].value;

    // 검색한 영화 localStorage에 담아둔 후 favorite 기능에 사용
    localStorage.setItem('search', search);

    $.ajax({
        type: "POST",
        url: "/movie",
        data: {search_give: search},
        success: function (response) {
            alert(response["msg"]);
            window.location.reload();
        }
    });
};

function onFavoriteMovie() {
    // 현재 검색한 영화 localStorage 에서 가져오기
    favorite_movie = localStorage.getItem('search');
    user_name = localStorage.getItem('user');

    $.ajax({
        type: "POST",
        url: "/movie/favorite",
        data: {favorite_give: favorite_movie, user_give: user_name},
        success: function (response) {
            alert(response["msg"]);
        }
    });
};

function onRemoveFavorite() {
    $.ajax({
        type: "POST",
        url: "/movie/remove",
        data: {remove_give: ""},
        success: function (response) {
            alert(response["msg"]);
        }
    });
};

// form내용이 submit 되었을 때 POST 함수 실행
searchMovie.addEventListener('submit', onSearchMovie);
favorite.addEventListener('click', onFavoriteMovie);
removeFavorite.addEventListener('click', onRemoveFavorite);