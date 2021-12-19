let test = document.formRate;
console.log(test);
let rad1 = [];
let rad2 = [];
let rad3 = [];
let rad4 = [];
let rad5 = [];
let rad6 = [];
for (let i = 0; i < test.length; i++) {
    rad1[i] = document.formRate[i].rates_deadlines;
    rad2[i] = document.formRate[i].rates_approaches;
    rad3[i] = document.formRate[i].rates_teamwork;
    rad4[i] = document.formRate[i].rates_practices;
    rad5[i] = document.formRate[i].rates_experience;
    rad6[i] = document.formRate[i].rates_adaptation;
}

console.log(rad1);

let prev = null;
let rates = ['Значительно выше моих ожиданий', 'Немного выше моих ожиданий',
    'Немного ниже моих ожиданий', 'Значительно ниже моих ожиданий'];

for (let j = 0; j < test.length; j++) {
    for (let i = 0; i < rad1[j].length; i++) {
        rad1[j][i].onclick = function () {
            document.getElementById('text_rate1').innerHTML = rates[rad1[j][i].value - 1];
        };
        rad2[j][i].onclick = function () {
            document.getElementById('text_rate2').innerHTML = rates[rad1[j][i].value - 1];
        };
        rad3[j][i].onclick = function () {
            document.getElementById('text_rate3').innerHTML = rates[rad1[j][i].value - 1];
        };
        rad4[j][i].onclick = function () {
            document.getElementById('text_rate4').innerHTML = rates[rad1[j][i].value - 1];
        };
        rad5[j][i].onclick = function () {
            document.getElementById('text_rate5').innerHTML = rates[rad1[j][i].value - 1];
        };
        rad6[j][i].onclick = function () {
            document.getElementById('text_rate6').innerHTML = rates[rad1[j][i].value - 1];
        };
    }
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