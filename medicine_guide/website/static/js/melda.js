document.getElementById("bmi-form").addEventListener("submit", function (event) {
    event.preventDefault(); // Отменить отправку формы

    var form = event.target;
    var formData = new FormData(form);

    var xhr = new XMLHttpRequest();
    xhr.open(form.method, form.action, true);
    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var resultContainer = document.getElementById("resulte");
            resultContainer.innerHTML = "MELD: " + xhr.responseText;
        }
    };
    xhr.send(formData);
});