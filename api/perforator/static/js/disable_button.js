
function remove_button_imanager() {
    fetch(window.location.origin + "/perforator/team")
        .then(response => response.json())
        .then(json => {
            let link = document.getElementById('i_manager_button')
            if (json.length >= 1){
                link.style.display = "block";
            }
        })
};
