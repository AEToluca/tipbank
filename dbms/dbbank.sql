show databases;
CREATE DATABASE tipbank;
use tipbank;

CREATE TABLE ticket (
    check_id INT AUTO_INCREMENT PRIMARY KEY,
    shift_id INT NOT NULL,
    
    party_size INT NOT NULL,
    
    bill_before_tip DECIMAL(10,2) NOT NULL,
    tip_amount DECIMAL(10,2) NOT NULL,
    
    tip_type ENUM('CR','UP','CS') NOT NULL,
    split_type ENUM('S','T') NOT NULL,
    
    FOREIGN KEY (shift_id) REFERENCES shifts(shift_id)
);
DROP TABLE ticket;
SELECT * FROM ticket;
DELETE FROM ticket;

CREATE TABLE shifts (
    shift_id INT AUTO_INCREMENT PRIMARY KEY,
    shift_date DATE NOT NULL,
    period ENUM('AM', 'PM') NOT NULL
);
