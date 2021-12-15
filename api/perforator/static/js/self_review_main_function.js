let btn_status = [false, false]

function self_review_main() {
    get_self_review()
        .then(response => response.json())
        .then(json => {
            let selfReview = document.getElementById("self-review");
            let flag = '';
            let el_id = 0;
            let is_draft = json['is_draft']
            for (let grade of json['grades']) {
                const allDiv = document.createElement("div");
                allDiv.setAttribute("id", `id${grade.id}`)
                allDiv.setAttribute("class", `introduction`)

                if (flag != grade.grade_category_name) {
                    allDiv.innerHTML =
                        `
                        <h4 id="theme${grade.id}">${grade.grade_category_name}</h4>
                        <p class="description">${grade.grade_category_preview_description}</p>
                    `
                    if (grade.grade_category_description != null) {
                        if (!is_draft) {
                            allDiv.innerHTML += `
                                <p class="question">${grade.grade_category_description}</p>
                                <input type="text" class="input-text" category_id="${grade.grade_category_id}" field="yes" value="${grade.comment}" disabled>
                            `;
                        } else {
                            allDiv.innerHTML += `
                                <p class="question">${grade.grade_category_description}</p>          
                                <input type="text" class="input-text" category_id="${grade.grade_category_id}" field="yes" value="${grade.comment}">
                            `;
                        }
                    } else {
                        if (!is_draft) {
                            allDiv.innerHTML += `
                                <textarea name="plans" id="plan" rows="5" field='yes' class="ta" category_id="${grade.grade_category_id}" disabled>${grade.comment}</textarea>
                            `;
                        } else {
                            allDiv.innerHTML += `
                                <textarea name="plans" id="plan" rows="5" field='yes' class="ta" category_id="${grade.grade_category_id}">${grade.comment}</textarea>
                            `;
                        }
                    }
                    flag = grade.grade_category_name;
                    el_id = grade.id;
                    selfReview.appendChild(allDiv);

                } else {
                    let container = document.getElementById(`id${el_id}`)
                    let p = document.createElement("p");
                    p.setAttribute("class", "question")
                    p.innerHTML = `${grade.grade_category_description}`;

                    let input = document.createElement("input");
                    input.setAttribute("class", "input-text");
                    input.setAttribute("type", "text");
                    input.setAttribute("category_id", `${grade.grade_category_id}`);
                    input.setAttribute("field", "yes");
                    if (!is_draft) {
                        input.setAttribute("disabled", "disabled");
                    }
                    input.setAttribute("value", `${grade.comment}`);

                    container.appendChild(p);
                    container.appendChild(input);
                }
            }
            if (!is_draft) {
                //disable_btn_peers();
                replace_send_btn();
            }
        })

}

function get_self_review() {
    return fetch(window.location.origin + "/perforator/self-review/");
}

function disable_btn_send() {
    let btn = document.querySelector(".send")
    try {
        btn.setAttribute("disabled", "disabled")
        btn.setAttribute("style", "background-color: #8e8e8e")
    }
    catch (error){

    }
}

function enable_btn_send() {
    let btn = document.querySelector(".send")
    try {
        btn.removeAttribute("disabled")
        btn.setAttribute("style", "background-color: #A5A4F5")
    }
    catch (error){

    }
}

function disable_btn_peers(){
    document.querySelector(".add-peer").remove()
    let btn_close = document.querySelectorAll("[id='close']");
    for (let b of btn_close) b.style.display = "none";
    //btn.setAttribute("disabled", "disabled")
    //btn.setAttribute("style", "background-color: #8e8e8e")
}
function replace_send_btn(){
    let galochka = document.createElement("img")
    let container_galochka = document.createElement("p")
    let text = document.createElement("h4");
    text.innerHTML = "Форма отправлена!";
    let container = document.querySelector(".wrapper-submit")
    galochka.setAttribute("src", "/static/img/check.svg")
    container_galochka.setAttribute("class", "check_img")

    //document.querySelector(".send").style.display = "none";
    //document.querySelector(".save").style.display = "none";
    document.querySelector(".send").remove();
    document.querySelector(".save").remove();
    document.getElementById("draft").remove();
    container_galochka.appendChild(galochka)
    container.appendChild(container_galochka)
    container.appendChild(text)
}

function check_free_fields() {
    let inputs = document.querySelectorAll("[field='yes']");
    for (let i of inputs) {
        if (i.value == "") {
            btn_status[0] = false;
            update_btn();
            return
        }
    }
    btn_status[0] = true;
    update_btn();
}

function check_peers_list() {
    let peers = document.getElementById("my_peers").children
    for (let p of peers){
        if (p.style.display != "none"){
            btn_status[1] = true;
            update_btn();
            return;
        }
    }
    btn_status[1] = false;
    update_btn();
}

function check_free_fields_onload() {
    let inputs = document.querySelectorAll("[field='yes']");
    for (let i of inputs) {
        i.addEventListener('blur', (event) => {
            check_peers_list();
            check_free_fields();
        })
    }
    check_free_fields();
    check_peers_list();
}

function update_btn() {
    btn_status[0] === true && btn_status[1] === true ? enable_btn_send() : disable_btn_send();
}

function save_self_review(is_draft) {
    check_peers_list();
    check_free_fields();
    if (btn_status[0] !== true && btn_status[1] !== true) return
    if (!is_draft) {
        disable_btn_send();
        disable_btn_peers();
        replace_send_btn()
    }
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    data = {'is_draft': is_draft, 'grades': []}
    let selfReviewGrades = document.querySelectorAll("[field='yes']");

    for (let gradeDiv of selfReviewGrades) {
        data['grades'].push({
            'grade_category_id': gradeDiv.getAttribute('category_id'),
            'comment': gradeDiv.value,
        })
        if (!is_draft) {
            gradeDiv.setAttribute("disabled", "disabled");
        }
    }
    fetch(window.location.origin + "/perforator/self-review/save/", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify(data)
    })
    let elem = document.querySelector("#draft")
    console.log(elem.classList);
    console.log(elem.classList.contains("active_draft"));
    if (elem.classList.contains("active_draft")) {
        $('#draft').removeClass('active_draft');
        $('#draft').addClass('hidden_draft');
        setTimeout(show_draft, 300);
    } else {
        $('#draft').addClass('active_draft');
    }
}

function show_draft() {
    $('#draft').removeClass('hidden_draft');
    $('#draft').addClass('active_draft');
    //document.getElementById('draft').setAttribute("style", "opacity:0; transition: opacity 1s ease-in-out;");
}

function disable_form() {
    let is_draft = false
    fetch(window.location.origin + "/perforator/self-review/is-draft/")
        .then(response => response.json())
        .then(json => {
            is_draft = json["is_draft"];
        })
    let selfReviewGrades = document.querySelectorAll("[field='yes']");
    //console.log(is_draft);
    //console.log(selfReviewGrades)
    for (let gradeDiv of selfReviewGrades) {

        if (!is_draft) {
            gradeDiv.setAttribute("disabled", "disabled");
            document.querySelector(".save").setAttribute("disabled", "disabled");
            document.querySelector(".send").setAttribute("disabled", "disabled");
        }
    }
}
