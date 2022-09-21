function get_team() {
    return fetch(window.location.origin + "/perforator/team");
}

function get_user_peers(id) {
    return fetch(window.location.origin + "/perforator/peers/uid?id=" + id)
}

function get_all_peers() {
    return fetch(window.location.origin + "/perforator/peers/all/");
}

function get_rates(id) {
    return fetch(window.location.origin + "/perforator/imanager/employee/rating?id=" + id);
}

function is_draft(id) {
    let is_draft = false
    console.log(id)

    fetch(window.location.origin + "/perforator/self-review/is-draft/?id=" + id)
        .then(response => response.json())
        .then(json => {

            return json['is_draft'];
        });
}

function replace_list_peers(list) {
    let window = document.getElementById("peers")
    window.replaceChild(dict_of_list_peers[list], document.getElementById("list_peers"))
    get_user_peers(list)
        .then(response => response.json())
        .then(json => {
            for (let i of json) {
                let id = i.user_id;
                save_peers_in_modal_window(list, id);
            }
        });
}


let dict_of_list_peers = {}
let average_rate = {
    'averages': {
            'time': 0.0,
            'target': 0.0,
            'teamwork': 0.0,
            'practices': 0.0,
            'technologies': 0.0,
            'adaptive': 0.0,
            'average': 0.0
    },
    'count': 0
}

