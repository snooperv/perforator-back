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
                    var my_peers = document.getElementById("my_peers");

                    for (let p of json) {
                        console.log(p);
                        const allDiv = document.createElement("div");
                        allDiv.setAttribute("id", `peer-${p['user_id']}`);
                        allDiv.classList.add("peers")
                        allDiv.innerHTML = `



    <button onclick="myFunction()" class="peer dropbtn">
        <div class="peers-pic">
            <img class="avatar" src="${p.photo}"/>
        </div>
        <span class="name">${p.username}</span>
        <a href="#" class="chevron">
            <i class="fas fa-chevron-right"></i>
        </a>
    </button>

`;
                        team_list.appendChild(allDiv);

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