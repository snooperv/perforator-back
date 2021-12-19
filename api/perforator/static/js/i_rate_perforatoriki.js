let rad1 = document.formRate[0].rates_deadlines;
let rad2 = document.formRate[0].rates_approaches;
let rad3 = document.formRate[0].rates_teamwork;
let rad4 = document.formRate[0].rates_practices;
let rad5 = document.formRate[0].rates_experience;
let rad6 = document.formRate[0].rates_adaptation;
let prev = null;
let rates = ['Значительно выше моих ожиданий', 'Немного выше моих ожиданий',
    'Немного ниже моих ожиданий', 'Значительно ниже моих ожиданий'];

for (let i = 0; i < rad1.length; i++) {
    rad1[i].onclick = function () {
        document.getElementById('text_rate1').innerHTML = rates[rad1[i].value - 1];
    };
    rad2[i].onclick = function () {
        document.getElementById('text_rate2').innerHTML = rates[rad1[i].value - 1];
    };
    rad3[i].onclick = function () {
        document.getElementById('text_rate3').innerHTML = rates[rad1[i].value - 1];
    };
    rad4[i].onclick = function () {
        document.getElementById('text_rate4').innerHTML = rates[rad1[i].value - 1];
    };
    rad5[i].onclick = function () {
        document.getElementById('text_rate5').innerHTML = rates[rad1[i].value - 1];
    };
    rad6[i].onclick = function () {
        document.getElementById('text_rate6').innerHTML = rates[rad1[i].value - 1];
    };
}

$('#deadlines, #goals, #teamwork, #techPrac, #techSkills, #adaptive').each(function () {
    let characterCount = $(this).val().length,
        current = $(this).next().find('.chars')
    $(this).keyup(function () {
        let characterCount = $(this).val().length,
            current = $(this).next().find('.chars')
        current.text(characterCount);
    })
    current.text(characterCount);
});