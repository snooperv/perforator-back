function get_team(){
    return fetch(window.location.origin + "/perforator/team");
}
function get_user_peers(id){
    return fetch(window.location.origin  + "/perforator/peers/uid?id=" + id)
}
window.onload = function () {
    console.log('page loaded');
    get_team()
        .then(response => response.json())
        .then(json => {
            let team_list = document.getElementById("team");
            let script_list = document.getElementById("script");
            var my_peers = document.getElementById("list_peers");

            for (let p of json) {
                const allDiv = document.createElement("div");
                const peers = document.createElement("div");
                const scripts = document.createElement("script");

                allDiv.setAttribute("id", `peer-${p['user_id']}`);
                allDiv.classList.add("peers")
                scripts.innerHTML = `function myFunction${p.user_id}() {
                                        document.getElementById('myDropdown${p.user_id}').classList.toggle('show')};`
                allDiv.innerHTML = `
                    <button onclick="myFunction${p.user_id}()" class="peer dropbtn">
                        <div class="peers-pic">
                            <img class="avatar" src="${p.photo}"/>
                        </div>
                        <span class="name" style="margin-left: 0">${p.username}</span>
                        <a href="#" class="chevron">
                            <i class="fas fa-chevron-right"></i>
                        </a>
                    </button> 
                    <div id="myDropdown${p.user_id}" class="dropdown-content"></div>
    
                    <script>
                        function myFunction2() {
                            document.getElementById('myDropdown1').classList.toggle('show')
                        }
                    </script>`;

                team_list.appendChild(allDiv);
                script_list.appendChild(scripts)
                
                const myDiv = document.createElement("div");
                myDiv.setAttribute("id", `my-peer-${p.user_id}`);
                myDiv.innerHTML = `
                    <div class="peer-sel">
                        <div class="peers-pic">
                            <img class="avatar" src="${p.photo}"/>
                        </div>
                        <div style="margin-top: 0" class="peer-info">${p.username}</div>
                        <button class="choose" onclick="select_peer_remote(${p.user_id})">Выбрать</button>
                    </div>`;
                //myDiv.style.display = 'none';
                my_peers.appendChild(myDiv);



                let peers_list = document.createElement("div");
                let peers_tag = document.getElementById(`myDropdown${p.user_id}`)
                let peers_add = document.createElement("div");

                get_user_peers(p.user_id)
                    .then(response => response.json())
                    .then(json => {
                        peers_list.classList.add("dropdown-container")
                        peers_list.setAttribute("id", "my_peers");
                        peers_list.innerHTML = `<div class="dropdown-description">пиры, которых выбрал сотрудник</div>`
                        peers_tag.appendChild(peers_list)

                        for (let u of json) {
                            const peer = document.createElement("div");
                            peer.classList.add("selected-peer")
                            peer.setAttribute("id", `my-peer-${u['user_id']}`);
                            peer.innerHTML = `
                                <img class="selected-peer-avatar" src="${u.photo}"/>
                                 <span class="selected-peer-name">${u.username}</span>       
                                 <a class="close delete-peer" onclick="remove_peer_remote(${u.user_id})">
                                    <i class="fas fa-times"></i>
                                 </a>`;
                            peers_list.appendChild(peer);
                        }

                        peers_add.innerHTML = `
                            <a href="#peers">
                                <button class="add-peer">
                                    <i class="icon-plus fas fa-plus"></i>
                                    Добавить пира
                                </button>
                                <input class="accept" type="submit" value="утвердить"/>
                            </a>`
                        peers_list.appendChild(peers_add)
                    })
            }
        })
        .then(() => {
            get_my_peers()
                .then(response => response.json())
                .then(json => {
                    console.log(json);
                    for (var p of json){
                        var id = p.user_id;
                        save_peers(id);
                    }
                });
        });
};

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
                console.log(response.json())
                delete_peers(id);
            }
        });
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

// удаляем пира, скрываем и показываем нужный элемент
// вызывается при клике, вызывает remove_peer
function delete_peers(id) {
    document.getElementById(`my-peer-${id}`).style.display = 'none';
    //document.getElementById(`peer-${id}`).style.display = 'block';
}

// выбираем пира, скрываем и показываем нужный элемент
// вызывается при клике, вызывает select_peer
function save_peers(id) {
    //document.getElementById(`my-peer-${id}`).style.display = 'block';
    //document.getElementById(`peer-${id}`).style.display = 'none';
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