window.onload = function () {
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
                get_rates(p.user_id)
                    .then(response => response.json())
                    .then(rate => {
                        let final_rate = get_rates_array(rate)
                        const allDiv = document.createElement("div");
                        const scripts = document.createElement("script");
                        const employee = document.createElement("div");
                        const stats = document.createElement("script")
                        let color = ''
                        employee.setAttribute("id", `employee-${p['user_id']}`);
                        allDiv.setAttribute("id", `peer-${p['user_id']}`);
                        allDiv.classList.add("peers")
                        scripts.innerHTML = `
                            function myFunction${p.user_id}() {
                                document.getElementById('myDropdown${p.user_id}').classList.toggle('show')};`

                        allDiv.innerHTML = `
                            <button onclick="myFunction${p.user_id}()" id="remove_btn${p.user_id}" class="peer dropbtn">
                                <div class="peers-pic-manager">
                                    <img class="avatar" src="${p.photo}"/>
                                </div>
                                <span class="name" style="margin-left: 0">${p.username}</span>
                                <a href="#" class="chevron" id="remove_ref${p.user_id}">
                                    <i class="fas fa-chevron-right"></i>
                                </a>
                            </button> 
                            <div id="myDropdown${p.user_id}" class="dropdown-content"></div>
                            `;
                        if (final_rate["averages"]["average"] < 2) {
                            color = 'bad'
                        } else if (final_rate["averages"]["average"] >= 3) {
                            color = 'great'
                        } else {
                            color = 'good'
                        }
                        employee.innerHTML = `
                            <div>
                                <div class="items rating-name">
                                    <a href="employee" onclick="stats${p.user_id}()" class="name-link">
                                        <div class="peers-pic-raiting"">
                                            <img class="avatar" src="${p.photo}"/>
                                        </div>
                                    </a>
                                    <a href="employee" onclick="stats${p.user_id}()" class="name-link">${p.username}</a>
                                </div>
                                <a href="employee" onclick="stats${p.user_id}()">
                                    <div class="grade">
                                        <div class="grade-number ${color}">${Number(final_rate["averages"]["average"]).toFixed(2).toString()}</div>
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
                                if (json['is_draft']) {
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
                        } else {
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
                                            <div class="peer-info">${u.username}</div>
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
                                        for (let i of json) {
                                            let id = i.user_id;
                                            save_peers(p.user_id, id);
                                        }
                                        for (let i in average_rate["averages"]) {
                                            let el = document.getElementById(i);
                                            el.innerHTML = Number(average_rate["averages"][i] / average_rate["count"]).toFixed(2).toString();
                                            get_color((average_rate["averages"][i] / average_rate["count"]), el)
                                        }
                                    });
                            });
                    }
                )}
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
function delete_peers(uid, id) {
    document.getElementById(`my-peer${uid}${id}`).style.display = 'none';
    document.getElementById(`peer${uid}${id}`).style.display = 'block';
}
function delete_peers_in_modal_window(uid, id) {
    document.getElementById(`my-peer${uid}${id}`).style.display = 'block';
    document.getElementById(`peer${uid}${id}`).style.display = 'none';
}
function save_peers(uid, id) {
    document.getElementById(`my-peer${uid}${id}`).style.display = 'block';
}
function save_peers_in_modal_window(uid, id) {
    document.getElementById(`peer${uid}${id}`).style.display = 'none';
}
function get_rates_array(json) {
    let u = json[0]
    let count = 0;
    let final_rate = {
        'manager': {
            'time': 0.0,
            'target': 0.0,
            'teamwork': 0.0,
            'practices': 0.0,
            'technologies': 0.0,
            'adaptive': 0.0,
            'average': 0.0
        },
        'peers': {
            'time': 0.0,
            'target': 0.0,
            'teamwork': 0.0,
            'practices': 0.0,
            'technologies': 0.0,
            'adaptive': 0.0,
            'average': 0.0
        },
        'averages': {
            'time': 0.0,
            'target': 0.0,
            'teamwork': 0.0,
            'practices': 0.0,
            'technologies': 0.0,
            'adaptive': 0.0,
            'average': 0.0
        }
    }

    for (let r of u.rates) {
        if ((r['is_manager'])) {
            let average = 0.0;
            final_rate['manager']['time'] = Number(r['r_deadline']);
            average += Number(r['r_deadline']);
            final_rate['manager']['target'] = r['r_approaches'];
            average += r['r_approaches'];
            final_rate['manager']['teamwork'] = r['r_teamwork'];
            average += r['r_teamwork'];
            final_rate['manager']['practices'] = r['r_practices'];
            average += r['r_practices'];
            final_rate['manager']['technologies'] = r['r_experience'];
            average += r['r_experience'];
            final_rate['manager']['adaptive'] = r['r_adaptation'];
            average += r['r_adaptation'];
            final_rate['manager']['average'] = (average / 6).toFixed(2);
        } else {
            count++;
            final_rate['peers']['time'] += Number(r['r_deadline']);
            final_rate['peers']['target'] += r['r_approaches'];
            final_rate['peers']['teamwork'] += r['r_teamwork'];
            final_rate['peers']['practices'] += r['r_practices'];
            final_rate['peers']['technologies'] += r['r_experience'];
            final_rate['peers']['adaptive'] += r['r_adaptation'];
        }
    }
    let average = 0.0;
    for (let r in final_rate["peers"]) {
        final_rate["peers"][r] /= count;
        final_rate["peers"][r] = final_rate["peers"][r]
        average += final_rate["peers"][r];
    }
    final_rate["peers"]['average'] = (average / 6).toFixed(2);


    final_rate['averages']['time'] = (final_rate['peers']['time'] + final_rate['manager']['time']) / 2;
    average_rate['averages']["time"] += final_rate['averages']['time'];
    final_rate['averages']['target'] = (final_rate['peers']['target'] + final_rate['manager']['target']) / 2;
    average_rate['averages']["target"] += final_rate['averages']['target'];
    final_rate['averages']['teamwork'] = (final_rate['peers']['teamwork'] + final_rate['manager']['teamwork']) / 2;
    average_rate['averages']["teamwork"] += final_rate['averages']['teamwork'];
    final_rate['averages']['practices'] = (final_rate['peers']['practices'] + final_rate['manager']['practices']) / 2;
    average_rate['averages']["practices"] += final_rate['averages']['practices'];
    final_rate['averages']['technologies'] = (final_rate['peers']['technologies'] + final_rate['manager']['technologies']) / 2;
    average_rate['averages']["technologies"] += final_rate['averages']['technologies'];
    final_rate['averages']['adaptive'] = (final_rate['peers']['adaptive'] + final_rate['manager']['adaptive']) / 2;
    average_rate['averages']["adaptive"] += final_rate['averages']['adaptive'];
    final_rate['averages']['average'] = (Number(final_rate['peers']['average']) + Number(final_rate['manager']['average'])) / 2;
    average_rate['averages']["average"] += final_rate['averages']['average'];
    average_rate['count']++;
    return final_rate;
}

function get_color(num, el) {
    if (num < 2) {
        el.classList.add('bad')
    } else if (num >= 3) {
        el.classList.add('great')
    } else {
        el.classList.add('good')
    }
}