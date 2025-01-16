ARCH_LIBDIR ?= /lib/$(shell $(CC) -dumpmachine)
UID ?= $(shell id -u)
GID ?= $(shell id -g)
TIMEOUT = 60

# Detect the Package Manager
ifneq ($(shell command -v apt-get),)
  PKG_MANAGER = apt-get
  MARIADB_RUNTIME_FOLDER = /var/run/mysqld
  MARIADB_LIB_FOLDER = /var/lib/mysql
else ifneq ($(shell command -v dnf),)
  PKG_MANAGER = dnf
  MARIADB_RUNTIME_FOLDER = /var/run/mariadb
  MARIADB_LIB_FOLDER = /var/lib/mysql
else
  $(error No supported package manager found)
endif

# Set log level to DEBUG if DEBUG=1 is given in cmdline
ifeq ($(DEBUG),1)
GRAMINE_LOG_LEVEL = debug
else
GRAMINE_LOG_LEVEL = error
endif

# Toggle between sgx and direct, if SGX=1 is given in cmdline
ifeq ($(SGX),)
GRAMINE = gramine-direct
else
GRAMINE = gramine-sgx
endif

.PHONY: all
all: mysqld.manifest
ifeq ($(SGX),1)
all: mysqld.manifest.sgx mysqld.sig
endif

# Gramine utility for generating the manifests
mysqld.manifest: mysqld.manifest.template
	gramine-manifest \
        -Dlog_level=$(GRAMINE_LOG_LEVEL) \
        -Darch_libdir=$(ARCH_LIBDIR) \
        -Duid=$(UID) \
        -Dgid=$(GID) \
	-Dentrypoint=/usr/sbin/mysqld \
	$< >$@

# Make on Ubuntu <= 20.04 doesn't support "Rules with Grouped Targets" (`&:`),
# for details on this workaround see
# https://github.com/gramineproject/gramine/blob/e8735ea06c/CI-Examples/helloworld/Makefile
mysqld.manifest.sgx mysqld.sig: sgx_sign
        @:

.INTERMEDIATE: sgx_sign
sgx_sign: mysqld.manifest
	gramine-sgx-sign \
	--manifest $< \
	--output $<.sgx

.PHONY: install-mariadb
install-mariadb:
	sudo -E $(PKG_MANAGER) install -y mariadb-server
	-sudo mkdir -p /var/run/mysqld
	-sudo mkdir -p /var/lib/mysql

# This is only for Testing locally
.PHONY: remove-mariadb
remove-mariadb:
	-sudo pkill -9 mysqld
	-sudo apt remove --purge -y mariadb-server
	-sudo apt autoremove --purge -y
	-sudo rm -rf /etc/mysql /var/lib/mysql /var/log/mysql /var/log/mariadb /var/cache/mysql

.PHONY: clean
clean:
	$(RM) *.sig *.manifest.sgx *.manifest *_output
	$(RM) -r /tmp/mysql-data

# This target is for testing mariadb with gramine-direct and gramine-sgx
.PHONY: test-gramine
test-gramine:
	sudo chmod -R 777 $(MARIADB_RUNTIME_FOLDER)
	sudo chmod -R 777 $(MARIADB_LIB_FOLDER)
	sudo chown -R mysql:mysql $(MARIADB_LIB_FOLDER)
	sudo chown -R mysql:mysql $(MARIADB_RUNTIME_FOLDER)

	-sudo pkill -9 mysqld

	$(GRAMINE) mysqld --skip-grant-tables --bind-address=127.0.0.1 > server_output 2>&1 &
	echo "Running MariaDB Server"

	echo "Running MariaDB Client after $(TIMEOUT) seconds"
	sleep $(TIMEOUT) && cat server_output && sudo mysql -h 127.0.0.1 --batch -N -e "SELECT 'SUCCESS';" > client_output
	-sudo pkill -9 mysqld
