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
  `household_type` varchar(64) NOT NULL,
  PRIMARY KEY (`household_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `household`
--

INSERT INTO `household` (`household_type`) VALUES
('Landed'),
('Condominium'),
('HDB'),
('Condominium'),
('HDB');
COMMIT;

-- --------------------------------------------------------

--
-- Table structure for table `member`
--

DROP TABLE IF EXISTS `member`;
CREATE TABLE IF NOT EXISTS `member` (
  `member_id` int(6) NOT NULL AUTO_INCREMENT,
  `household_id` int(6) NOT NULL,
  `name` varchar(64) NOT NULL,
  `gender` varchar(10) NOT NULL,
  `marital_status` varchar(64) NOT NULL,
  `spouse` varchar(64) NOT NULL,
  `occupation_type` varchar(64) NOT NULL,
  `annual_income` decimal(20,2) NOT NULL,
  `dob` date NOT NULL,
  PRIMARY KEY (`member_id`),
  FOREIGN KEY (`household_id`) REFERENCES `household` (`household_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `member`
--

INSERT INTO `member` (`household_id`,`name`,`gender`,`marital_status`,`spouse`,`occupation_type`,`annual_income`,`dob`) VALUES
(1,'John','male','married','Mary','employed',50000,'1990-01-01'),
(1,'Mary','female','married','John','employed',75000,'1990-01-01'),
(1,'Sonny','male','single','','Student',0,'2010-01-01'),
(2,'Sam','male','married','Jessica','Unemployed',0,'1990-01-01'),
(2,'Jessica','female','married','John','Unemployed',0,'1990-01-01'),
(2,'OldMan','male','single','','Unemployed',0,'1950-01-01'),
(3,'Sam','male','single','','Unemployed',0,'1990-01-01'),
(3,'Ahpek','male','single','','Unemployed',0,'1951-01-01'),
(4,'Lisa','female','single','','Unemployed',0,'1990-01-01'),
(4,'Baby','male','single','','Unemployed',0,'2022-07-01'),
(5,'James','male','married','','employed',50000,'1990-01-01'),
(5,'Xin Wei','female','married','','Student',10000,'1992-01-01');
COMMIT;