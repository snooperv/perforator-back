console.log('Buttons script enabled');
let btn_add = document.querySelector('#btn_add');
let btn_close1 = document.querySelector('#btn_close1');
let btn_close2 = document.querySelector('#btn_close2');
let addPeers = document.getElementById('peers');
function add_peers() {
    addPeers.style.visibility = 'visible';
    addPeers.style.opacity = '1';
    btn_close2.style.visibility = 'visible';
    btn_close2.style.opacity = '1';
}

function close_peers1() {
    addPeers.style.visibility = 'hidden';
    addPeers.style.opacity = '0';
    btn_close2.style.visibility = 'hidden';
    btn_close2.style.opacity = '0';
}

function close_peers2() {
    addPeers.style.visibility = 'hidden';
    addPeers.style.opacity = '0';
    btn_close2.style.visibility = 'hidden';
    btn_close2.style.opacity = '0';
}
