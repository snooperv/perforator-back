$.ajax({
    type: 'GET',
    cache: false,
    dataType: 'json',
    url: '/perforator/team',
    data: 'string=1234',
    success: function (data) {
        console.log(data.length);
        if (data.length >= 1) {
            document.getElementById('i_manager_button').style.display = "block";
        }
    }
});