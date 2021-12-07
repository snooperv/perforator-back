function get_team(){
            return fetch(window.location.origin + "/perforator/team");
    }
    window.onload = function () {
            console.log('page loaded');
            get_team()
                .then(response => response.json())
                .then(json => {
                    console.log(json);

                    let team_list = document.getElementById("team");
                    let script_list = document.getElementById("script");
                    var my_peers = document.getElementById("my_peers");

                    for (let p of json) {
                        console.log(p);
                        const allDiv = document.createElement("div");
                        const scripts = document.createElement("script")

                        allDiv.setAttribute("id", `peer-${p['user_id']}`);
                        allDiv.classList.add("peers")
                        scripts.innerHTML = `function myFunction${p.user_id}() {
                                                document.getElementById('myDropdown${p.user_id}').classList.toggle('show')};`
                        allDiv.innerHTML = `



    <button onclick="myFunction${p.user_id}()" class="peer dropbtn">
        <div class="peers-pic">
            <img class="avatar" src="${p.photo}"/>
        </div>
        <span class="name">${p.username}</span>
        <a href="#" class="chevron">
            <i class="fas fa-chevron-right"></i>
        </a>
    </button>
    
    <div id="myDropdown${p.user_id}" class="dropdown-content">
        <div class="dropdown-container">
            <div class="dropdown-description">пиры, которых выбрал сотрудник</div>
            <div class="selected-peer">
                <img src="{% static 'img/pic.png' %}" class="selected-peer-avatar"/>
                <span class="selected-peer-name">Коновалов Илья</span>
                <a href="#" class="delete-peer">
                    <i class="fas fa-times"></i>
                </a>
            </div>
                        
            <button class="add-peer">
                <i class="icon-plus fas fa-plus"></i>Добавить пира
            </button>
            <input class="accept" type="submit" value="утвердить"/>
        </div>
    </div>
    
    <script>
    function myFunction2() {
            document.getElementById('myDropdown1').classList.toggle('show')
        }
    </script>

`;
                        team_list.appendChild(allDiv);
                        script_list.appendChild(scripts)
                        const myDiv = document.createElement("div");
                        myDiv.setAttribute("id", `my-peer-${p.user_id}`);
                        myDiv.innerHTML = `<div class="peer-sel"><div class="peers-pic"><img class="avatar" src="${p.photo}"/></div><div class="peer-info">${p.username}</div><a class="close" onclick="remove_peer_remote(${p.user_id})"><i class="fas fa-times"></i></a></div>`;
                        myDiv.style.display = 'none';
                        //my_peers.appendChild(myDiv);
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