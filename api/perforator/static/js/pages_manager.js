$('.d-link').on('click', function () {
    $('.d-link.dactive').removeClass('dactive');
    $(this).addClass('dactive');
});

function myFunction() {
    document.getElementById('myDropdown').classList.toggle('show')
};