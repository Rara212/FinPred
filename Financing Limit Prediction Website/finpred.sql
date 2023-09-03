-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 20, 2023 at 03:04 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `finpred`
--

-- --------------------------------------------------------

--
-- Table structure for table `customerpred`
--

CREATE TABLE `customerpred` (
  `pby_bank` varchar(20) NOT NULL,
  `uang_muka` varchar(20) NOT NULL,
  `omset_xbrl` varchar(20) NOT NULL,
  `ratio_rbh` varchar(20) NOT NULL,
  `jangka_waktu_bulan` varchar(20) NOT NULL,
  `nilai_agunan` varchar(20) NOT NULL,
  `equivalen_rate_kontrak` varchar(20) NOT NULL,
  `sektor_ekonomi` varchar(20) NOT NULL,
  `golongan_pemilik` varchar(20) NOT NULL,
  `kode_produk` varchar(20) NOT NULL,
  `kategori_usaha` varchar(20) NOT NULL,
  `kategori_nasabah` varchar(20) NOT NULL,
  `kategori_produk` varchar(20) NOT NULL,
  `kategori_segmen` varchar(20) NOT NULL,
  `kode_bisnis` varchar(20) NOT NULL,
  `jenis_piutang` varchar(20) NOT NULL,
  `kategori_portofolio` varchar(20) NOT NULL,
  `result` varchar(20) NOT NULL,
  `id` int(50) NOT NULL,
  `ao_id` int(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `customerpred`
--

INSERT INTO `customerpred` (`pby_bank`, `uang_muka`, `omset_xbrl`, `ratio_rbh`, `jangka_waktu_bulan`, `nilai_agunan`, `equivalen_rate_kontrak`, `sektor_ekonomi`, `golongan_pemilik`, `kode_produk`, `kategori_usaha`, `kategori_nasabah`, `kategori_produk`, `kategori_segmen`, `kode_bisnis`, `jenis_piutang`, `kategori_portofolio`, `result`, `id`, `ao_id`) VALUES
('47000000000.0', '28834334852.0', '42836661071.0', '99.99', '96.0', '39022790460.0', '13.0', '852000', '8152', '913', '90', '4', '0', '5', '102', '2', '35', '[1]', 8, 1),
('47000000000.0', '28834334852.0', '42836661071.0', '99.99', '96.0', '39022790460.0', '13.0', '852000', '8152', '913', '90', '4', '0', '5', '102', '2', '35', '[1]', 9, 1),
('47000000000.0', '28834334852.0', '42836661071.0', '99.99', '96.0', '39022790460.0', '13.0', '852000', '8152', '913', '90', '4', '0', '5', '102', '2', '35', '[1]', 10, 1),
('47000000000.0', '28834334852.0', '42836661071.0', '99.99', '96.0', '39022790460.0', '13.0', '852000', '8152', '913', '90', '4', '0', '5', '102', '2', '35', '[1]', 11, 1),
('0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '0.0', '851000', '601', '902', '10', '0', '0', '1', '101', '0', '15', '[3]', 12, 1),
('50000000000.0', '23472492864.0', '13219162107.0', '99.99', '101.0', '41367120450.0', '10.25', '861000', '601', '902', '10', '0', '0', '1', '101', '0', '15', '[4]', 13, 1);

-- --------------------------------------------------------

--
-- Table structure for table `login_log`
--

CREATE TABLE `login_log` (
  `date` timestamp NOT NULL DEFAULT current_timestamp(),
  `name` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `login_log`
--

INSERT INTO `login_log` (`date`, `name`) VALUES
('2023-07-16 17:00:00', 'mutya'),
('2023-07-17 07:10:53', 'mutya'),
('2023-07-17 08:12:57', 'mutya'),
('2023-07-18 05:59:05', 'mutya'),
('2023-07-18 06:24:26', 'mutya'),
('2023-07-18 06:26:32', 'mutya'),
('2023-07-18 06:29:19', 'mutya'),
('2023-07-19 00:08:40', 'mutya'),
('2023-07-20 08:06:54', 'mutya'),
('2023-07-20 08:09:06', 'mutya'),
('2023-07-20 08:23:46', 'mutya'),
('2023-07-20 12:37:50', 'mutya');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(50) NOT NULL,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `name`, `email`) VALUES
(1, 'mutya', 'mutya@gmail.com');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `customerpred`
--
ALTER TABLE `customerpred`
  ADD PRIMARY KEY (`id`),
  ADD KEY `ao_id` (`ao_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `customerpred`
--
ALTER TABLE `customerpred`
  MODIFY `id` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `customerpred`
--
ALTER TABLE `customerpred`
  ADD CONSTRAINT `customerpred_ibfk_1` FOREIGN KEY (`ao_id`) REFERENCES `users` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
