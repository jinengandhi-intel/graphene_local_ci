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
	$(GRAMINE) mysqld --initialize --datadir /tmp/mysql-data 2>&1 | tee OUTPUT
	@grep -q '\[Server\] A temporary password is generated for' OUTPUT && echo [ "Success 1/2" ]
	sudo mysql -u root --skip-password -e 'SELECT DATABASE();' 2>&1 | tee OUTPUT1
	@grep -q 'DATABASE()' OUTPUT1 && grep -q 'NULL' OUTPUT1 && echo "Success 2/2"

.PHONY: run-native
run-native: all
	mysqld --initialize --datadir /tmp/mysql-data 2>&1 | tee OUTPUT
	@grep -q '\[Server\] A temporary password is generated for' OUTPUT && echo [ "Success 1/2" ]
	sudo mysql -u root --skip-password -e 'SELECT DATABASE();' 2>&1 | tee OUTPUT1
	@grep -q 'DATABASE()' OUTPUT1 && grep -q 'NULL' OUTPUT1 && echo [ "Success 2/2" ]

.PHONY: install-dependencies
install-dependencies:
	sudo apt install -y mysql-server
	sudo sed -i "s|^\(log_error.*\)|#\1|g" /etc/mysql/mysql.conf.d/mysqld.cnf
	sudo systemctl stop mysql.service
	sudo mkdir -p /var/run/mysqld
	sudo chown -R $$USER:$$USER /var/run/mysqld
	sudo chown -R $$USER:$$USER /var/lib/mysql-files
	sudo /etc/init.d/mysql start

.PHONY: clean
clean:
	$(RM) *.sig *.manifest.sgx *.manifest
	$(RM) -r /tmp/mysql-data

.PHONY: distclean
distclean: clean
