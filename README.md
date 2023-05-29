# search-engine-parser-bot

Телеграм-бот для поиска номера элемента на странице товаров на Wildberries.
Протестировать его можно по ссылке https://t.me/parse_wb_bot

Его задача: вернуть номер страницы и номер элемента на странице данного товара.
В команду /parse "товар" "артикул" передаются аргументы по которым происходит парсинг.

Проблемы при разработке
1) Спарсить количество товара и найти доступное количество страниц не составило труда. Но, на этом маркетплейсе принудительно ограничено количство страниц (60).
2) Вывод при не корректном артикуле или товаре ограничен специально, в дальнейшем будет фикс (с помощью FCM).

Бот асинхронный. При синхронном подходе разница во времени парсинга была в 6 раз медленнее.

------

Telegram bot to find the item number on the product page on Wildberries.
You can test it at the link https://t.me/parse_wb_bot

Its task is to return the page number and the number of the item on the page of the given product.
In the command /parse "item" "article" passed arguments on which is parsing.

Problems in development
1) It wasn't difficult to parse the number of items and find the available number of pages. But, on this marketplace is forcibly limited to the number of pages (60).
2) The output when the wrong article or product is limited on purpose, in the future will be fiks (with FCM).

Bot asynchronous. With synchronous approach parsing time difference was 6 times slower.
