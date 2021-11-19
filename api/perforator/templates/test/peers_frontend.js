// ВАЖНО!
// 1) Рекомендую сначала посмотреть peers.py (я там написал хорошую (надеюсь) документацию),
// а также raw_peers_views.py - там прописаны роуты
// 2) Обращаю внимание, что в <head> подключаем библиотеку JQuery
// 3) Чтобы пользоваться, нужно обязательно АВТОРИЗОВАТЬСЯ
// 4) window.location.origin - для того, чтобы работало и на localhost, и на удаленном сервере


// при загрузке страницы мы сразу заполняем my_peers и peers_list
// всеми возможными вариантами (пользователями), а потом просто
// меняем у них visibility
// Если у вас есть другой вариант реализации - можете его реализовать
$(function(){

    get_all_peers()
        .then(response => response.json())
        .then(json => {
            var peers_list = document.getElementById("peers_list");
            var my_peers = document.getElementById("my_peers");

            for (var p in json) {
                const allDiv = document.createElement("div");
                allDiv.setAttribute("id", `peer-${p.user_id}`);
                allDiv.innerHTML = `photo: ${p.photo} | ${p.username} | <button onclick="save_peers(${p.user_id})"> Выбрать </button>`;
                peers_list.appendChild(allDiv);

                const myDiv = document.createElement("div");
                myDiv.setAttribute("id", `my-peer-${p.user_id}`);
                myDiv.innerHTML = `photo: ${p.photo} | ${p.username} | <button onclick="delete_peers(${p.user_id})"> Удалить </button>`;
                my_peers.appendChild(myDiv);
            }
        });

    get_my_peers()
        .then(response => response.json())
        .then(json => {

        });

});


// посылаем post-запрос на сервер, что пользователь выбрал пира
function select_peer(id){
    return fetch(window.location.origin + "/perforator/peers/save/", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify([id])
    });
}


// посылаем post-запрос на сервер, что пользователь удалил пира из выбранных
function remove_peer(id){
    return fetch(window.location.origin + "/perforator/peers/delete/", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify([id])
    });
}


// получить всех возможных пиров - get-запрос
// (пока это все пользователи)
function get_all_peers(){
    return fetch(window.location.origin + "/perforator/peers/all/");
}


// получить выбранных пиров пользователя - get-запрос
// используется только при загрузке страницы
function get_my_peers(){
    return fetch(window.location.origin + "/perforator/peers/my/");
}


// удаляем пира, скрываем и показываем нужный элемент
// вызывается при клике, вызывает remove_peer
function delete_peers(id){
    document.getElementById(`my-peer-${id}`).style.visibility = 'hidden';
}


// выбираем пира, скрываем и показываем нужный элемент
// вызывается при клике, вызывает select_peer
function save_peers(id){
    document.getElementById(`my-peer-${id}`).style.visibility = 'visible';
}
