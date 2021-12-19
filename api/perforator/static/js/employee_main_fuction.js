window.onload = function () {
    get_rates(localStorage['user'])
        .then(response => response.json())
        .then(json => {
            let u = json[0]
            let final_rate = get_rates_array(json)
            set_value(final_rate, "manager")
            set_value(final_rate, "peers")
            set_value(final_rate, "averages")
            set_manager_review(u);
        })
    set_self_review();
}

function set_self_review() {
    get_self_review(localStorage['user'])
        .then(response => response.json())
        .then(json => {
            let selfReview = document.getElementById("self-review");
            let flag = '';
            let el_id = 0;
            for (let grade of json['grades']) {
                const allDiv = document.createElement("div");
                allDiv.setAttribute("id", `id${grade.id}`)
                allDiv.setAttribute("class", `self-review-manager-result gray-border`)
                if (flag != grade.grade_category_name) {
                    allDiv.innerHTML =
                        `
                                <h4 id="theme${grade.id}" class="grade_category_name">${grade.grade_category_name}</h4>
                                <p class="description">${grade.grade_category_preview_description}</p>
                            `
                    if (grade.grade_category_description != null) {
                        allDiv.innerHTML += `
                                        <p class="question">${grade.grade_category_description}</p>
                                        <div class="white-border">
                                            <div class="text-in-self">
                                                <span class="description">${grade.comment}</span>
                                            </div>
                                        </div>
                                    `;
                    } else {
                        allDiv.innerHTML += `
                                    <div class="white-border">
                                        <div class="text-in-self">
                                            <span class="description">${grade.comment}</span>
                                        </div>
                                    </div>
                                `;
                    }
                    flag = grade.grade_category_name;
                    el_id = grade.id;
                    selfReview.appendChild(allDiv);
                } else {
                    let container = document.getElementById(`id${el_id}`)
                    let p = document.createElement("p");
                    p.setAttribute("class", "question")
                    p.innerHTML = `${grade.grade_category_description}`;

                    let input = document.createElement("div");
                    input.setAttribute("class", "white-border");
                    input.innerHTML = `
                                <div class="text-in-self">
                                    <span class="description">${grade.comment}</span>
                                </div>
                            `;
                    container.appendChild(p);
                    container.appendChild(input);
                }
            }
            $('#plan, #imp-zones').each(function () {
                let characterCount = $(this).val().length,
                    current = $(this).next().find('.chars')
                $(this).keyup(function () {
                    let characterCount = $(this).val().length,
                        current = $(this).next().find('.chars')
                    current.text(characterCount);
                })
                current.text(characterCount);
            });
        })
}

function set_manager_review(u) {
    for (let r of u.rates) {
        if (!r['is_manager']) {
            continue
        }
        for (let i in r) {
            let el = document.getElementById(i);
            if (el == null) continue
            el.innerHTML += r[i];
        }
    }
}

function set_value(final_rate, name) {
    for (let i in final_rate[name]) {
        let el = document.getElementById(i + '_avg_' + name);
        el.innerHTML = Number(final_rate[name][i]).toFixed(2).toString();
        get_color(final_rate[name][i], el)
    }
}

function get_color(num, el) {
    if (num < 2) {
        el.classList.add('bad')
    } else if (num >= 3) {
        el.classList.add('great')
    } else {
        el.classList.add('good')
    }
}

function get_rates_array(json) {
    let u = json[0]
    let name = document.getElementById("head");
    name.innerHTML += u.username;
    let count = 0;
    let final_rate = {
        'manager': {
            'time': 0.0,
            'target': 0.0,
            'teamwork': 0.0,
            'practices': 0.0,
            'technologies': 0.0,
            'adaptive': 0.0,
            'average': 0.0
        },
        'peers': {
            'time': 0.0,
            'target': 0.0,
            'teamwork': 0.0,
            'practices': 0.0,
            'technologies': 0.0,
            'adaptive': 0.0,
            'average': 0.0
        },
        'averages': {
            'time': 0.0,
            'target': 0.0,
            'teamwork': 0.0,
            'practices': 0.0,
            'technologies': 0.0,
            'adaptive': 0.0,
            'average': 0.0
        }
    }

    for (let r of u.rates) {
        if ((r['is_manager'])) {
            let average = 0.0;
            final_rate['manager']['time'] = Number(r['r_deadline']);
            average += Number(r['r_deadline']);
            final_rate['manager']['target'] = r['r_approaches'];
            average += r['r_approaches'];
            final_rate['manager']['teamwork'] = r['r_teamwork'];
            average += r['r_teamwork'];
            final_rate['manager']['practices'] = r['r_practices'];
            average += r['r_practices'];
            final_rate['manager']['technologies'] = r['r_experience'];
            average += r['r_experience'];
            final_rate['manager']['adaptive'] = r['r_adaptation'];
            average += r['r_adaptation'];
            final_rate['manager']['average'] = (average / 6).toFixed(2);
        } else {
            count++;
            final_rate['peers']['time'] += Number(r['r_deadline']);
            final_rate['peers']['target'] += r['r_approaches'];
            final_rate['peers']['teamwork'] += r['r_teamwork'];
            final_rate['peers']['practices'] += r['r_practices'];
            final_rate['peers']['technologies'] += r['r_experience'];
            final_rate['peers']['adaptive'] += r['r_adaptation'];
        }
    }
    let average = 0.0;
    for (let r in final_rate["peers"]) {
        final_rate["peers"][r] /= count;
        final_rate["peers"][r] = final_rate["peers"][r]
        average += final_rate["peers"][r];
    }
    final_rate["peers"]['average'] = (average / 6).toFixed(2);


    final_rate['averages']['time'] = (final_rate['peers']['time'] + final_rate['manager']['time']) / 2
    final_rate['averages']['target'] = (final_rate['peers']['target'] + final_rate['manager']['target']) / 2
    final_rate['averages']['teamwork'] = (final_rate['peers']['teamwork'] + final_rate['manager']['teamwork']) / 2
    final_rate['averages']['practices'] = (final_rate['peers']['practices'] + final_rate['manager']['practices']) / 2
    final_rate['averages']['technologies'] = (final_rate['peers']['technologies'] + final_rate['manager']['technologies']) / 2
    final_rate['averages']['adaptive'] = (final_rate['peers']['adaptive'] + final_rate['manager']['adaptive']) / 2
    final_rate['averages']['average'] = (Number(final_rate['peers']['average']) + Number(final_rate['manager']['average'])) / 2
    return final_rate;
}

function get_rates(id) {
    return fetch(window.location.origin + "/perforator/imanager/employee/rating?id=" + id);
}

function get_team() {
    return fetch(window.location.origin + "/perforator/team");
}

function get_self_review(id) {
    return fetch(window.location.origin + "/perforator/self-review/id?id=" + id);
}

function myFunction() {
    document.getElementById('myDropdown').classList.toggle('show')
}

function toggle_sr() {
    document.getElementById('sr').classList.toggle('show')
}