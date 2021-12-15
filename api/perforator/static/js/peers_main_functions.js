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
window.onload = function () {
    console.log('page loaded');
    //self_review_main();

    fetch(window.location.origin + "/perforator/manager")
    .then(response => response.json())
        .then(manager => {

            get_all_peers()
                .then(response => response.json())
                .then(json => {
                    let peers_list = document.getElementById("list_peers");
                    let my_peers = document.getElementById("my_peers");

                    for (let p of json) {
                        if (manager.message === "ok")
                            if (manager.user_id === p.user_id)
                                continue
                        if (p.user_id == '1') {
                                //console.log(u.user_id == '1', p.user_id, u.user_id)
                            continue
                        }
                        const allDiv = document.createElement("div");
                        allDiv.setAttribute("id", `peer-${p['user_id']}`);
                        allDiv.setAttribute("style", `margin: 0 25px 0 5px`);
                        allDiv.innerHTML =
                            `<div class="one-peer">
                                <div class="peers-pic">
                                    <img class="avatar" src="${p.photo}"/>
                                </div>
                                <div class="peer-info">
                                    ${p.username}
                                </div>
                                <button class="choose" onclick="select_peer_remote(${p.user_id})">Выбрать</button>
                            </div>`;
                        peers_list.appendChild(allDiv);

                        const myDiv = document.createElement("div");
                        myDiv.setAttribute("id", `my-peer-${p.user_id}`);
                        myDiv.innerHTML =
                            `<div class="peer-sel">
                                <div class="peers-pic">
                                    <img class="avatar" src="${p.photo}"/>
                                </div>
                                <div class="peer-info">
                                    ${p.username}
                                </div>
                                <a class="close" id="close" onclick="remove_peer_remote(${p.user_id})">
                                    <i class="close-icon fas fa-times"></i>
                                </a>
                            </div>`;
                        myDiv.style.display = 'none';
                        my_peers.appendChild(myDiv);
                    }
                })
                .then(() => {
                    get_my_peers()
                        .then(response => response.json())
                        .then(json => {
                            for (let p of json) {
                                let id = p.user_id;
                                save_peers(id);
                            }
                        })
                        .then(() => {
                            get_my_peers()
                                .then(response => response.json())
                                .then(json => {

                                    for (let p of json) {
                                        let id = p.user_id;
                                        save_peers(id);

                                    }
                                    check_free_fields_onload();
                                    get_self_review()
                                        .then(response => response.json())
                                        .then(json => {
                                           let is_draft = json['is_draft']
                                           if (!is_draft) {
                                               disable_btn_peers();
                                               disable_btn_send();
                                           }
                                        });
                                });
                        });
                });
    })
    self_review_main();
}

// посылаем post-запрос на сервер, что пользователь выбрал пира
function select_peer_remote(id) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch(window.location.origin + "/perforator/peers/save/", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify([id])
    })
        .then(response => {
            if (response.ok) {
                save_peers(id);
            }
        });
}


// посылаем post-запрос на сервер, что пользователь удалил пира из выбранных
function remove_peer_remote(id) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch(window.location.origin + "/perforator/peers/delete/", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify([id])
    })
        .then(response => {
            if (response.ok) {
                delete_peers(id);
            }
        });
    ;
}


// получить всех возможных пиров - get-запрос
// (пока это все пользователи)
function get_all_peers() {
    return fetch(window.location.origin + "/perforator/peers/all/");
}


// получить выбранных пиров пользователя - get-запрос
// используется только при загрузке страницы
function get_my_peers() {
    return fetch(window.location.origin + "/perforator/peers/my/");
}


// удаляем пира, скрываем и показываем нужный элемент
// вызывается при клике, вызывает remove_peer
function delete_peers(id) {
    document.getElementById(`my-peer-${id}`).style.display = 'none';
    document.getElementById(`peer-${id}`).style.display = 'block';
    check_peers_list();
}

// выбираем пира, скрываем и показываем нужный элемент
// вызывается при клике, вызывает select_peer
function save_peers(id) {
    document.getElementById(`my-peer-${id}`).style.display = 'block';
    document.getElementById(`peer-${id}`).style.display = 'none';
    check_peers_list();
}