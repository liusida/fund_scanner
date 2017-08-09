#!/bin/sh
/bin/gunzip < funds.gz | /usr/bin/mysql funds -u root -p
/bin/gunzip < stock_index.gz | /usr/bin/mysql stock_index -u root -p
