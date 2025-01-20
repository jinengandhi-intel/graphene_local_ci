ARCH_LIBDIR ?= /lib/$(shell $(CC) -dumpmachine)
UID ?= $(shell id -u)
GID ?= $(shell id -g)

ifeq ($(DEBUG),1)
GRAMINE_LOG_LEVEL = debug
else
GRAMINE_LOG_LEVEL = error
endif

.PHONY: all
all: mysqld.manifest
ifeq ($(SGX),1)
all: mysqld.manifest.sgx mysqld.sig
endif

mysqld.manifest: mysqld.manifest.template
	gramine-manifest \
	-Dlog_level=$(GRAMINE_LOG_LEVEL) \
	-Darch_libdir=$(ARCH_LIBDIR) \
	-Duid=$(UID) \
	-Dgid=$(GID) \
	-Dentrypoint=$(realpath $(shell sh -c "command -v mysqld")) \
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


ifeq ($(SGX),)
GRAMINE = gramine-direct
else
GRAMINE = gramine-sgx
endif

.PHONY: check
check: all
	rm -rf OUTPUT
	mysqld --initialize-insecure --datadir=/tmp/mysql-data 2>&1 | tee OUTPUT
	@grep -q '\[Server\] root@localhost is created with an empty password !' OUTPUT && echo [ "Success" ]
	sleep 5s && ($(GRAMINE) mysqld --datadir /tmp/mysql-data &)

.PHONY: install-dependencies
install-dependencies:
	sudo -E apt-get install -y mysql-server
	sudo -E apt-get install -y sysbench

.PHONY: privileges
privileges:
	sudo sed -i "s|^\(log_error.*\)|#\1|g" /etc/mysql/mysql.conf.d/mysqld.cnf
	-sudo systemctl stop mysql.service
	sudo mkdir -p /var/run/mysqld
	sudo mkdir -p /var/lib/mysql-files
	sudo chown -R $$USER:$$USER /var/run/mysqld
	sudo chown -R $$USER:$$USER /var/lib/mysql-files
	sudo chmod 777 /var/run/mysqld
	sudo chmod 777 /var/lib/mysql-files

.PHONY: uninstall-mysql
uninstall-mysql:
	rm -rf /var/run/mysqld /tmp/mysql-data /var/lib/mysql-files *.sig *.manifest.sgx *.manifest

.PHONY: conncheck
conncheck:
	rm -rf CREATE_RESULT RUN_RESULT DELETE_RESULT
	sudo -E mysqladmin -h 127.0.0.1 -P 3306 create sbtest
	sysbench --db-driver=mysql --mysql-host=127.0.0.1 --mysql-port=3306 --mysql-user=root --mysql-db=sbtest --time=20 --report-interval=5 oltp_read_write --tables=2 --table_size=100000 --threads=32 prepare 2>&1 | tee CREATE_RESULT
	sysbench --db-driver=mysql --mysql-host=127.0.0.1 --mysql-port=3306 --mysql-user=root --mysql-db=sbtest --time=20 --report-interval=5 oltp_read_write --tables=2 --table_size=100000 --threads=32 run 2>&1 | tee RUN_RESULT
	sysbench --db-driver=mysql --mysql-host=127.0.0.1 --mysql-port=3306 --mysql-user=root --mysql-db=sbtest --time=20 --report-interval=5 oltp_read_write --tables=2 --table_size=100000 --threads=32 cleanup 2>&1 | tee DELETE_RESULT

.PHONY: clean
clean:
	$(RM) *.sig *.manifest.sgx *.manifest
	$(RM) -rf /tmp/mysql-data

.PHONY: distclean
distclean: clean
