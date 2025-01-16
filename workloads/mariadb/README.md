# Installing and Configuring MariaDB on Ubuntu 22.04

This guide provides comprehensive steps to install, configure, and optionally remove MariaDB from the following distros

- Ubuntu 22.04  
- Ubuntu 24.04  
- Rhel9  
- Centos9  

---

## Prerequisites

- Network Access
- User with root or sudo privileges.

---

## Steps to Install MariaDB
- apt/apt-get is the default Package Manager for Debian and Ubuntu 
- dnf is the default package manager for rhel9 and centos

```bash
# Ensure the package list is up to date
sudo ${PKG_MANAGER} update

# Install MariaDB server and client packages:
sudo ${PKG_MANAGER} install -y mariadb-server 
# Owner should be mysql, and permissions should be set for MARIADB_RUNTIME_FOLDER and MARIADB_LIB_FOLDER - these might change based on distros, so please refer to the Make file
sudo chmod -R 777 ${MARIADB_RUNTIME_FOLDER}
sudo chmod -R 777 ${MARIADB_LIB_FOLDER}
sudo chmod -R msql:mysql ${MARIADB_RUNTIME_FOLDER}
sudo chmod -R mysql:mysql ${MARIADB_LIB_FOLDER}

```

---
## Starting a Mariadb Server
We need to use --skip-grant-tables to skip the password verification step in mariadb
```
mysqld --skip-grant-tables --bind-address 127.0.0.1
```
---

---
## Starting a Mariadb Client Instance
In a seperate terminal instance run the following command
```
mysql -h 127.0.0.1 
```
---

---

## Steps to Completely Remove MariaDB

```bash
# Stop the MariaDB Service
pkill -9 mysql
# Uninstall MariaDB Packages
sudo ${PKG_MANAGER} remove --purge -y mariadb-server
sudo ${PKG_MANAGER} remove --purge -y mariadb-client
sudo ${PKG_MANAGER} autoremove --purge -y
# Delete Configuration and Data Files
sudo rm -rf /etc/mysql /var/lib/mysql /var/lib/mysql-files /var/log/mysql /var/log/mariadb /var/cache/mysql 
```