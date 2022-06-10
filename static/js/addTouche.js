const toucheForm = document.querySelector("#toucheForm");


toucheForm.addEventListener("submit", (e) => {
    e.preventDefault();

    const formData = new FormData(e.target);

    const data = fromFormDataToObject(formData);

    fetch(toucheFormUrl, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => console.log(data))
});

const fromFormDataToObject = (formData) => {
    var object = {};
    formData.forEach((value, key) => object[key] = value);
    return object;
}