CREATE TABLE IF NOT EXISTS `user` (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(255) NOT NULL UNIQUE,
  email VARCHAR(255) NOT NULL UNIQUE,
  hashed_password VARCHAR(255) NOT NULL,
  role ENUM('user', 'customer', 'admin', 'vendor') NOT NULL DEFAULT 'user',
  totp_secret VARCHAR(255),

  INDEX idx_user_username (username),
  INDEX idx_user_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ALTER TABLE user
-- MODIFY COLUMN role ENUM('user', 'admin', 'vendor') NOT NULL DEFAULT 'user';