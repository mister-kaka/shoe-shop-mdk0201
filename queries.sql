-- 1. Товары дороже 10 000 руб.
SELECT id, name, price
FROM Products
WHERE price > 10000
ORDER BY price DESC;

-- 2. Товары категории "Женская обувь"
SELECT p.id, p.name, p.price
FROM Products p
JOIN Categories c ON c.id = p.category_id
WHERE c.name = 'Женская обувь'
ORDER BY p.id;

-- 3. Количество моделей у каждого производителя
SELECT m.name AS manufacturer, COUNT(*) AS models
FROM Manufacturers m
JOIN Products p ON p.manufacturer_id = m.id
GROUP BY m.id
ORDER BY models DESC, m.name;

-- 4. Средняя цена по категориям
SELECT c.name AS category, ROUND(AVG(p.price), 2) AS avg_price
FROM Categories c
JOIN Products p ON p.category_id = c.id
GROUP BY c.id;

-- 5. Товары, которых на складе меньше 3 (суммарно по всем размерам)
SELECT p.id, p.name, SUM(s.quantity) AS total
FROM Products p
JOIN Stock s ON s.product_id = p.id
GROUP BY p.id
HAVING SUM(s.quantity) < 3;

-- 6. Товары без заказов за прошлый месяц (скидка 25%)
-- "сегодня" берём 2026-05-20: в файле заказы за апрель и май 2026, прошлый месяц - апрель
SELECT p.id, p.name, p.price, ROUND(p.price * 0.75, 2) AS price_final
FROM Products p
WHERE p.id NOT IN (
    SELECT s.product_id
    FROM OrderItems oi
    JOIN Stock s ON s.id = oi.stock_id
    JOIN Orders o ON o.id = oi.order_id
    WHERE strftime('%Y-%m', o.order_date) = strftime('%Y-%m', '2026-05-20', '-1 month')
)
ORDER BY p.id;

-- 7. Топ-5 самых дорогих заказов с ФИО клиента
SELECT o.id, o.order_date, u.last_name || ' ' || u.first_name || ' ' || COALESCE(u.middle_name, '') AS fio,
       SUM(oi.quantity * oi.unit_price) AS total
FROM Orders o
JOIN Users u ON u.id = o.user_id
JOIN OrderItems oi ON oi.order_id = o.id
GROUP BY o.id
ORDER BY total DESC
LIMIT 5;

-- 8. Размеры, которые есть на складе, но ни разу не заказывались
SELECT DISTINCT z.value AS size
FROM Stock s
JOIN Sizes z ON z.id = s.size_id
WHERE s.quantity > 0
  AND s.size_id NOT IN (
    SELECT st.size_id
    FROM OrderItems oi
    JOIN Stock st ON st.id = oi.stock_id
  )
ORDER BY CAST(z.value AS REAL);
