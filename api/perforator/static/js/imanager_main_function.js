function get_team(){
    return fetch(window.location.origin + "/perforator/team");
}
function get_user_peers(id){
    return fetch(window.location.origin  + "/perforator/peers/uid?id=" + id)
}
function get_all_peers(){
    return fetch(window.location.origin + "/perforator/peers/all/");
}
function is_draft(id){
    let is_draft = false
    console.log(id)

    fetch(window.location.origin + "/perforator/self-review/is-draft/?id=" + id)
        .then(response => response.json())
        .then(json => {

            return json['is_draft'];
        });
    //console.log(is_draft)

    //return is_draft;
}
function replace_list_peers(list){
    let window = document.getElementById("peers")
    window.replaceChild(dict_of_list_peers[list], document.getElementById("list_peers"))
    get_user_peers(list)
        .then(response => response.json())
        .then(json => {
            for (let i of json){
                let id = i.user_id;
                save_peers_in_modal_window(list, id);
            }
        });
}


let dict_of_list_peers = {}

window.onload = function () {
    console.log('page loaded');
    get_team()
        .then(response => response.json())
        .then(json => {
            let team_list_not_approve = document.getElementById("team_not_approve");
            let team_list_approve = document.getElementById("team_approve");
            let team_without_sr = document.getElementById("team_without_self_review");
            let team_list = document.querySelector(".rating")

            let script_list = document.getElementById("script");
            let el_approve_counter = document.getElementById("approve_users_count");
            let el_not_approve_counter = document.getElementById("not_approve_users_count");
            let approve_counter = 0;
            let not_approve_counter = 0;
            let without_sr_counter = 0;

            for (let p of json) {
                const allDiv = document.createElement("div");
                const scripts = document.createElement("script");
                const employee = document.createElement("div");
                const stats = document.createElement("script")

                employee.setAttribute("id", `employee-${p['user_id']}`);
                allDiv.setAttribute("id", `peer-${p['user_id']}`);
                allDiv.classList.add("peers")
                scripts.innerHTML = `
                    function myFunction${p.user_id}() {
                        document.getElementById('myDropdown${p.user_id}').classList.toggle('show')};`

                allDiv.innerHTML = `
                    <button onclick="myFunction${p.user_id}()" id="remove_btn${p.user_id}" class="peer dropbtn">
                        <div class="peers-pic">
                            <img class="avatar" src="${p.photo}"/>
                        </div>
                        <span class="name" style="margin-left: 0">${p.username}</span>
                        <a href="#" class="chevron" id="remove_ref${p.user_id}">
                            <i class="fas fa-chevron-right"></i>
                        </a>
                    </button> 
                    <div id="myDropdown${p.user_id}" class="dropdown-content"></div>
                    `;

                employee.innerHTML = `
                    <div>
                        <div class="items rating-name">
                            <div class="peers-pic">
                                <img class="" src="${p.photo}"/>
                            </div>
                            <a href="" class="name-link">${p.username}</a>
                        </div>
                        <a href="employee" onclick="stats${p.user_id}()">
                            <div class="grade">
                                <div class="grade-number great">3.8</div>
                            </div>
                        </a>
                    </div>    
                `
                stats.innerHTML = `
                    function stats${p.user_id}(){
                        localStorage.setItem('user', ${p.user_id})
                    } 
                `

                script_list.appendChild(scripts);
                script_list.appendChild(stats);
                team_list.appendChild(employee);

                fetch(window.location.origin + "/perforator/self-review/is-draft/?id=" + p.user_id)
                    .then(response => response.json())
                    .then(json => {
                        if (json['is_draft']){
                            let el_without_sr_counter = document.getElementById("without_sr_users_count");
                            let btn = document.getElementById(`remove_btn${p.user_id}`)
                            btn.removeAttribute("onclick");
                            btn.setAttribute("style", "cursor: default")
                            document.getElementById(`remove_ref${p.user_id}`).setAttribute("style", "pointer-events: none")
                            team_without_sr.appendChild(allDiv);
                            without_sr_counter++;
                            not_approve_counter--;
                            el_without_sr_counter.innerHTML = without_sr_counter.toString();
                            el_approve_counter.innerHTML = approve_counter.toString();
                            el_not_approve_counter.innerHTML = not_approve_counter.toString();
                        }
                    });
                if (!p.approve) {
                    team_list_not_approve.appendChild(allDiv);
                    not_approve_counter++;
                }
                else {
                    team_list_approve.appendChild(allDiv);
                    approve_counter++;
                }



                let peers_list = document.createElement("div");
                let peers_tag = document.getElementById(`myDropdown${p.user_id}`)
                let peers_add = document.createElement("div");


                get_all_peers()
                    .then(response => response.json())
                    .then(json => {
                        peers_list.classList.add("dropdown-container")
                        peers_list.setAttribute("id", "my_peers");
                        peers_list.innerHTML = `<div class="dropdown-description">пиры, которых выбрал сотрудник</div>`
                        peers_tag.appendChild(peers_list)

                        let my = document.createElement("div")
                        my.setAttribute("id", "list_peers");

                        for (let u of json) {
                            const peer = document.createElement("div");
                            peer.classList.add("selected-peer")
                            peer.setAttribute("id", `my-peer${p.user_id}${u['user_id']}`);
                            peer.innerHTML = `
                                <img class="selected-peer-avatar" src="${u.photo}"/>
                                 <div class="selected-peer-name">${u.username}</div>`
                            if (!p.approve) {
                                peer.innerHTML += `
                                    <a class="close delete-peer" onclick="remove_peer_remote(${p.user_id}, ${u.user_id})">
                                        <i class="fas fa-times"></i>
                                    </a>`;
                            }
                            peer.style.display = 'none';
                            peers_list.appendChild(peer);

                            if (u.user_id == '1' || p.user_id == u.user_id) {
                                console.log(u.user_id == '1', p.user_id, u.user_id)
                                continue
                            }
                            const myDiv = document.createElement("div");
                            myDiv.setAttribute("id", `peer${p.user_id}${u.user_id}`);
                            myDiv.setAttribute("style", `margin: 0 25px 0 15px`);
                            myDiv.innerHTML = `
                                <div class="one-peer">
                                    <div class="peers-pic">
                                        <img class="avatar" src="${u.photo}"/>
                                    </div>
                                    <div style="margin-top: 0" class="peer-info">${u.username}</div>
                                    <button class="choose" onclick="select_peer_remote(${p.user_id}, ${u.user_id})">Выбрать</button>
                                </div>`;
                            my.appendChild(myDiv);
                        }

                        dict_of_list_peers[p.user_id] = my;

                        peers_add.innerHTML = `
                            <a id="choose${p.user_id}" onclick="replace_list_peers(${p.user_id})">
                                <button class="add-peer" onclick="add_peers()">
                                    <i class="icon-plus fas fa-plus"></i>
                                    Добавить пира
                                </button>
                            </a>
                            <input class="accept" type="submit" value="утвердить" onclick="approve_user(${p.user_id})"/>
                            `
                        if (!p.approve) {
                            peers_list.appendChild(peers_add)
                        }


                    })
                    .then(() => {
                        get_user_peers(p.user_id)
                            .then(response => response.json())
                            .then(json => {
                                for (let i of json){
                                    let id = i.user_id;
                                    save_peers(p.user_id, id);
                                }
                            });
                    });
            }


        })
};

