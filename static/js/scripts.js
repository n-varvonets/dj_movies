

// Add star rating
const rating = document.querySelector('form[name=rating]');  // в нашем document с помощью querySelector я ищу форму по имени rating

rating.addEventListener("change", function (e) { // когда у этой формы вызовится событие change, то
    // Получаем данные из формы
    let data = new FormData(this);  //создавая FormData и передав нашу форму мы получим все значения наших полей
    fetch(`${this.action}`, {  // с помощью fetch на урл нашей формы мы будем отправлять post запрос
        method: 'POST',
        body: data  // и  и передавая в тело нашу инфу
    })
        .then(response => alert("Rating set")) // при успехе будет выводиться надпись - Рейтинг установлен
        .catch(error => alert("Error")) // а при неудаче - Ошибка
});