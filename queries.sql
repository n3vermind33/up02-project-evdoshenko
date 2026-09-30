SELECT цена FROM Товар ORDER BY цена DESC LIMIT 1;

SELECT цена FROM Товар ORDER BY цена LIMIT 1;

SELECT страна, длительность, цена FROM Товар WHERE длительность = 7;

SELECT страна FROM Товар WHERE страна LIKE '%а%';

SELECT * FROM Заказ;

SELECT * FROM Заказ WHERE клиент = "Иванов Иван Иванович";

SELECT Заказ.дата, Заказ.клиент, Товар.страна, Заказ.количество
FROM Заказ
JOIN Товар ON Заказ.товар_id = Товар.id;



-- SELECT SUM(Товар.цена * Заказ.количество)
FROM Заказ
JOIN Товар ON Заказ.товар_id = Товар.id;


SELECT клиент, количество FROM Заказ GROUP BY клиент;

--Что я хочу получить: логин, фио, роль каждого пользователя

SELECT фио, логин, роль FROM Пользователь;