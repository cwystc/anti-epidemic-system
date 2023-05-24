-- MySQL Script generated by MySQL Workbench
-- Mon May 22 17:43:18 2023
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema anti-epidemic db
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema anti-epidemic db
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `anti-epidemic db` DEFAULT CHARACTER SET utf8 ;
USE `anti-epidemic db` ;

-- -----------------------------------------------------
-- Table `anti-epidemic db`.`person`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `anti-epidemic db`.`person` (
  `ID_number` INT NOT NULL AUTO_INCREMENT,
  `person_name` VARCHAR(45) NULL,
  `advisor` INT NOT NULL,
  PRIMARY KEY (`ID_number`),
  INDEX `fk_person_person_idx` (`advisor` ASC) VISIBLE,
  CONSTRAINT `fk_person_person`
    FOREIGN KEY (`advisor`)
    REFERENCES `anti-epidemic db`.`person` (`ID_number`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `anti-epidemic db`.`testing sites`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `anti-epidemic db`.`testing sites` (
  `test_site_number` INT NOT NULL AUTO_INCREMENT,
  `test_site_name` VARCHAR(45) NULL,
  PRIMARY KEY (`test_site_number`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `anti-epidemic db`.`test record`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `anti-epidemic db`.`test record` (
  `test_number` INT NOT NULL AUTO_INCREMENT,
  `test_result` BIT(1) NULL,
  `test_time` DATETIME NULL,
  `person_tested` INT NOT NULL,
  `test_location` INT NOT NULL,
  PRIMARY KEY (`test_number`),
  INDEX `fk_test record_person1_idx` (`person_tested` ASC) VISIBLE,
  INDEX `fk_test record_testing sites1_idx` (`test_location` ASC) VISIBLE,
  CONSTRAINT `fk_test record_person1`
    FOREIGN KEY (`person_tested`)
    REFERENCES `anti-epidemic db`.`person` (`ID_number`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_test record_testing sites1`
    FOREIGN KEY (`test_location`)
    REFERENCES `anti-epidemic db`.`testing sites` (`test_site_number`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `anti-epidemic db`.`location`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `anti-epidemic db`.`location` (
  `location_number` INT NOT NULL AUTO_INCREMENT,
  `location_name` VARCHAR(45) NULL,
  `risk_level` VARCHAR(10) NULL,
  PRIMARY KEY (`location_number`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `anti-epidemic db`.`travel record`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `anti-epidemic db`.`travel record` (
  `travel_number` INT NOT NULL AUTO_INCREMENT,
  `traveler` INT NOT NULL,
  `travel_location` INT NOT NULL,
  PRIMARY KEY (`travel_number`),
  INDEX `fk_travel record_person1_idx` (`traveler` ASC) VISIBLE,
  INDEX `fk_travel record_location1_idx` (`travel_location` ASC) VISIBLE,
  CONSTRAINT `fk_travel record_person1`
    FOREIGN KEY (`traveler`)
    REFERENCES `anti-epidemic db`.`person` (`ID_number`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_travel record_location1`
    FOREIGN KEY (`travel_location`)
    REFERENCES `anti-epidemic db`.`location` (`location_number`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;