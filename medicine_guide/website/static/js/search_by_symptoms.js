 // Получить все чекбоксы симптомов
 var checkboxes = document.querySelectorAll('input[type="checkbox"][name="symptoms"]');

 // При изменении состояния чекбоксов
 checkboxes.forEach(function(checkbox) {
   checkbox.addEventListener('change', function() {
     if (this.checked) {
       // Изменить цвет текста выбранного симптома
       this.nextElementSibling.style.color = "#0d6efe"; // Здесь можно указать нужный цвет
     } else {
       // Вернуть цвет текста не выбранного симптома
       this.nextElementSibling.style.color = '';
     }
   });
 });

 // При нажатии на Enter
 document.addEventListener('keydown', function(event) {
   if (event.key === 'Enter') {
   
     document.querySelector('button[type="submit"]').click(); // Кликнуть на скрытую кнопку отправки
   }
 });
// // document.addEventListener('keydown', function(event) {
//     if (event.key === "Enter" && event.target.nodeName !== "BUTTON") {
//       event.preventDefault(); // предотвращаем отправку формы
//       document.getElementById("searchForm").submit();
//     }
//   });