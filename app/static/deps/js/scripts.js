

// Когда HTML-документ готов
$(document).ready(function () {
    // берем в переменную элемент разметки с id jq-notification для оповещений от ajax
    var successMessage = $("#jq-notification");


    // =========================================



    // Открыть модальное окно выбора подборки пользователя для добавления
    $('#modalButton').click(function () {
        $('#exampleModal').appendTo('body');

        $('#exampleModal').modal('show');
    });

    // Собыите клик по кнопке закрыть окна корзины
    $('#exampleModal .btn-close').click(function () {
        $('#exampleModal').modal('hide');
    });



    // =========================================



    // Сделать кликабельным строчку таблицы с классом '.clickable-row', кроме иконок удаления и добавления в коллекцию
    document.querySelectorAll('.clickable-row').forEach(row => {
        row.addEventListener('click', function (event) {
            // Проверяем, не был ли клик по элементу с классом 'delete-icon' или 'add-to-user-collection'
            if (!event.target.closest('.delete-icon') && !event.target.closest('.add-to-user-collection')) {
                window.location.href = this.getAttribute('data-href');
            }
        });
    });



    // ==========================================================================


    // Добавление категорий пользователя

    // Обработчик клика на кнопку создания категории
    $('#create-category-btn').on('click', function (e) {
        e.preventDefault();  // Предотвращаем стандартное поведение формы

        // Получаем значение категории из поля ввода
        const categoryName = $('#category-name').val().trim();

        if (categoryName === '') {
            alert('Введите название категории');
            return;
        }

        // Отправляем AJAX-запрос на создание новой категории
        $.ajax({
            url: $('#category-form').attr('action'),  // Получаем URL из атрибута формы
            method: 'POST',
            data: {
                category_name: categoryName,
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()  // Передаем CSRF токен
            },
            success: function (response) {
                // Очищаем поле ввода
                $('#category-name').val('');

                // Сообщение
                successMessage.html(response.message);
                successMessage.fadeIn(400);
                // Через 7сек убираем сообщение
                setTimeout(function () {
                    successMessage.fadeOut(400);
                }, 7000);

                // Меняем содержимое категорий на ответ от Django (новый отрисованный HTML)
                var tileContainer = $("#include-list-categories-place");
                tileContainer.html(response.collections);  // Обновляем контейнер с категориями

            },
            error: function (xhr, status, error) {
                console.error('Ошибка при создании категории:', error);
            }
        });
    });

    // ==========================================================================


    // Удаление категории пользователя

    // Обработчик клика на значок корзины
    $(document).on('click', '.cart-icon', function (e) {
        e.preventDefault(); // Предотвращаем стандартное действие

        // Получаем данные из атрибутов значка корзины
        var categoryName = $(this).data('category');
        var actionUrl = $(this).attr("href");

        // Отправляем AJAX POST запрос
        $.ajax({
            url: actionUrl,
            method: 'POST',
            data: {
                category_name: categoryName,
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val() // Передаем CSRF токен
            },
            success: function (response) {
                // Сообщение
                successMessage.html(response.message);
                successMessage.fadeIn(400);
                // Через 7сек убираем сообщение
                setTimeout(function () {
                    successMessage.fadeOut(400);
                }, 7000);

                // Меняем содержимое категорий на ответ от Django (новый отрисованный HTML)
                var tileContainer = $("#include-list-categories-place");
                tileContainer.html(response.collections);  // Обновляем контейнер с категориями
            },
            error: function (xhr, status, error) {
                // Обрабатываем ошибку
                console.error('Ошибка при удалении категории:', error);
            }
        });
    });


    // ==========================================================================
    // Удаление токена из подборки

    $(document).on('click', '.delete-icon', function (e) {
        e.preventDefault();

        var poolAddress = $(this).data('pool-address');
        var collectionName = $(this).data('category');
        var actionUrl = $(this).data('action');

        $.ajax({
            type: 'POST',
            url: actionUrl,
            data: {
                pool_address: poolAddress,
                collection_name: collectionName,
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function (response) {
                // Сообщение
                successMessage.html(response.message);
                successMessage.fadeIn(400);
                // Через 7сек убираем сообщение
                setTimeout(function () {
                    successMessage.fadeOut(400);
                }, 7000);

                // location.reload(); // Обновляем страницу после удаления

                // Удаление строки с нужным data-href
                var poolUrl = response.pool_url;
                $('tr[data-href="' + poolUrl + '"]').remove();
            },
            error: function (xhr, status, error) {
                console.error('Ошибка при удалении пула:', error);
            }
        });
    });


    // ==========================================================================


    // Добавление токена в подборку
    // Ловим собыитие клика по кнопке добавить в корзину
    $(document).on("click", ".add-to-user-collection", function (e) {
        // Блокируем его базовое действие
        e.preventDefault();

        // Получаем address пула из атрибута data-addres
        var address = $(this).data("address");
        // Получаем название категории пула из атрибута data-category
        var collection_name = $(this).data("collection");

        // Из атрибута href берем ссылку на контроллер django
        var add_to_collection_url = $(this).attr("href");

        // делаем post запрос через ajax не перезагружая страницу
        $.ajax({
            type: "POST",
            url: add_to_collection_url,
            data: {
                pool_address: address,
                collection_name: collection_name,
                csrfmiddlewaretoken: $("[name=csrfmiddlewaretoken]").val(),
            },
            success: function (data) {
                // Сообщение
                successMessage.html(data.message);
                successMessage.fadeIn(400);
                // Через 7сек убираем сообщение
                setTimeout(function () {
                    successMessage.fadeOut(400);
                }, 7000);
            },

            error: function (data) {
                console.log("Ошибка при добавлении товара в корзину");
            },
        });
    });



    // =========================================


    // Берем из разметки элемент по id - оповещения от django
    var notification = $('#notification');
    // И через 7 сек. убираем
    if (notification.length > 0) {
        setTimeout(function () {
            notification.alert('close');
        }, 7000);
    }


    // ==========================================

    // Открытие и закрытие модального окна результатов поиска

    function openModal() {
        var myModal = new bootstrap.Modal(document.getElementById('searchModal'));
        myModal.show();
    }
    

    function closeModal() {
        document.getElementById('searchModal').style.display = 'none';
    }



    // ==========================================



    // Поиск

    document.getElementById('searchForm').addEventListener('submit', function (e) {
        e.preventDefault();  // Предотвращаем стандартное поведение отправки формы

        let query = this.q.value;  // Получаем значение поля ввода

        if (query === '') {
            // Сообщение
            successMessage.html("Запрос не может быть пустым");
            successMessage.fadeIn(400);
            // Через 7сек убираем сообщение
            setTimeout(function () {
                successMessage.fadeOut(400);
            }, 7000);
            return;
        }

        // Обновляем URL
        history.pushState(null, '', `?q=${encodeURIComponent(query)}`);

        // Здесь выполняем AJAX-запрос с поисковым запросом
        console.log("Поисковый запрос:", query);

        // Отправляем AJAX-запрос на создание новой категории
        $.ajax({
            url: $('#searchForm').attr('action'),  // Получаем URL из атрибута формы
            method: 'GET',
            data: {
                q: query,
            },
            success: function (response) {
                // Очищаем поле ввода
                $('#category-name').val('');

                // Сообщение
                successMessage.html(response.message);
                successMessage.fadeIn(400);
                // Через 7сек убираем сообщение
                setTimeout(function () {
                    successMessage.fadeOut(400);
                }, 7000);

                // Меняем содержимое категорий на ответ от Django (новый отрисованный HTML)
                var tileContainer = $("#searchResults");
                tileContainer.html(response.q_results);  // Обновляем контейнер с категориями
                openModal();  // Открываем модальное окно
            },
            error: function (xhr, status, error) {
                console.error('Ошибка при создании категории:', error);
            }
        });
    });



    window.addEventListener('popstate', function (event) {
        // Получение значения query из URL
        const query = new URLSearchParams(window.location.search).get('q');
        
        if (query) {
            // Отправляем запрос для получения данных при возврате к предыдущему состоянию
            $.ajax({
                url: $('#searchForm').attr('action'),
                method: 'GET',
                data: {
                    q: query,
                },
                success: function (response) {
                    var tileContainer = $("#searchResults");
                    tileContainer.html(response.q_results);  // Обновляем контейнер с категориями
                    openModal();  // Открываем модальное окно
                },
                error: function (xhr, status, error) {
                    console.error('Ошибка при создании категории:', error);
                }
            });
        }
    });
    

});
