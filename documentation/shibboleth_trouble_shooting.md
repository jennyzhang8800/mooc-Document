>从Open edX点击"shibboleth登录"，跳转到Shibboleth页面时出错的解决方法

### 1. 查看Shibboleth日志
 ```
 sudo vim /opt/shibboleth-idp/logs/idp-process.log  
 ```
 
### 2. 重启apache 和tomcat

```
sudo  /etc/init.d/apache2 restart    
sudo  /etc/init.d/tomcat7 restart  
```

这里重启tomcat7失败，提示/usr/lib/jvm/java-7-openjdk-amd64 (no such file)
原因是JAVA_HOME路径没有配置正确。
输入下面的命令修改：
```
sudo vim /etc/enviroment
```
把JAVA_HOME改为正确的路径：
```
PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games"
JAVA_HOME="/usr/lib/jvm/java-7-oracle"
```
重新重启tomcat7
```
sudo  /etc/init.d/tomcat7 restart 
```
可以看到tomcat7重启成功

### 3. 重启机器：
```
sudo reboot
```
有时候问题解决不了，reboot之后就好了，很神奇。
