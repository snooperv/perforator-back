let test = document.formRate;
let rad1 = [];
let rad2 = [];
let rad3 = [];
let rad4 = [];
let rad5 = [];
let rad6 = [];
for (let i = 0; i < test.length; i++) {
    rad1[i] = document.getElementsByClassName('radio-' + (i + 1) + '-1');
    rad2[i] = document.getElementsByClassName('radio-' + (i + 1) + '-2');
    rad3[i] = document.getElementsByClassName('radio-' + (i + 1) + '-3');
    rad4[i] = document.getElementsByClassName('radio-' + (i + 1) + '-4');
    rad5[i] = document.getElementsByClassName('radio-' + (i + 1) + '-5');
    rad6[i] = document.getElementsByClassName('radio-' + (i + 1) + '-6');
}

let prev = null;
let rates = ['Значительно ниже моих ожиданий', 'Немного ниже моих ожиданий',
    'Немного выше моих ожиданий', 'Значительно выше моих ожиданий'];

for (let j = 0; j < test.length; j++) {
    for (let i = 0; i < rad1[j].length; i++) {
        rad1[j][i].onclick = function () {
            document.getElementById('text-rate-' + (j + 1) + '-1').innerHTML = rates[rad1[j][i].value - 1];
        };
        rad2[j][i].onclick = function () {
            document.getElementById('text-rate-' + (j + 1) + '-2').innerHTML = rates[rad1[j][i].value - 1];
        };
        rad3[j][i].onclick = function () {
            document.getElementById('text-rate-' + (j + 1) + '-3').innerHTML = rates[rad1[j][i].value - 1];
        };
        rad4[j][i].onclick = function () {
            document.getElementById('text-rate-' + (j + 1) + '-4').innerHTML = rates[rad1[j][i].value - 1];
        };
        rad5[j][i].onclick = function () {
            document.getElementById('text-rate-' + (j + 1) + '-5').innerHTML = rates[rad1[j][i].value - 1];
        };
        rad6[j][i].onclick = function () {
            document.getElementById('text-rate-' + (j + 1) + '-6').innerHTML = rates[rad1[j][i].value - 1];
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