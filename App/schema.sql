--
-- Database: `government-grant-disbursement`
--
CREATE DATABASE IF NOT EXISTS `government-grant-disbursement` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `government-grant-disbursement`;

-- --------------------------------------------------------

--
-- Table structure for table `household`
--

DROP TABLE IF EXISTS `household`;
CREATE TABLE IF NOT EXISTS `household` (
  `household_id` int(6) NOT NULL AUTO_INCREMENT,
  `housing_type` varchar(64) NOT NULL,
  PRIMARY KEY (`household_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `family_member`
--

DROP TABLE IF EXISTS `family_member`;
CREATE TABLE IF NOT EXISTS `family_member` (
  `family_member_id` int(6) NOT NULL AUTO_INCREMENT,
  `household_id` int(6) NOT NULL,
  `name` varchar(64) NOT NULL,
  `gender` varchar(10) NOT NULL,
  `marital_status` varchar(64) NOT NULL,
  `spouse` varchar(64) NOT NULL,
  `occupation_type` varchar(64) NOT NULL,
  `annual_income` decimal(20,2) NOT NULL,
  `dob` date NOT NULL,
  PRIMARY KEY (`family_member_id`),
  FOREIGN KEY (`household_id`) REFERENCES `household` (`household_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;