function remove_peer_remote(uid, id) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch(window.location.origin + `/perforator/peers/delete/user?id=${uid}`, {
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
                delete_peers(uid, id);
            }
        });
}

// посылаем post-запрос на сервер, что пользователь выбрал пира
function select_peer_remote(uid, id) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch(window.location.origin + `/perforator/peers/save/user?id=${uid}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify([id])
    })
        .then(response => {
            if (response.ok) {
                delete_peers_in_modal_window(uid, id);
            }
        });
}

function approve_user(id) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch(window.location.origin + `/perforator/peers/approve?id=${id}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify([id])
    })
        .then(response => {
            if (response.ok) {
                window.location.reload();
            }
        });
}

// удаляем пира, скрываем и показываем нужный элемент
// вызывается при клике, вызывает remove_peer
function delete_peers(uid, id) {
    document.getElementById(`my-peer${uid}${id}`).style.display = 'none';
    //document.getElementById(`peer${uid}${id}`).style.display = 'block';
}
function delete_peers_in_modal_window(uid, id) {
    document.getElementById(`my-peer${uid}${id}`).style.display = 'block';
    document.getElementById(`peer${uid}${id}`).style.display = 'none';
}

// выбираем пира, скрываем и показываем нужный элемент
// вызывается при клике, вызывает select_peer
function save_peers(uid, id) {
    console.log(`my-peer${uid}${id}`)
    document.getElementById(`my-peer${uid}${id}`).style.display = 'block';
    //document.getElementById(`peer${uid}${id}`).style.display = 'none';
}
function save_peers_in_modal_window(uid, id) {
    //console.log(`peer${uid}${id}`)
    //document.getElementById(`my-peer${uid}${id}`).style.display = 'block';
    document.getElementById(`peer${uid}${id}`).style.display = 'none';
}
