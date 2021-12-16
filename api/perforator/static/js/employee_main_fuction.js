window.onload = function (){
    alert("hellow")
    get_team()
        .then(response => response.json())
        .then(json => {
            alert("hellow")
        });
}