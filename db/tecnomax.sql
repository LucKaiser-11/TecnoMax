-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1:3306
-- Tiempo de generación: 28-09-2025 a las 23:00:34
-- Versión del servidor: 9.1.0
-- Versión de PHP: 8.3.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `tecnomax`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `bitacora`
--

DROP TABLE IF EXISTS `bitacora`;
CREATE TABLE IF NOT EXISTS `bitacora` (
  `id_bitacora` int NOT NULL AUTO_INCREMENT,
  `accion` varchar(255) DEFAULT NULL,
  `fecha` datetime DEFAULT CURRENT_TIMESTAMP,
  `ip_origen` varchar(45) DEFAULT NULL,
  `id_persona` int DEFAULT NULL,
  PRIMARY KEY (`id_bitacora`),
  KEY `id_persona` (`id_persona`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `carrito`
--

DROP TABLE IF EXISTS `carrito`;
CREATE TABLE IF NOT EXISTS `carrito` (
  `id_carrito` int NOT NULL AUTO_INCREMENT,
  `cantidad` int DEFAULT NULL,
  `fecha_agregado` datetime DEFAULT NULL,
  `persona_id` int DEFAULT NULL,
  `producto_id` int DEFAULT NULL,
  PRIMARY KEY (`id_carrito`),
  KEY `persona_id` (`persona_id`),
  KEY `producto_id` (`producto_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `categorias`
--

DROP TABLE IF EXISTS `categorias`;
CREATE TABLE IF NOT EXISTS `categorias` (
  `id_categoria` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(30) DEFAULT NULL,
  `descripcion` text,
  PRIMARY KEY (`id_categoria`)
) ENGINE=MyISAM AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `categorias`
--

INSERT INTO `categorias` (`id_categoria`, `nombre`, `descripcion`) VALUES
(1, 'Laptops', 'Equipos portátiles para trabajo y estudio'),
(2, 'Smartphones', 'Teléfonos móviles inteligentes'),
(3, 'Accesorios', 'Cables, fundas, soportes, adaptadores'),
(4, 'Audio', 'Auriculares, parlantes, micrófonos'),
(5, 'Almacenamiento', 'Discos duros, SSD, memorias USB'),
(6, 'Periféricos', 'Teclados, mouse, monitores'),
(7, 'Redes', 'Routers, switches, tarjetas de red'),
(8, 'Componentes', 'RAM, placas madre, procesadores'),
(9, 'Gaming', 'Consolas, controles, sillas gamer'),
(10, 'Domótica', 'Smart home: enchufes, luces, asistentes');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalle_pedido`
--

DROP TABLE IF EXISTS `detalle_pedido`;
CREATE TABLE IF NOT EXISTS `detalle_pedido` (
  `id_detalle_pedido` int NOT NULL AUTO_INCREMENT,
  `cantidad` int DEFAULT NULL,
  `precio_unitario` decimal(10,2) DEFAULT NULL,
  `pedido_id` int DEFAULT NULL,
  `producto_id` int DEFAULT NULL,
  PRIMARY KEY (`id_detalle_pedido`),
  KEY `pedido_id` (`pedido_id`),
  KEY `producto_id` (`producto_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `devoluciones`
--

DROP TABLE IF EXISTS `devoluciones`;
CREATE TABLE IF NOT EXISTS `devoluciones` (
  `id_devolucion` int NOT NULL AUTO_INCREMENT,
  `motivo` text,
  `fecha` datetime DEFAULT NULL,
  `pedido_id` int DEFAULT NULL,
  `estado_id` int DEFAULT NULL,
  PRIMARY KEY (`id_devolucion`),
  KEY `pedido_id` (`pedido_id`),
  KEY `estado_id` (`estado_id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `devoluciones`
--

INSERT INTO `devoluciones` (`id_devolucion`, `motivo`, `fecha`, `pedido_id`, `estado_id`) VALUES
(1, 'Producto defectuoso', '2025-09-28 01:10:06', 2, 3);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `envios`
--

DROP TABLE IF EXISTS `envios`;
CREATE TABLE IF NOT EXISTS `envios` (
  `id_envio` int NOT NULL AUTO_INCREMENT,
  `direccion_entrega` varchar(50) DEFAULT NULL,
  `fecha_envio` datetime DEFAULT NULL,
  `costo_envio` decimal(10,2) DEFAULT NULL,
  `tipo_envio` varchar(50) DEFAULT NULL,
  `pedido_id` int DEFAULT NULL,
  `estado_id` int DEFAULT NULL,
  PRIMARY KEY (`id_envio`),
  KEY `pedido_id` (`pedido_id`),
  KEY `estado_id` (`estado_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `envios`
--

INSERT INTO `envios` (`id_envio`, `direccion_entrega`, `fecha_envio`, `costo_envio`, `tipo_envio`, `pedido_id`, `estado_id`) VALUES
(1, 'Calle 12 #99', '2025-09-28 01:09:51', 50.00, 'express', 1, 2),
(2, 'Av. Central 45', '2025-09-28 01:09:51', 30.00, 'normal', 2, 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `estados_generales`
--

DROP TABLE IF EXISTS `estados_generales`;
CREATE TABLE IF NOT EXISTS `estados_generales` (
  `id_estado` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) DEFAULT NULL,
  `descripcion` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_estado`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `historial_precios`
--

DROP TABLE IF EXISTS `historial_precios`;
CREATE TABLE IF NOT EXISTS `historial_precios` (
  `id_historial_precio` int NOT NULL AUTO_INCREMENT,
  `precio_anterior` decimal(10,2) DEFAULT NULL,
  `precio_nuevo` decimal(10,2) DEFAULT NULL,
  `fecha` datetime DEFAULT NULL,
  `producto_id` int DEFAULT NULL,
  PRIMARY KEY (`id_historial_precio`),
  KEY `producto_id` (`producto_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `inventario`
--

DROP TABLE IF EXISTS `inventario`;
CREATE TABLE IF NOT EXISTS `inventario` (
  `id_inventario` int NOT NULL AUTO_INCREMENT,
  `cantidad_actual` int DEFAULT NULL,
  `fecha_actualizacion` datetime DEFAULT NULL,
  `producto_id` int DEFAULT NULL,
  PRIMARY KEY (`id_inventario`),
  KEY `producto_id` (`producto_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `inventario`
--

INSERT INTO `inventario` (`id_inventario`, `cantidad_actual`, `fecha_actualizacion`, `producto_id`) VALUES
(1, 15, '2025-09-28 01:09:03', 1),
(2, 40, '2025-09-28 01:09:03', 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `multimedia`
--

DROP TABLE IF EXISTS `multimedia`;
CREATE TABLE IF NOT EXISTS `multimedia` (
  `id_multimedia` int NOT NULL AUTO_INCREMENT,
  `url_multimedia` varchar(255) DEFAULT NULL,
  `descripcion` varchar(50) DEFAULT NULL,
  `producto_id` int DEFAULT NULL,
  `tipo_multimedia` int DEFAULT NULL,
  PRIMARY KEY (`id_multimedia`),
  KEY `producto_id` (`producto_id`),
  KEY `tipo_multimedia` (`tipo_multimedia`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pagos`
--

DROP TABLE IF EXISTS `pagos`;
CREATE TABLE IF NOT EXISTS `pagos` (
  `id_pago` int NOT NULL AUTO_INCREMENT,
  `fecha_pago` datetime DEFAULT NULL,
  `monto` decimal(10,2) DEFAULT NULL,
  `pedido_id` int DEFAULT NULL,
  `estado_id` int DEFAULT NULL,
  PRIMARY KEY (`id_pago`),
  KEY `pedido_id` (`pedido_id`),
  KEY `estado_id` (`estado_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pedidos`
--

DROP TABLE IF EXISTS `pedidos`;
CREATE TABLE IF NOT EXISTS `pedidos` (
  `id_pedido` int NOT NULL AUTO_INCREMENT,
  `fecha` datetime DEFAULT NULL,
  `estado_general` varchar(50) DEFAULT NULL,
  `persona_id` int DEFAULT NULL,
  PRIMARY KEY (`id_pedido`),
  KEY `persona_id` (`persona_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `persona`
--

DROP TABLE IF EXISTS `persona`;
CREATE TABLE IF NOT EXISTS `persona` (
  `id_persona` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(30) DEFAULT NULL,
  `apellidoPat` varchar(30) DEFAULT NULL,
  `apellidoMat` varchar(30) DEFAULT NULL,
  `correo_` varchar(50) DEFAULT NULL,
  `direccion` varchar(255) DEFAULT NULL,
  `telefono` varchar(10) DEFAULT NULL,
  `contrase` varchar(100) DEFAULT NULL,
  `rol_id` int DEFAULT NULL,
  PRIMARY KEY (`id_persona`),
  KEY `rol_id` (`rol_id`)
) ENGINE=MyISAM AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `persona`
--

INSERT INTO `persona` (`id_persona`, `nombre`, `apellidoPat`, `apellidoMat`, `correo_`, `direccion`, `telefono`, `contrase`, `rol_id`) VALUES
(1, 'Lucas', 'Leigue', 'Menacho', 'lucadleigue@gmail.com', 'Av. Siempre Viva 123', '75529469', '12345678', 3),
(2, 'Nagely', 'Ajhuacho', 'Calizaya', 'nagelyaa4@gmail.com', 'Calle 5 #45', '62065744', '12345678', 3),
(3, 'Ronaldo', 'Cr7', 'Rodri', 'rodricr7@gmail.com', 'avenida plan 3000', '75337903', '12345678', 2),
(4, 'Romario', 'Martinez', 'Loayza', 'romario@gmail.com', 'Ave. 6 agosto', '79853147', '12345678', 2),
(5, 'Leonardo', 'Menacho', 'Leigue', 'leo@gmail.com', 'avenida nunca viva', '61509652', '12345678', 2);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `productos`
--

DROP TABLE IF EXISTS `productos`;
CREATE TABLE IF NOT EXISTS `productos` (
  `id_producto` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) DEFAULT NULL,
  `descripcion` text,
  `precio` decimal(10,2) DEFAULT NULL,
  `categoria_id` int DEFAULT NULL,
  `proveedor_id` int DEFAULT NULL,
  PRIMARY KEY (`id_producto`),
  KEY `categoria_id` (`categoria_id`),
  KEY `proveedor_id` (`proveedor_id`)
) ENGINE=MyISAM AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `productos`
--

INSERT INTO `productos` (`id_producto`, `nombre`, `descripcion`, `precio`, `categoria_id`, `proveedor_id`) VALUES
(1, 'Laptop TecnoMax Pro', 'Intel i7, 16GB RAM, SSD 512GB', 31050.00, 1, 1),
(2, 'Auriculares Pro', 'Bluetooth, cancelación de ruido', 2208.00, 2, 2),
(3, 'Smartphone X10', 'Pantalla AMOLED, 128GB, cámara triple', 19320.00, 3, 1),
(4, 'Teclado Mecánico RGB', 'Switches azules, retroiluminado', 1725.00, 6, 2),
(5, 'Mouse Gamer GX', 'Sensor óptico 16000 DPI, RGB', 1242.00, 6, 2),
(6, 'SSD 1TB NVMe', 'Velocidad de lectura 3500MB/s', 4968.00, 5, 1),
(7, 'Memoria RAM 16GB DDR4', '3200MHz, CL16', 2898.00, 8, 1),
(8, 'Monitor 27\" 2K', 'IPS, 144Hz, sin bordes', 11040.00, 6, 2),
(9, 'Router WiFi 6', 'Cobertura extendida, 4 antenas', 4692.00, 7, 1),
(10, 'Switch 8 Puertos Gigabit', 'Administrable, carcasa metálica', 2691.00, 7, 1),
(11, 'Consola GameBox Z', '4K HDR, 1TB, mando incluido', 22080.00, 9, 2),
(12, 'Silla Gamer Pro', 'Ergonómica, reclinable, soporte lumbar', 14490.00, 9, 2),
(13, 'Cámara IP Smart', 'Detección de movimiento, visión nocturna', 5865.00, 10, 1),
(14, 'Enchufe Inteligente WiFi', 'Control remoto desde app', 1242.00, 10, 1),
(15, 'Hub USB-C 7 en 1', 'HDMI, USB 3.0, lector SD', 1794.00, 3, 2),
(16, 'Power Bank 20000mAh', 'Carga rápida, doble salida', 2208.00, 3, 2),
(17, 'Parlante Bluetooth 360°', 'Resistente al agua, batería 12h', 3726.00, 2, 2),
(18, 'Micrófono Condensador USB', 'Ideal para streaming y podcast', 3312.00, 2, 2),
(19, 'Disco Duro Externo 2TB', 'USB 3.1, carcasa resistente', 4278.00, 5, 1),
(20, 'Procesador Ryzen 7 5800X', '8 núcleos, 16 hilos, 4.7GHz', 12420.00, 8, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `proveedores`
--

DROP TABLE IF EXISTS `proveedores`;
CREATE TABLE IF NOT EXISTS `proveedores` (
  `id_proveedor` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(30) DEFAULT NULL,
  `contacto` varchar(50) DEFAULT NULL,
  `direccion` varchar(255) DEFAULT NULL,
  `telefono` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id_proveedor`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `proveedores`
--

INSERT INTO `proveedores` (`id_proveedor`, `nombre`, `contacto`, `direccion`, `telefono`) VALUES
(1, 'TechBol', 'Carlos Rojas', 'Zona Industrial', '700123456'),
(2, 'AudioMax', 'Laura Pérez', 'Av. Sonido 88', '701234567');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `registro_movimientos`
--

DROP TABLE IF EXISTS `registro_movimientos`;
CREATE TABLE IF NOT EXISTS `registro_movimientos` (
  `id_movimiento` int NOT NULL AUTO_INCREMENT,
  `tipo_movimiento` varchar(20) DEFAULT NULL,
  `cantidad` int DEFAULT NULL,
  `fecha` datetime DEFAULT NULL,
  `producto_id` int DEFAULT NULL,
  `persona_id` int DEFAULT NULL,
  PRIMARY KEY (`id_movimiento`),
  KEY `producto_id` (`producto_id`),
  KEY `persona_id` (`persona_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `rese`
--

DROP TABLE IF EXISTS `rese`;
CREATE TABLE IF NOT EXISTS `rese` (
  `id_rese` int NOT NULL AUTO_INCREMENT,
  `comentario` text,
  `calificacion` int DEFAULT NULL,
  `fecha` datetime DEFAULT NULL,
  `persona_id` int DEFAULT NULL,
  `producto_id` int DEFAULT NULL,
  PRIMARY KEY (`id_rese`),
  KEY `persona_id` (`persona_id`),
  KEY `producto_id` (`producto_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `rol`
--

DROP TABLE IF EXISTS `rol`;
CREATE TABLE IF NOT EXISTS `rol` (
  `id_rol` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_rol`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `rol`
--

INSERT INTO `rol` (`id_rol`, `nombre`) VALUES
(1, 'admin'),
(2, 'cliente'),
(3, 'trabajador');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipo_multimedia`
--

DROP TABLE IF EXISTS `tipo_multimedia`;
CREATE TABLE IF NOT EXISTS `tipo_multimedia` (
  `id_tipo_multimedia` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) DEFAULT NULL,
  `descripcion` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id_tipo_multimedia`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Volcado de datos para la tabla `tipo_multimedia`
--

INSERT INTO `tipo_multimedia` (`id_tipo_multimedia`, `nombre`, `descripcion`) VALUES
(1, 'imagen', 'Fotografía del producto'),
(2, 'video', 'Demostración en uso');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
