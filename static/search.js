<!--  form의 id값을 셀렉트해서 DOM 제어  -->
const searchMovie = document.querySelector('#search');

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


// form내용이 submit 되었을 때 POST 함수 실행
searchMovie.addEventListener('submit', onSearchMovie);