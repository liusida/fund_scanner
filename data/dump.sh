#!/bin/sh
/usr/bin/mysqldump --quick stock_index -u root -p | /bin/gzip > ./stock_index.gz
/usr/bin/mysqldump --quick funds -u root -p | /bin/gzip > ./funds.gz

