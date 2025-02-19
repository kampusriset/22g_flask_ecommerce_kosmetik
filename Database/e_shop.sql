-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3307
-- Waktu pembuatan: 19 Feb 2025 pada 03.43
-- Versi server: 10.4.32-MariaDB
-- Versi PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `e_shop`
--

-- --------------------------------------------------------

--
-- Struktur dari tabel `cart`
--

CREATE TABLE `cart` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `orders`
--

CREATE TABLE `orders` (
  `order_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `address` text NOT NULL,
  `total_price` decimal(10,2) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `orders`
--

INSERT INTO `orders` (`order_id`, `user_id`, `address`, `total_price`, `created_at`) VALUES
(1, 5, 'gumpang kartasura', 660000.00, '2025-01-31 05:48:55'),
(2, 5, 'gumpang permai', 255000.00, '2025-01-31 05:57:16'),
(3, 5, 'experiment', 1560000.00, '2025-01-31 06:37:33');

-- --------------------------------------------------------

--
-- Struktur dari tabel `order_items`
--

CREATE TABLE `order_items` (
  `id` int(11) NOT NULL,
  `order_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL,
  `total_price` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Struktur dari tabel `product`
--

CREATE TABLE `product` (
  `id` int(11) NOT NULL,
  `product_name` varchar(255) NOT NULL,
  `price` int(11) NOT NULL,
  `description` text NOT NULL,
  `image` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `product`
--

INSERT INTO `product` (`id`, `product_name`, `price`, `description`, `image`) VALUES
(13, 'Teratai', 1300000, 'aku adalah kingkong', '295306.jpg'),
(14, 'Nivea', 130000, 'Nivea Man 200000', 'nivea.jpg'),
(15, 'Marina', 125000, 'Produk marina hasil olahan kedelai', 'marina.png'),
(16, 'Kahf', 130000, 'Produk hasil olahan anak bangsa', 'download.jpeg'),
(17, 'Scarlet', 140000, 'produk milik scarlet', 'scarlet_.png');

-- --------------------------------------------------------

--
-- Struktur dari tabel `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `role` enum('admin','user') DEFAULT 'user'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data untuk tabel `users`
--

INSERT INTO `users` (`id`, `username`, `password_hash`, `email`, `role`) VALUES
(3, 'bayu', 'scrypt:32768:8:1$ddpikrub2Vrf6jPh$5daea32259659996b4b14fbd78f85aabfee0bb458f8c93d463a75f24d424755781bb34d3c7af73922940f8cb4105189645503645025ac19fc4b5c01b99034c4c', 'bayu12@gmail.com', 'user'),
(5, 'saiful', 'scrypt:32768:8:1$MboUrQNQc7V3TkOQ$4094367d3959d1daea5c783a1d66b7cc664eee4e444edd7f349dcc924a9749e18d45a7336b4eb5c24d431542db8dfd481c93aa5fdaa12c20d07e85e2565a7249', 'saiful12@gmail.com', 'user'),
(10, 'nisa', 'scrypt:32768:8:1$1Ixjz1O7hOTFpP7d$f10f33822894d3e0a57114da6b90491dd14041aac372416308095c95947f38a1f0b9098dedb572cc99fa7d4fc97cc81571164eb52be599335cdc99c2419e4473', 'nisa@gmail.com', 'user'),
(11, 'admin', 'scrypt:32768:8:1$Koxc0QjVJje8QbFy$1d345375294d21ac4e0d2d22a43e78c928c63ec73650fb37dae940d43fe37c7ffb4d8091ec349d2dc1961aa88b5d3735a02e9986e8f2a3be2c76e9d633ef84fc', 'admin@gmail.com', 'admin'),
(12, 'riz', 'scrypt:32768:8:1$6lrrDU1hjF9AksWf$e8f5de5d7863906956c4e1ae50f4a7c99c3d3d8357e313933ea0ef8cb5b23995bed738d29568b65896467ec9b78fab7a28b977da32fc76d73d37976aa708a7b8', 'riz12@gmail.com', 'user');

--
-- Indexes for dumped tables
--

--
-- Indeks untuk tabel `cart`
--
ALTER TABLE `cart`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `product_id` (`product_id`);

--
-- Indeks untuk tabel `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`order_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indeks untuk tabel `order_items`
--
ALTER TABLE `order_items`
  ADD PRIMARY KEY (`id`),
  ADD KEY `order_id` (`order_id`),
  ADD KEY `product_id` (`product_id`);

--
-- Indeks untuk tabel `product`
--
ALTER TABLE `product`
  ADD PRIMARY KEY (`id`);

--
-- Indeks untuk tabel `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT untuk tabel yang dibuang
--

--
-- AUTO_INCREMENT untuk tabel `cart`
--
ALTER TABLE `cart`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT untuk tabel `orders`
--
ALTER TABLE `orders`
  MODIFY `order_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT untuk tabel `order_items`
--
ALTER TABLE `order_items`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT untuk tabel `product`
--
ALTER TABLE `product`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT untuk tabel `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- Ketidakleluasaan untuk tabel pelimpahan (Dumped Tables)
--

--
-- Ketidakleluasaan untuk tabel `cart`
--
ALTER TABLE `cart`
  ADD CONSTRAINT `cart_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `cart_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`);

--
-- Ketidakleluasaan untuk tabel `orders`
--
ALTER TABLE `orders`
  ADD CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Ketidakleluasaan untuk tabel `order_items`
--
ALTER TABLE `order_items`
  ADD CONSTRAINT `order_items_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `order_items_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `product` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
