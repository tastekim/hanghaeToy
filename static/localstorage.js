const loginForm = document.querySelector("#login-form")
const loginInput = document.querySelector("#login-form input");
const loginUser = document.querySelector("#greeting");
const searchBar = document.getElementById("search");

const HIDDEN_CLASSNAME = "hidden"
const USER_KEY = "user"

function onLoginSubmit(event) {
    event.preventDefault();
    const username = loginInput.value;
    loginForm.classList.add(HIDDEN_CLASSNAME);
    localStorage.setItem(USER_KEY, username);
    showUserName(username);
    searchBar.style.visibility = 'visible'
}

function showUserName(username) {
    loginUser.classList.remove(HIDDEN_CLASSNAME);
    loginUser.innerText = `Hello ${username}`;
}

const savedUserName = localStorage.getItem(USER_KEY);

if (savedUserName === null) {
    loginForm.addEventListener("submit", onLoginSubmit);
} else {
    loginForm.classList.add(HIDDEN_CLASSNAME);
    showUserName(savedUserName);
}
