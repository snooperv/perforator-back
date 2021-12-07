
window.onload = function () {
    get_team()
        .then(response => response.json())
        .then(json => {
            let link = document.getElementById('i_manager_button')
            if (!json.length >= 1){
                link.href = ''
                link.classList.add("imanager_disable")
            }
            console.log(json.length)
            console.log(link.href)
        })
};

function get_team(){
    return fetch(window.location.origin + "/perforator/team");
}