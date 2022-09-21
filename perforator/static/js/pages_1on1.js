$('.d-link').on('click', function () {
    $('.d-link.dactive').removeClass('dactive');
    $(this).addClass('dactive');
});

function myFunction1() {
    document.getElementById('myDropdown1').classList.toggle('show');
    document.getElementById('chev1').classList.toggle('down');
}

function myFunction2() {
    document.getElementById('myDropdown2').classList.toggle('show');
    document.getElementById('chev2').classList.toggle('down');
}

function toggleOneToOneReview(id) {
    document.getElementById('myDropdown-' + id).classList.toggle('show');
    document.getElementById('chev-' + id).classList.toggle('down');
}