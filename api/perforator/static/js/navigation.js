/*window.onload = async function () {
    fetch(window.location.origin + "/perforator/team")
        .then(response => response.json())
        .then(json => {
            let link = document.getElementById('i_manager_button')
            if (!json.length < 1) {
                link.style.display = "block";
            }
            console.log(json.length)
            console.log(link.href)
        })
};*/

try {
    var el = document.getElementById('menuItems').getElementsByTagName('a');
    var nav = document.getElementById('menuItems').getElementsByTagName('nav');
    var url = document.location.href;
    for (var i = 0; i < el.length; i++) {
        if (url === el[i].href || url === el[i].href + '#popup' || url === el[i].href + '#') {
            nav[i].className += ' active';
        }
    }
} catch (e) {
}