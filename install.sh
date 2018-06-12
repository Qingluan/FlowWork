#!/bin/bash

SYS=$(uname)

if [[ $SYS == "Darwin" ]];then
	cd  WebDriverExecutor/ && unzip chromedriver_mac64.zip && cp -v  chromedriver /usr/local/bin/;
elif [[ $SYS == "Linux" ]];then
	cd  WebDriverExecutor/ && unzip chromedriver_linux64.zip && cp -v  chromedriver /usr/local/bin/;
fi

if [ $? -eq 0 ];then
	echo "chromedriver install ok";
fi