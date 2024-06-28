var checkboxes = document.querySelectorAll('input[name="symptoms"]');
checkboxes.forEach(function(checkbox) {
  checkbox.addEventListener('change', function() {
    var symptomText = this.parentNode.querySelector('#symptomText');
    symptomText.style.color = this.checked ? 'red' : 'black'; // изменяем цвет текста при выборе элемента
  });
});

document.addEventListener('keydown', function(event) {
    if (event.key === "Enter" && event.target.nodeName !== "BUTTON") {
      event.preventDefault(); // предотвращаем отправку формы
      document.getElementById("searchForm").submit();
    }
  });