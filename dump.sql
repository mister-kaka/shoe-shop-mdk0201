BEGIN TRANSACTION;
CREATE TABLE Categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);
INSERT INTO "Categories" VALUES(1,'Детская обувь');
INSERT INTO "Categories" VALUES(10,'Женская обувь');
INSERT INTO "Categories" VALUES(23,'Мужская обувь');
CREATE TABLE Manufacturers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);
INSERT INTO "Manufacturers" VALUES(1,'Малыш-Спорт');
INSERT INTO "Manufacturers" VALUES(2,'Топ-Топ');
INSERT INTO "Manufacturers" VALUES(3,'Лапушка');
INSERT INTO "Manufacturers" VALUES(4,'Тёплые ножки');
INSERT INTO "Manufacturers" VALUES(5,'Северята');
INSERT INTO "Manufacturers" VALUES(6,'Весна');
INSERT INTO "Manufacturers" VALUES(7,'Здоровый шаг');
INSERT INTO "Manufacturers" VALUES(8,'Карапуз');
INSERT INTO "Manufacturers" VALUES(9,'Маленький франт');
INSERT INTO "Manufacturers" VALUES(10,'Барбари');
INSERT INTO "Manufacturers" VALUES(12,'Твой комфорт');
INSERT INTO "Manufacturers" VALUES(13,'Стиль и комфорт');
INSERT INTO "Manufacturers" VALUES(14,'Кожевенные традиции');
INSERT INTO "Manufacturers" VALUES(15,'Модный силуэт');
INSERT INTO "Manufacturers" VALUES(23,'Азимут');
INSERT INTO "Manufacturers" VALUES(27,'Берестов');
CREATE TABLE OrderItems (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL REFERENCES Orders (id) ON DELETE CASCADE,
    stock_id INTEGER NOT NULL REFERENCES Stock (id),
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    unit_price REAL NOT NULL CHECK (unit_price >= 0)
);
INSERT INTO "OrderItems" VALUES(1,1,1,1,2190.0);
INSERT INTO "OrderItems" VALUES(2,1,20,1,2790.0);
INSERT INTO "OrderItems" VALUES(3,2,30,1,25000.0);
INSERT INTO "OrderItems" VALUES(4,2,39,1,7500.0);
INSERT INTO "OrderItems" VALUES(5,3,34,1,17000.0);
INSERT INTO "OrderItems" VALUES(6,3,57,1,8565.0);
INSERT INTO "OrderItems" VALUES(7,3,65,1,7795.0);
INSERT INTO "OrderItems" VALUES(8,4,50,1,7757.0);
INSERT INTO "OrderItems" VALUES(9,4,48,1,12340.0);
INSERT INTO "OrderItems" VALUES(10,4,44,1,7130.0);
INSERT INTO "OrderItems" VALUES(11,4,62,1,8765.0);
INSERT INTO "OrderItems" VALUES(12,4,32,1,15000.0);
INSERT INTO "OrderItems" VALUES(13,5,77,1,9567.0);
INSERT INTO "OrderItems" VALUES(14,5,87,1,21500.0);
INSERT INTO "OrderItems" VALUES(15,5,73,1,7890.0);
INSERT INTO "OrderItems" VALUES(16,6,80,1,24569.0);
INSERT INTO "OrderItems" VALUES(17,6,89,1,14567.0);
INSERT INTO "OrderItems" VALUES(18,6,91,1,15670.0);
INSERT INTO "OrderItems" VALUES(19,7,16,1,4290.0);
INSERT INTO "OrderItems" VALUES(20,7,2,2,2190.0);
INSERT INTO "OrderItems" VALUES(21,7,24,1,1690.0);
INSERT INTO "OrderItems" VALUES(22,8,86,1,25625.0);
INSERT INTO "OrderItems" VALUES(23,8,75,3,7890.0);
INSERT INTO "OrderItems" VALUES(24,8,70,2,6550.0);
INSERT INTO "OrderItems" VALUES(25,9,7,1,2490.0);
INSERT INTO "OrderItems" VALUES(26,9,14,2,3190.0);
INSERT INTO "OrderItems" VALUES(27,10,53,1,7550.0);
INSERT INTO "OrderItems" VALUES(28,10,43,1,7130.0);
INSERT INTO "OrderItems" VALUES(29,10,46,1,12340.0);
INSERT INTO "OrderItems" VALUES(30,10,61,2,8765.0);
CREATE TABLE Orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_date TEXT NOT NULL,
    user_id INTEGER NOT NULL REFERENCES Users (id)
);
INSERT INTO "Orders" VALUES(1,'2026-04-02',3);
INSERT INTO "Orders" VALUES(2,'2026-04-05',17);
INSERT INTO "Orders" VALUES(3,'2026-04-08',7);
INSERT INTO "Orders" VALUES(4,'2026-04-12',15);
INSERT INTO "Orders" VALUES(5,'2026-04-18',12);
INSERT INTO "Orders" VALUES(6,'2026-04-22',9);
INSERT INTO "Orders" VALUES(7,'2026-04-25',14);
INSERT INTO "Orders" VALUES(8,'2026-04-28',20);
INSERT INTO "Orders" VALUES(9,'2026-05-05',5);
INSERT INTO "Orders" VALUES(10,'2026-05-08',17);
CREATE TABLE Products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER NOT NULL REFERENCES Categories (id),
    manufacturer_id INTEGER NOT NULL REFERENCES Manufacturers (id),
    name TEXT NOT NULL,
    subcategory TEXT,
    description TEXT,
    composition TEXT,
    price REAL NOT NULL CHECK (price >= 0),
    image TEXT,
    UNIQUE (name, manufacturer_id)
);
INSERT INTO "Products" VALUES(1,1,1,'Кроссовки детские «Звёздочка» экокожа','Кроссовки','Кроссовки детские «Звёздочка» экокожа. Производитель: ООО «Малыш-Спорт», г. Смоленск','Верх — экокожа (полиуретан на хлопковой основе), подкладка — хлопок 100%, подошва — ПВХ',2190.0,'IMG_KS_195217.png');
INSERT INTO "Products" VALUES(2,1,2,'Кроссовки детские «Гонщик» экокожа','Кроссовки','Кроссовки детские «Гонщик» экокожа. Производитель: Фабрика «Топ-Топ», г. Киров','Верх — экокожа (микрофибра), подкладка — текстиль сетчатый (полиэстер), подошва — термопластичная резина (ТЭП)',2490.0,'IMG_KS_195213.png');
INSERT INTO "Products" VALUES(3,1,3,'Кроссовки детские «Радуга» экокожа перфорированная','Кроссовки','Кроссовки детские «Радуга» экокожа перфорированная. Производитель: ИП Смирнова Л.В. (бренд «Лапушка»), г. Вологда','Верх — экокожа перфорированная, вставки — нейлон, стелька — ортопедическая с латексной подушкой, подошва — ЭВА',1990.0,'IMG_KS_195222.png');
INSERT INTO "Products" VALUES(4,1,4,'Сапожки детские «Снежинка» зимние на меху','Сапоги','Сапожки детские «Снежинка» зимние на меху. Производитель: ООО «Тёплые ножки», г. Новосибирск','Верх — экокожа морозостойкая, утеплитель — искусственный мех (акрил 70%, полиэстер 30%), подкладка — флис, подошва — термоэластопласт (ТЭП)',3490.0,'IMG_KB_185501.png');
INSERT INTO "Products" VALUES(5,1,5,'Сапожки детские «Медвежонок» демисезонные непромокаемые','Сапоги','Сапожки детские «Медвежонок» демисезонные непромокаемые. Производитель: Компания «Северята», г. Архангельск','Верх — плащёвая ткань с водоотталкивающей пропиткой (полиэстер 100%), отделка — экокожа, подкладка — микрофибра, мембрана — AirTex, подошва — резина',3190.0,'IMG_KB_164816.png');
INSERT INTO "Products" VALUES(6,1,6,'Сапожки детские «Принцесса» кожаные','Сапоги','Сапожки детские «Принцесса» кожаные. Производитель: Мастерская «Весна», г. Тула','Верх — натуральная кожа (КРС), подкладка — шерсть натуральная (70%), байка (30%), стелька — войлочная, подошва — полиуретан',4290.0,'IMG_KB_164811.png');
INSERT INTO "Products" VALUES(7,1,7,'Сандалии детские «Пчёлка» ортопедические летние','Босоножки','Сандалии детские «Пчёлка» ортопедические летние. Производитель: ООО «Здоровый шаг», г. Воронеж','Верх — нубук натуральный, подкладка — кожа растительного дубления, стелька — анатомическая с супинатором (латекс + пробка), подошва — каучук',2790.0,'IMG_KSd_195207.png');
INSERT INTO "Products" VALUES(8,1,8,'Сандалии детские «Морячок» текстильные с фиксатором','Босоножки','Сандалии детские «Морячок» текстильные с фиксатором. Производитель: ИП Кузнецов А.Д. (бренд «Карапуз»), г. Краснодар','Верх — джинсовая ткань (хлопок 100%), окантовка — искусственная кожа, подкладка — хлопок, подошва — ЭВА лёгкая',1690.0,'IMG_KSd_185508.png');
INSERT INTO "Products" VALUES(9,1,9,'Туфли детские «Бантик» лаковые праздничные','Туфли','Туфли детские «Бантик» лаковые праздничные. Производитель: Дом обуви «Маленький франт», г. Москва','Верх — искусственная лаковая кожа (ПВХ), носок усиленный — термопластичный полиуретан, подкладка — кожа искусственная дышащая, стелька — анатомическая с амортизацией, подошва — полиуретан',2390.0,'IMG_KSho_185512.png');
INSERT INTO "Products" VALUES(10,10,10,'Сапоги зимние натуральная кожа','Сапоги','Сапоги женские зимние, нескользящая, устойчивая подошва, натуральный мех. Производитель: Дом обуви «Барбари», г. Новороссийск','Верх — натуральная кожа, подкладка — евромех, натуральный мех, текстильный утеплитель, подошва — резина',25000.0,'IMG_WB_170905.png');
INSERT INTO "Products" VALUES(11,10,10,'Сапоги осенние натуральная кожа','Сапоги','Сапоги женские демисезонные из высококачественной натуральной кожи. Производитель: Дом обуви «Барбари», г. Новороссийск','Верх — натуральная кожа, подкладка — текстильный утеплитель, стелька — текстиль, подошва — ТПР',15000.0,'IMG_WB_170859.png');
INSERT INTO "Products" VALUES(12,10,12,'Сапоги трубы демисезонные замшевые','Сапоги','Сапоги женские демисезонные замшевые. Производитель: ОАО «Твой комфорт», г. Ярославль','Верх — натуральная замша, утепленные, тракторная подошва, стелька — байка, подошва — резина',17000.0,'IMG_WB_170906.png');
INSERT INTO "Products" VALUES(13,10,13,'Босоножки «Песчаный берег» коричневые','Босоножки','Коричневая кожаная модель с открытым носком, боковой пряжкой и закрытым каблуком. Производитель: ИП «Стиль и комфорт», г. Санкт-Петербург','Верх — 100% козья кожа, подкладка — 100% кожа; подошва: 100% кожа',7500.0,'IMG_WSd_174332.png');
INSERT INTO "Products" VALUES(14,10,14,'Женские босоножки «Черный кофе» со скульптурным каблуком','Босоножки','Открытый носок и ремешок со сборной пряжкой, низкий каблук и резиновая подошва гарантируют комфорт. Производитель: ЗАО «Кожевенные традиции», г. Вятка','Верх — кожа собственного производств, подкладка — кожа; подошва: резина',5600.0,'IMG_WSd_185156.png');
INSERT INTO "Products" VALUES(15,10,15,'Босоножки женские «Летний бриз»','Босоножки','Босоножки женские кожаные белые, регулируемый ремешок, закрытый каблук и кожаная подошва. Производитель: ООО «Модный силуэт», г. Кострома','Верх — натуральная кожа, подкладка — натуральная кожа, подошва — кожа',7130.0,'IMG_WSd_185551.png');
INSERT INTO "Products" VALUES(16,10,15,'Демисезонные туфли натуральная кожа','Туфли','Комфортные лаконичные лодочки, классический дизайна с современными акцентами. Производитель: ООО «Модный силуэт», г. Кострома','Верх — натуральная овечья кожа, подкладка и стелька — натуральная овечья кожа, подошва — резина',12340.0,'IMG_WSho_174409.png');
INSERT INTO "Products" VALUES(17,10,14,'Туфли женские натуральная кожа с металлическими вставками','Туфли','Стильные туфли для весеннего и летнего сезона. Производитель: ЗАО «Кожевенные традиции», г. Вятка','Верх — натуральная телячьей кожа, металлическая пряжка, подкладка и стелька— натуральная овечья кожа, подошва — резина',7757.0,'IMG_WSho_185202.png');
INSERT INTO "Products" VALUES(18,10,13,'Туфли классические лодочки натуральная кожа','Туфли','Модель из натуральной кожи, классический острый носок и изящная шпилька. Производитель: ИП «Стиль и комфорт», г. Санкт-Петербург','Верх — натуральная кожа, подкладка и стелька — натуральная кожа, подошва — тунит',7550.0,'IMG_WSho_185545.png');
INSERT INTO "Products" VALUES(19,10,2,'Кроссовки белые с оранжевым и красным','Кроссовки','Многослойный верх из кожи и текстиля. Производитель: Фабрика «Топ-Топ», г. Киров','Верх — 70% кожа, 30% текстиль, подкладка — текстиль, подошва — резина',9450.0,'IMG_WS_174110.png');
INSERT INTO "Products" VALUES(20,10,2,'Кроссовки летние кожаные','Кроссовки','Уверенность на каждом шагу. Материал обеспечивает долговечность и комфорт при носке. Производитель: Фабрика «Топ-Топ», г. Киров','Верх — 87% кожа, 11% текстиль, 2% синтетика; подкладка: 100% текстиль; подошва: резина, пластик',8565.0,'IMG_WS_185528.png');
INSERT INTO "Products" VALUES(21,10,13,'Кроссовки кожаные','Кроссовки','Кроссовки женские из натуральной кожи. Производитель: ИП «Стиль и комфорт», г. Санкт-Петербург','Верх — натуральная кожа, подкладка — кожа, подошва — полиуретан',8765.0,'IMG_WS_185535.png');
INSERT INTO "Products" VALUES(22,10,13,'Кроссовки «Стиль и комфорт»','Кроссовки','Кроссовки женские из натуральной кожи и синтетических материалов, сетчатые вставки. Производитель: ИП «Стиль и комфорт», г. Санкт-Петербург','Верх — 70% кожа, 20% полиамид, 10% полиуретан; подкладка — текстиль, подошва — ТПУ',7795.0,'IMG_WS_185538.png');
INSERT INTO "Products" VALUES(23,23,23,'Кроссовки для бега «Драйв»','Кроссовки','Сочетание стиля, комфорта и современных технологий. Производитель: Фабрика «Азимут», г. Санкт-Петербург','Верх —  сетка, подкладка — текстиль, подошва —  резина',6550.0,'IMG_MS_185531.png');
INSERT INTO "Products" VALUES(24,23,23,'Кроссовки «Азимут Бег»','Кроссовки','Универсальный выбор для повседневного использования. Производитель: Фабрика «Азимут», г. Санкт-Петербург','Верх — 6% кожа, 29% текстиль, 15% полимерные материалы; подкладка — 100% текстиль; подошва — полимерные материалы, резина',7890.0,'IMG_MS_185532.png');
INSERT INTO "Products" VALUES(25,23,2,'Кроссовки','Кроссовки','Кроссовки для мужчин, идеальное сочетание стиля и комфорта. Производитель: Фабрика «Топ-Топ», г. Киров','Верх — 56% кожа, 29% текстиль, 15% полимерные материалы; подкладка — 100% текстиль; подошва — полимерные материалы, резина',9567.0,'IMG_MS_185533.png');
INSERT INTO "Products" VALUES(26,23,10,'Черные туфли в классическом стиле — база для деловых образов','Туфли','Модель выполнена из натуральной кожи, на резиновой подошве. Производитель: Дом обуви «Барбари», г. Новороссийск','Верх — натуральная кожа, подкладка — текстиль, стелька — натуральная кожа, подошва — резина',24569.0,'IMG_MSho_190514.png');
INSERT INTO "Products" VALUES(27,23,27,'Туфли мужские светлые классика демисезонные','Туфли','Туфли на низком каблуке кожаные','Верх — натуральная кожа, подкладка — текстиль, стелька — натуральная кожа, подошва — ТЭП',10155.0,'IMG_MSho_190518.png');
INSERT INTO "Products" VALUES(28,23,27,'Туфли из натуральной кожи','Туфли','Модель выполнена из натуральной кожи, на резиновой подошве, поддеживает классический и деловой стиль образов. Производитель: Дом обуви «Берестов», г. Москва','Верх — натуральная кожа, подкладка — натуральная кожа, стелька — натуральная кожа, подошва — резина',25625.0,'IMG_MSho_191612.png');
INSERT INTO "Products" VALUES(29,23,10,'Ботинки мужские демисезонные','Ботинки','Ботинки из натуральной кожи темно-коричневого и черного цвета на шнурках. Производитель: Дом обуви «Берестов», г. Москва','Верх — натуральная кожа, подкладка — текстиль, подошва — искусственный материал',21500.0,'IMG_MB_174349.png');
INSERT INTO "Products" VALUES(30,23,14,'Ботинки черные из натуральной кожи','Ботинки','Ботинки представляют баланс традиций и современности. Выполнены из натуральной кожи насыщенного черного цвета. Производитель: ЗАО «Кожевенные традиции», г. Вятка','Верх — натуральная кожа, подкладка — ворсин, стелька — ворсин, подошва — тунит',14567.0,'IMG_MB_191200.png');
INSERT INTO "Products" VALUES(31,23,10,'Ботинки зимние классические','Ботинки','Выбор на каждый день — натуральная кожа, натуральный мех. Производитель: Дом обуви «Барбари», г. Новороссийск','Верх — натуральная кожа, подкладка — натуральный мех, стелька — натуральный мех, подошва — ТЭП',15670.0,'IMG_MB_191205.png');
CREATE TABLE Sizes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    value TEXT NOT NULL UNIQUE
);
INSERT INTO "Sizes" VALUES(1,'18');
INSERT INTO "Sizes" VALUES(2,'19');
INSERT INTO "Sizes" VALUES(3,'20');
INSERT INTO "Sizes" VALUES(4,'21');
INSERT INTO "Sizes" VALUES(5,'22');
INSERT INTO "Sizes" VALUES(6,'23');
INSERT INTO "Sizes" VALUES(7,'24');
INSERT INTO "Sizes" VALUES(8,'25');
INSERT INTO "Sizes" VALUES(9,'26');
INSERT INTO "Sizes" VALUES(10,'27');
INSERT INTO "Sizes" VALUES(11,'28');
INSERT INTO "Sizes" VALUES(12,'29');
INSERT INTO "Sizes" VALUES(13,'30');
INSERT INTO "Sizes" VALUES(14,'31');
INSERT INTO "Sizes" VALUES(15,'32');
INSERT INTO "Sizes" VALUES(16,'33');
INSERT INTO "Sizes" VALUES(17,'34');
INSERT INTO "Sizes" VALUES(18,'35');
INSERT INTO "Sizes" VALUES(19,'36');
INSERT INTO "Sizes" VALUES(20,'36.5');
INSERT INTO "Sizes" VALUES(21,'37');
INSERT INTO "Sizes" VALUES(22,'37.5');
INSERT INTO "Sizes" VALUES(23,'38');
INSERT INTO "Sizes" VALUES(24,'38.5');
INSERT INTO "Sizes" VALUES(25,'39');
INSERT INTO "Sizes" VALUES(26,'39.5');
INSERT INTO "Sizes" VALUES(27,'40');
INSERT INTO "Sizes" VALUES(28,'40.5');
INSERT INTO "Sizes" VALUES(29,'41');
INSERT INTO "Sizes" VALUES(30,'41.5');
INSERT INTO "Sizes" VALUES(31,'42');
INSERT INTO "Sizes" VALUES(32,'42.5');
INSERT INTO "Sizes" VALUES(33,'43');
INSERT INTO "Sizes" VALUES(34,'44');
INSERT INTO "Sizes" VALUES(35,'45');
CREATE TABLE Stock (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL REFERENCES Products (id) ON DELETE CASCADE,
    size_id INTEGER NOT NULL REFERENCES Sizes (id),
    quantity INTEGER NOT NULL DEFAULT 0 CHECK (quantity >= 0),
    UNIQUE (product_id, size_id)
);
INSERT INTO "Stock" VALUES(1,1,3,20);
INSERT INTO "Stock" VALUES(2,1,4,20);
INSERT INTO "Stock" VALUES(3,1,5,20);
INSERT INTO "Stock" VALUES(4,1,6,20);
INSERT INTO "Stock" VALUES(5,1,7,20);
INSERT INTO "Stock" VALUES(6,1,8,20);
INSERT INTO "Stock" VALUES(7,2,16,2);
INSERT INTO "Stock" VALUES(8,2,17,2);
INSERT INTO "Stock" VALUES(9,3,2,30);
INSERT INTO "Stock" VALUES(10,3,3,30);
INSERT INTO "Stock" VALUES(11,4,2,15);
INSERT INTO "Stock" VALUES(12,4,3,15);
INSERT INTO "Stock" VALUES(13,5,4,5);
INSERT INTO "Stock" VALUES(14,5,5,5);
INSERT INTO "Stock" VALUES(15,5,6,5);
INSERT INTO "Stock" VALUES(16,6,1,4);
INSERT INTO "Stock" VALUES(17,6,2,4);
INSERT INTO "Stock" VALUES(18,6,3,4);
INSERT INTO "Stock" VALUES(19,7,4,4);
INSERT INTO "Stock" VALUES(20,7,5,4);
INSERT INTO "Stock" VALUES(21,7,6,4);
INSERT INTO "Stock" VALUES(22,7,7,4);
INSERT INTO "Stock" VALUES(23,8,10,7);
INSERT INTO "Stock" VALUES(24,8,11,7);
INSERT INTO "Stock" VALUES(25,8,12,7);
INSERT INTO "Stock" VALUES(26,8,13,7);
INSERT INTO "Stock" VALUES(27,9,1,7);
INSERT INTO "Stock" VALUES(28,9,2,7);
INSERT INTO "Stock" VALUES(29,9,3,7);
INSERT INTO "Stock" VALUES(30,10,19,12);
INSERT INTO "Stock" VALUES(31,10,21,12);
INSERT INTO "Stock" VALUES(32,11,25,2);
INSERT INTO "Stock" VALUES(33,11,27,2);
INSERT INTO "Stock" VALUES(34,12,21,5);
INSERT INTO "Stock" VALUES(35,12,25,5);
INSERT INTO "Stock" VALUES(36,12,27,5);
INSERT INTO "Stock" VALUES(37,13,19,10);
INSERT INTO "Stock" VALUES(38,13,21,10);
INSERT INTO "Stock" VALUES(39,13,23,10);
INSERT INTO "Stock" VALUES(40,13,25,10);
INSERT INTO "Stock" VALUES(41,13,27,10);
INSERT INTO "Stock" VALUES(42,14,18,3);
INSERT INTO "Stock" VALUES(43,15,21,23);
INSERT INTO "Stock" VALUES(44,15,25,23);
INSERT INTO "Stock" VALUES(45,15,27,23);
INSERT INTO "Stock" VALUES(46,16,19,25);
INSERT INTO "Stock" VALUES(47,16,21,25);
INSERT INTO "Stock" VALUES(48,16,23,25);
INSERT INTO "Stock" VALUES(49,17,19,4);
INSERT INTO "Stock" VALUES(50,17,23,4);
INSERT INTO "Stock" VALUES(51,17,25,4);
INSERT INTO "Stock" VALUES(52,17,27,4);
INSERT INTO "Stock" VALUES(53,18,18,9);
INSERT INTO "Stock" VALUES(54,18,23,9);
INSERT INTO "Stock" VALUES(55,19,18,2);
INSERT INTO "Stock" VALUES(56,19,19,2);
INSERT INTO "Stock" VALUES(57,20,21,5);
INSERT INTO "Stock" VALUES(58,20,22,5);
INSERT INTO "Stock" VALUES(59,20,23,5);
INSERT INTO "Stock" VALUES(60,20,24,5);
INSERT INTO "Stock" VALUES(61,21,18,16);
INSERT INTO "Stock" VALUES(62,21,19,16);
INSERT INTO "Stock" VALUES(63,21,23,16);
INSERT INTO "Stock" VALUES(64,21,25,16);
INSERT INTO "Stock" VALUES(65,22,18,3);
INSERT INTO "Stock" VALUES(66,22,23,3);
INSERT INTO "Stock" VALUES(67,23,30,18);
INSERT INTO "Stock" VALUES(68,23,31,18);
INSERT INTO "Stock" VALUES(69,23,32,18);
INSERT INTO "Stock" VALUES(70,23,33,18);
INSERT INTO "Stock" VALUES(71,24,23,50);
INSERT INTO "Stock" VALUES(72,24,24,50);
INSERT INTO "Stock" VALUES(73,24,25,50);
INSERT INTO "Stock" VALUES(74,24,26,50);
INSERT INTO "Stock" VALUES(75,24,27,50);
INSERT INTO "Stock" VALUES(76,24,29,50);
INSERT INTO "Stock" VALUES(77,25,29,3);
INSERT INTO "Stock" VALUES(78,25,31,3);
INSERT INTO "Stock" VALUES(79,25,34,3);
INSERT INTO "Stock" VALUES(80,26,27,23);
INSERT INTO "Stock" VALUES(81,26,29,23);
INSERT INTO "Stock" VALUES(82,26,33,23);
INSERT INTO "Stock" VALUES(83,27,31,15);
INSERT INTO "Stock" VALUES(84,27,33,15);
INSERT INTO "Stock" VALUES(85,27,34,15);
INSERT INTO "Stock" VALUES(86,28,34,3);
INSERT INTO "Stock" VALUES(87,29,29,1);
INSERT INTO "Stock" VALUES(88,29,31,1);
INSERT INTO "Stock" VALUES(89,30,31,20);
INSERT INTO "Stock" VALUES(90,30,33,20);
INSERT INTO "Stock" VALUES(91,31,29,30);
INSERT INTO "Stock" VALUES(92,31,31,30);
CREATE TABLE Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    last_name TEXT NOT NULL,
    first_name TEXT NOT NULL,
    middle_name TEXT,
    login TEXT NOT NULL UNIQUE,
    role TEXT NOT NULL
        CHECK (role IN ('Администратор', 'Менеджер', 'Авторизованный пользователь'))
);
INSERT INTO "Users" VALUES(1,'Иванов','Иван','Сергеевич','isivanov','Администратор');
INSERT INTO "Users" VALUES(2,'Петров','Пётр','Алексеевич','papetrov','Менеджер');
INSERT INTO "Users" VALUES(3,'Сидорова','Анна','Дмитриевна','asidorova','Авторизованный пользователь');
INSERT INTO "Users" VALUES(4,'Кузнецова','Екатерина','Андреевна','ekuznetsova','Менеджер');
INSERT INTO "Users" VALUES(5,'Смирнов','Дмитрий','Владимирович','dsmirnov','Авторизованный пользователь');
INSERT INTO "Users" VALUES(6,'Попов','Алексей','Николаевич','apopov','Администратор');
INSERT INTO "Users" VALUES(7,'Васильева','Ольга','Игоревна','ovasileva','Авторизованный пользователь');
INSERT INTO "Users" VALUES(8,'Соколов','Павел','Викторович','psokolov','Менеджер');
INSERT INTO "Users" VALUES(9,'Михайлова','Татьяна','Юрьевна','tmikhailova','Авторизованный пользователь');
INSERT INTO "Users" VALUES(10,'Новикова','Наталья','Сергеевна','nnovikova','Менеджер');
INSERT INTO "Users" VALUES(11,'Фёдоров','Андрей','Максимович','afedorov','Администратор');
INSERT INTO "Users" VALUES(12,'Морозов','Сергей','Павлович','smorozov','Авторизованный пользователь');
INSERT INTO "Users" VALUES(13,'Волкова','Юлия','Александровна','jvolkova','Менеджер');
INSERT INTO "Users" VALUES(14,'Алексеев','Артём','Евгеньевич','aalekseev','Авторизованный пользователь');
INSERT INTO "Users" VALUES(15,'Лебедева','Ирина','Владимировна','ilebedeva','Авторизованный пользователь');
INSERT INTO "Users" VALUES(16,'Егоров','Никита','Денисович','negorov','Менеджер');
INSERT INTO "Users" VALUES(17,'Павлова','Елена','Петровна','epavlova','Авторизованный пользователь');
INSERT INTO "Users" VALUES(18,'Козлов','Роман','Олегович','rkozlov','Администратор');
INSERT INTO "Users" VALUES(19,'Степанова','Виктория','Романовна','vstepanova','Менеджер');
INSERT INTO "Users" VALUES(20,'Николаев','Владимир','Иванович','vnikolaev','Авторизованный пользователь');
CREATE INDEX idx_products_category ON Products (category_id);
CREATE INDEX idx_products_manufacturer ON Products (manufacturer_id);
CREATE INDEX idx_stock_product ON Stock (product_id);
CREATE INDEX idx_orders_user ON Orders (user_id);
CREATE INDEX idx_orders_date ON Orders (order_date);
CREATE INDEX idx_orderitems_order ON OrderItems (order_id);
CREATE INDEX idx_orderitems_stock ON OrderItems (stock_id);
DELETE FROM "sqlite_sequence";
INSERT INTO "sqlite_sequence" VALUES('Sizes',127);
INSERT INTO "sqlite_sequence" VALUES('Users',20);
INSERT INTO "sqlite_sequence" VALUES('Categories',62);
INSERT INTO "sqlite_sequence" VALUES('Manufacturers',62);
INSERT INTO "sqlite_sequence" VALUES('Products',31);
INSERT INTO "sqlite_sequence" VALUES('Stock',92);
INSERT INTO "sqlite_sequence" VALUES('Orders',10);
INSERT INTO "sqlite_sequence" VALUES('OrderItems',30);
COMMIT;
