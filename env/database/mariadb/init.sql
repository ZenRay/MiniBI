-- Optional initialization SQL run on first container start
-- This file is copied to /docker-entrypoint-initdb.d/ and will be executed
-- by the official MariaDB entrypoint on an empty data directory.

CREATE DATABASE IF NOT EXISTS `superset` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'superset'@'%' IDENTIFIED BY 'superset';
GRANT ALL PRIVILEGES ON `superset`.* TO 'superset'@'%';
FLUSH PRIVILEGES;
