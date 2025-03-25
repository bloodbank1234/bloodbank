/*
SQLyog Enterprise - MySQL GUI v6.56
MySQL - 5.5.27 : Database - bloodbank
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/`bloodbank` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `bloodbank`;

/*Table structure for table `blood_alert` */

DROP TABLE IF EXISTS `blood_alert`;

CREATE TABLE `blood_alert` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hsp_id` varchar(1000) DEFAULT NULL,
  `blood_type` varchar(1000) DEFAULT NULL,
  `contact` varchar(100) DEFAULT NULL,
  `desc` varchar(1000) DEFAULT NULL,
  `donor_name` longtext,
  `donor_mobile` longtext,
  `status` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

/*Data for the table `blood_alert` */

insert  into `blood_alert`(`id`,`hsp_id`,`blood_type`,`contact`,`desc`,`donor_name`,`donor_mobile`,`status`) values (1,'6','A+','09493040484','hi','streamway','09493040484','Approved'),(2,'5','A+','09493040484','we required this Blood urgent if any body is interested','waiting','waiting','Pending');

/*Table structure for table `donation_request` */

DROP TABLE IF EXISTS `donation_request`;

CREATE TABLE `donation_request` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hsp` varchar(1000) DEFAULT NULL,
  `name` varchar(1000) DEFAULT NULL,
  `email` varchar(1000) DEFAULT NULL,
  `disease` varchar(1000) DEFAULT NULL,
  `blood_type` varchar(1000) DEFAULT NULL,
  `b_unites` varchar(1000) DEFAULT NULL,
  `r_date` varchar(1000) DEFAULT NULL,
  `status` varchar(1000) DEFAULT NULL,
  `age` varchar(1000) DEFAULT NULL,
  `gender` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;

/*Data for the table `donation_request` */

insert  into `donation_request`(`id`,`hsp`,`name`,`email`,`disease`,`blood_type`,`b_unites`,`r_date`,`status`,`age`,`gender`) values (1,'5','streamway','streamwaytechnologiespvtltd@gmail.com','Nothing','A+','5','2025-02-20','Approved','23','Male'),(2,'5','streamway','streamwaytechnologiespvtltd@gmail.com','Nothing','A+','4','2025-03-07','Approved','27','Male'),(3,'6','kishan','kishan@gmail.com','Nothing','B+','3','2025-03-08','Approved','34','Male'),(4,'5','kishan','gkvtechsolutions@gmail.com','Nothing','A+','5','2025-03-17','Approved','56','Male');

/*Table structure for table `donor` */

DROP TABLE IF EXISTS `donor`;

CREATE TABLE `donor` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `f_name` varchar(1000) DEFAULT NULL,
  `email` varchar(1000) DEFAULT NULL,
  `mobile` varchar(1000) DEFAULT NULL,
  `password` varchar(1000) DEFAULT NULL,
  `otp` varchar(1000) DEFAULT NULL,
  `blood_type` varchar(1000) DEFAULT NULL,
  `address` varchar(1000) DEFAULT NULL,
  `status` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;

/*Data for the table `donor` */

insert  into `donor`(`id`,`f_name`,`email`,`mobile`,`password`,`otp`,`blood_type`,`address`,`status`) values (3,'streamway','streamwaytechnologiespvtltd@gmail.com','09493040484','123','754660','A+','hyderabad','Verified'),(7,'kishan','gkvtechsolutions@gmail.com','1234567890','123','775570','A+','hyderabad','Verified');

/*Table structure for table `faq` */

DROP TABLE IF EXISTS `faq`;

CREATE TABLE `faq` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `question` longtext,
  `answer` longtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

/*Data for the table `faq` */

insert  into `faq`(`id`,`question`,`answer`) values (1,'hi','hi how are you'),(2,'good morning','very good morning have a nice day'),(3,'tell me usage of blood donation if i would done','Donated blood is crucial for saving lives in emergencies, surgeries, and medical treatments. It helps accident victims, surgery patients, and those with conditions like anemia, cancer, and blood disorders. Blood transfusions are vital for individuals undergoing chemotherapy, organ transplants, or suffering from severe blood loss. Your donation can provide life-saving support to those in critical need.');

/*Table structure for table `feedback` */

DROP TABLE IF EXISTS `feedback`;

CREATE TABLE `feedback` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hsp_id` varchar(1000) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `mobile` varchar(1000) DEFAULT NULL,
  `date_feed` varchar(100) DEFAULT NULL,
  `overall_service` varchar(100) DEFAULT NULL,
  `request_handling` varchar(100) DEFAULT NULL,
  `description` longtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

/*Data for the table `feedback` */

insert  into `feedback`(`id`,`hsp_id`,`email`,`mobile`,`date_feed`,`overall_service`,`request_handling`,`description`) values (1,'6','kishan@gmail.com','09493040484','2025-02-20','Very Poor','Good','good');

/*Table structure for table `hospital` */

DROP TABLE IF EXISTS `hospital`;

CREATE TABLE `hospital` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `contact` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `address` varchar(100) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  `status` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;

/*Data for the table `hospital` */

insert  into `hospital`(`id`,`name`,`contact`,`email`,`address`,`password`,`status`) values (5,'Apolo','1234567890','GKVTECHSOLUTIONS@gmail.com','hyderabad','GPEWUM','Authorized'),(6,'Gandhi','09493040484','streamwaytechnologiespvtltd@gmail.com','hyderabad','cNVCG7','Authorized'),(7,'KishanHsp','01234567890','kishan@gmail.com','hyderabad','4bD0gW','Authorized');

/*Table structure for table `patient_request` */

DROP TABLE IF EXISTS `patient_request`;

CREATE TABLE `patient_request` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hsp_id` varchar(1000) DEFAULT NULL,
  `b_group` varchar(1000) DEFAULT NULL,
  `p_name` varchar(1000) DEFAULT NULL,
  `contact` varchar(1000) DEFAULT NULL,
  `address` varchar(1000) DEFAULT NULL,
  `status` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

/*Data for the table `patient_request` */

insert  into `patient_request`(`id`,`hsp_id`,`b_group`,`p_name`,`contact`,`address`,`status`) values (2,'6','A+','patient','09493040484','hyderabad','Approved'),(3,'6','B+','patient2','1234567890','hyderabad','Rejected');

/*Table structure for table `total_units` */

DROP TABLE IF EXISTS `total_units`;

CREATE TABLE `total_units` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `blood_group` varchar(1000) DEFAULT NULL,
  `no_of_units` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

/*Data for the table `total_units` */

insert  into `total_units`(`id`,`blood_group`,`no_of_units`) values (1,'A ','18'),(2,'B+','45');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
