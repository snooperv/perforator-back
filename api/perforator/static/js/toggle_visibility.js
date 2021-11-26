document.addEventListener('DOMContentLoaded', function () {
    let btn_change = document.querySelector('#btn-change');
    let btn_cancel = document.querySelector('#btn_cancel');
    let changeData = document.getElementById('changeData');
    let popup = document.getElementById('popup');
    btn_change.addEventListener('click', function() {
        changeData.style.visibility = 'visible';
        popup.style.visibility = 'hidden';
        changeData.style.opacity = '1';
        popup.style.opacity = '0';
      });
    btn_cancel.addEventListener('click', function() {
        changeData.style.visibility = 'hidden';
        popup.style.visibility = 'visible';
        changeData.style.opacity = '0';
        popup.style.opacity = '1';
      });
    /*if (changeData.style.visibility === 'hidden') {
        changeData.style.visibility = 'visible';
        popup.style.visibility = 'hidden';
    } else {
        changeData.style.visibility = 'hidden';
        popup.style.visibility = 'visible';
    }*/
})