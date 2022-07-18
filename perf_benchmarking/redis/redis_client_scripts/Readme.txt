############### How to prepare client ICL system ################

Client build for Redis:
    # Install Redis
        $ wget http://download.redis.io/releases/redis-6.0.6.tar.gz
        $ tar xzf redis-6.0.6.tar.gz
        $ cd redis-6.0.6
        $ make
        $ make test
    
    Setup sysctl
        $ add "net.core.somaxconn=1024" to /etc/sysctl.conf
        $ add "vm.overcommit_memory=1" to /etc/sysctl.conf
        
    # X: Disable THP (Transparent Huge Pages)
        $ sudo apt-get install hugepages
        $ sudo hugeadm --thp-never
        $ cat /sys/kernel/mm/transparent_hugepage/enabled
        $ echo '#!/bin/bash' | sudo tee /etc/rc.local
        $ echo 'hugeadm --thp-never' | sudo tee -a /etc/rc.local
        $ echo 'exit 0' | sudo tee -a /etc/rc.local
        $ sudo chmod +x /etc/rc.local
        Read more: 
            https://linuxmedium.com/how-to-enable-etc-rc-local-with-systemd-on-ubuntu-20-04/
            https://docs.mongodb.com/manual/tutorial/transparent-huge-pages/
            
        $ vim /etc/systemd/system/rc-local.service
            [Unit]
             Description=/etc/rc.local Compatibility
             ConditionPathExists=/etc/rc.local

            [Service]
             Type=forking
             ExecStart=/etc/rc.local start
             TimeoutSec=0
             StandardOutput=tty
             RemainAfterExit=yes
             SysVStartPriority=99

            [Install]
             WantedBy=multi-user.target
        
        $ systemctl start rc-local
        $ systemctl enable rc-local
        
    # Install memtier_benchmark
        $ git clone https://github.com/RedisLabs/memtier_benchmark.git
        $ cd memtier_benchmark
        $ sudo apt-get install -y build-essential autoconf automake libpcre3-dev libevent-dev pkg-config zlib1g-dev libssl-dev
        $ autoreconf -ivf
        $ ./configure
        $ make
        $ sudo make install

    # Data Collection
     1. Copy redis_client_scripts.zip in your ICL client system and unzip it.
     2. Check start_benchamark.sh once and run "./start_benchamark.sh"