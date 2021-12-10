
function self_review_main() {
    get_self_review()
        .then(response => response.json())
        .then(json => {
            let selfReview = document.getElementById("self-review");
            let flag = '';
            let el_id = 0;
            let is_draft = json['is_draft']
            //console.log(json['grades'])
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
                        if (!is_draft){
                            allDiv.innerHTML += `
                                <p class="question">${grade.grade_category_description}</p>
                                <input type="text" class="input-text" category_id="${grade.grade_category_id}" field="yes" value="${grade.comment}" disabled>
                            `;
                        }
                        else {
                            allDiv.innerHTML += `
                                <p class="question">${grade.grade_category_description}</p>          
                                <input type="text" class="input-text" category_id="${grade.grade_category_id}" field="yes" value="${grade.comment}">
                            `;
                        }
                    }
                    else {
                        if (!is_draft){
                            allDiv.innerHTML += `
                                <textarea name="plans" id="plan" rows="5" field='yes' class="ta" category_id="${grade.grade_category_id}" disabled>${grade.comment}</textarea>
                            `;
                        }
                        else {
                            allDiv.innerHTML += `
                                <textarea name="plans" id="plan" rows="5" field='yes' class="ta" category_id="${grade.grade_category_id}">${grade.comment}</textarea>
                            `;
                        }
                    }
                    flag = grade.grade_category_name;
                    el_id = grade.id;
                    selfReview.appendChild(allDiv);

                }
                else{
                    let container = document.getElementById(`id${el_id}`)
                    let p = document.createElement("p");
                    p.setAttribute("class", "question")
                    p.innerHTML = `${grade.grade_category_description}`;

                    let input = document.createElement("input");
                    input.setAttribute("class", "input-text");
                    input.setAttribute("type", "text");
                    input.setAttribute("category_id", `${grade.grade_category_id}`);
                    input.setAttribute("field", "yes");
                    if (!is_draft){
                        input.setAttribute("disabled", "disabled");
                    }
                    input.setAttribute("value", `${grade.comment}`);

                    container.appendChild(p);
                    container.appendChild(input);
                }
            }
            if (!is_draft){
                document.querySelector(".save").setAttribute("disabled", "disabled");
                document.querySelector(".send").setAttribute("disabled", "disabled");
            }

        })

}

function get_self_review() {
    return fetch(window.location.origin + "/perforator/self-review/");
}

function save_self_review(is_draft) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    data = {'is_draft': is_draft, 'grades': []}
    let selfReviewGrades = document.querySelectorAll("[field='yes']");

    for (let gradeDiv of selfReviewGrades) {
        data['grades'].push({
            'grade_category_id': gradeDiv.getAttribute('category_id'),
            'comment': gradeDiv.value,
        })
        if (!is_draft){
            gradeDiv.setAttribute("disabled", "disabled");
            document.querySelector(".save").setAttribute("disabled", "disabled");
            document.querySelector(".send").setAttribute("disabled", "disabled");
        }
    }
    //console.log(data)
    fetch(window.location.origin + "/perforator/self-review/save/", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json;charset=utf-8',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify(data)
    })
}


function disable_form(){
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

        if (!is_draft){
            gradeDiv.setAttribute("disabled", "disabled");
            document.querySelector(".save").setAttribute("disabled", "disabled");
            document.querySelector(".send").setAttribute("disabled", "disabled");
        }
    }
}