-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 23, 2025 at 03:09 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `project`
--

--
-- Dumping data for table `airline`
--

INSERT INTO `airline` (`name`) VALUES
('China Eastern'),
('Delta Airlines'),
('Jet Blue');

--
-- Dumping data for table `airline_email`
--

INSERT INTO `airline_email` (`username`, `staff_email`) VALUES
('pvg_admin', 'celinalee@yahoo.com');

--
-- Dumping data for table `airline_staff`
--

INSERT INTO `airline_staff` (`username`, `password`, `first_name`, `last_name`, `date_of_birth`, `airline_name`) VALUES
('jetblue_admin', 'passw0rd', 'Alice', 'Smith', '07042000', 'Jet Blue'),
('pvg_admin', '21232f297a57a5a743894a0e4a801fc3', 'Celina', 'Lee', '1990-08-', 'China Eastern');

--
-- Dumping data for table `airplane`
--

INSERT INTO `airplane` (`airplane_ID`, `airline_name`, `num_seats`, `manufacturing_company`) VALUES
(1920, 'Jet Blue', 100, 'Plane Inc'),
(2012, 'Jet Blue', 180, 'Boeing'),
(3001, 'China Eastern', 150, 'Boeing'),
(3002, 'China Eastern', 200, 'Airbus'),
(3003, 'China Eastern', 180, 'COMAC'),
(3014, 'China Eastern', 120, 'Boeing'),
(4001, 'Delta Airlines', 160, 'Boeing'),
(4002, 'Delta Airlines', 220, 'Airbus'),
(8012, 'Jet Blue', 200, 'Plane Corp');

--
-- Dumping data for table `airport`
--

INSERT INTO `airport` (`code`, `name`, `city`, `country`) VALUES
('CDG', 'Paris Charles de Gau', 'Paris', 'France'),
('DOH', 'Doha Hamad Internati', 'Doha', 'Qatar'),
('JFK', 'John F. Kennedy Airp', 'New York City', 'USA'),
('LAX', 'Los Angeles Internat', 'Los Angeles', 'USA'),
('PVG', 'Shanghai Pudong Airp', 'Shanghai', 'China');

--
-- Dumping data for table `customer`
--

INSERT INTO `customer` (`email`, `name`, `password`, `building_number`, `street`, `city`, `state`, `phone_number`, `passport_number`, `passport_expiration`, `passport_country`, `date_of_birth`) VALUES
('allie@gmail.com', 'Allie Marcu', 'Pass123', '444', 'Champion St', 'Brooklyn', 'New York', '7021892288', '000099992', '2025-11-18', 'USA', '1990-01-03'),
('jj@icloud.com', 'John James', 'blahblah', '2', 'Broadway', 'Los Angeles', 'California', '3892849829', '23892849', '2029-03-05', 'USA', '2000-01-01'),
('tanzia@yahoo.com', 'Tanzia Nur', 'Word0000', '123', 'Sesame St', 'Las Vegas', 'Nevada', '1902229999', '12290989', '2035-09-27', 'USA', '1980-12-30'),
('thisisatest@gmail.com', 'Mary Jane', '5f4dcc3b5aa765d61d8327deb882cf99', '345', 'Atlantic Ave', 'Brooklyn', 'NY', '5678901234', '11122233', '2029-04-19', 'USA', '1985-04-12');

--
-- Dumping data for table `flight`
--

INSERT INTO `flight` (`airline_name`, `flight_number`, `departure_datetime`, `arrival_datetime`, `airplane_ID`, `departure_airport_code`, `arrival_airport_code`, `base_price`, `status`) VALUES
('China Eastern', 'MU456', '2025-04-22 14:00:00', '2025-04-23 06:30:00', 3001, 'PVG', 'CDG', 900.00, 'On Time'),
('China Eastern', 'MU587', '2025-03-26 09:00:00', '2025-03-27 01:00:00', 3002, 'PVG', 'JFK', 950.00, 'On Time'),
('China Eastern', 'MU588', '2025-04-11 10:00:00', '2025-04-12 02:00:00', 3003, 'PVG', 'JFK', 550.00, 'On Time'),
('China Eastern', 'MU673', '2025-04-30 17:00:00', '2025-05-01 14:00:00', 3014, 'PVG', 'LAX', 450.00, 'Upcoming'),
('Delta Airlines', 'DL123', '2025-04-20 10:00:00', '2025-04-20 13:30:00', 4001, 'JFK', 'LAX', 300.00, 'On Time'),
('Delta Airlines', 'DL287', '2025-04-16 11:00:00', '2025-04-17 03:00:00', 4002, 'JFK', 'PVG', 950.00, 'On Time'),
('Jet Blue', 'JB100', '2025-04-10 08:00:00', '2025-04-11 00:00:00', 2012, 'JFK', 'PVG', 500.00, 'Delayed'),
('Jet Blue', 'JB150', '2025-04-15 09:00:00', '2025-04-16 01:00:00', 8012, 'PVG', 'JFK', 890.00, 'On Time'),
('Jet Blue', 'JB202', '2025-03-25 07:00:00', '2025-03-25 23:00:00', 1920, 'JFK', 'PVG', 899.00, 'On Time'),
('Jet Blue', 'JB789', '2025-04-25 08:00:00', '2025-04-25 19:00:00', 1920, 'JFK', 'DOH', 1300.00, 'On Time');

--
-- Dumping data for table `purchase`
--

INSERT INTO `purchase` (`ticket_ID`, `email`, `card_type`, `card_number`, `card_name`, `card_expiry`, `purchase_datetime`, `sold_price`) VALUES
(1290, 'tanzia@yahoo.com', 'AmEx', '378282246310005', 'Tanzia Nur', '2026-11-01', '2025-03-03 12:00:00', 890.00),
(4902, 'allie@gmail.com', 'Visa', '4111111111111111', 'Allie Marcu', '2028-01-01', '2025-03-01 10:00:00', 890.00),
(28943, 'jj@icloud.com', 'MasterCard', '5555555555554444', 'John James', '2027-12-01', '2025-03-02 11:00:00', 890.00);

--
-- Dumping data for table `staff_phone`
--

INSERT INTO `staff_phone` (`username`, `phone_number`) VALUES
('pvg_admin', '5431239845');

--
-- Dumping data for table `ticket`
--

INSERT INTO `ticket` (`ticket_ID`, `airline_name`, `flight_number`, `departure_datetime`) VALUES
(1290, 'Jet Blue', 'JB150', '2025-04-15 09:00:00'),
(4902, 'Jet Blue', 'JB150', '2025-04-15 09:00:00'),
(28943, 'Jet Blue', 'JB150', '2025-04-15 09:00:00');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
