# 从IBM数据迁移至实验室MOOC平台
##1. gitlab数据迁移
数据迁移其实是先在机器A进行备份，然后把备份拷到机器B, 最后在机器B导入备份。

| 机器 | IP | 位置 |
| :-------: | :-------: | :-----:|
|机器A|172.16.13.236|IBM |
|机器B|192.168.1.136|实验室内部|
**注意：**机器A和机器B的gitlab版本号必须一样！

+ 1. 先在机器A 对 gitlab进行备份
```
sudo gitlab-rake gitlab:backup:create
```
   默认备份文件储存在   /var/opt/gitlab/backups/1478884176_gitlab_backup.tar 

+ 2. 把备份拷贝到机器B  /var/opt/gitlab/backups/ 目录下

在机器B输入下面的命令以完成备份从机器A远程拷贝到机器B：
```
scp -p opuser@172.16.13.236:/git-backup.temp/1478884176_gitlab_backup.tar  /var/opt/gitlab/backups/  
```
注意：由于备份文件有14G，因此实际拷贝时，先对原始备份进行切片(split)，分片拷贝到机器B后，再把分片数据合并(cat)。下面是切片与合并的命令：
```
sudo split -b 512m 1478884176_gitlab_backup.tar -d -a 3 gitlab_backup
```
```
sudo cat gitlab* >1478884176_gitlab_backup.tar  
```
+ 3. 在机器B进行数据的恢复

```
sudo gitlab-ctl stop unicorn
sudo gitlab-ctl stop sidekiq
sudo gitlab-rake gitlab:backup:restore BACKUP=1478884176   
sudo gitlab-ctl start
sudo gitlab-rake gitlab:check SANITIZE=true
```

+ 4. 重新加载gitlab

```
sudo gitlab-ctl reconfigure
```

##2. edx数据迁移

+ 1.Mongo数据迁移

 * (1)先在机器A（IBM edx机器）进行mongo数据库的备份
  
```
 mongodump -h dbhost -d dbname -o dbdirectory
```
  
```
-h：MongDB所在服务器地址，例如：127.0.0.1，当然也可以指定端口号：127.0.0.1:27017
-d：需要备份的数据库实例，例如：test
-o：备份的数据存放位置，例如：c:\data\dump，当然该目录需要提前建立，在备份完成后，系统自动在dump目录下建立一个test目录，这个目录里面存放该数据库实例的备份数据。

```

 * (2)把备份数据拷贝到机器B（实验室 edx机器）
  
 * (3)恢复数据
 
```
  mongorestore -h dbhost -d dbname --directoryperdb dbdirectory
```

```
  -h： MongoDB所在服务器地址
  -d：需要恢复的数据库实例，例如：test，当然这个名称也可以和备份时候的不一样，比如test2
  --directoryperdb：备份数据所在位置，例如：c:\data\dump\test，这里为什么要多加一个test，而不是备份时候的dump，读者自己查看提示吧！
  --drop：恢复的时候，先删除当前数据，然后恢复备份的数据。就是说，恢复后，备份后添加修改的数据都会被删除，慎用哦！

```
+ 2.xblock迁移

   xblock无法迁移，需要重新安装。下面是MOOC平台中XBlcok安装的帮助：
   
 * [Piazza](https://github.com/jennyzhang8800/mooc-PiazzaXBlock)
  
 * [练习题](https://github.com/jennyzhang8800/mooc-Quizzes2XBlock)
 * [题库编辑](https://github.com/jennyzhang8800/mooc-ExerciseMdf)
 * [代码浏览与编辑](https://github.com/xyongcn/online_experiment_platform/tree/master/XBlock)
 * [练习题完成情况统计](https://github.com/jennyzhang8800/mooc-StatisticXblock)
 
 ### 数据备份
 
 IBM edx机器的数据备份位于实验室edx机器（IP：192.168.1.135）的``/home/zyni/IBM_backup``目录下
 
 |  IBM edx原路径 | 实验室edx备份名称   | 实验室edx备份名称 |
| :-------------: |:-------------:| :-----:|
| /edx/app/nginx     |edx-app-nginx.tar.gz |
| /Lams    | lams.tar.gz | 
| /home/lfwen      | git.tar.gz |
| /home/lfwen  |lfwen.tar.gz |
| /home/zyu | zyu.tar.gz |
| /home/opuser | opuser.tar.gz |
| /var/www/zyni/script | var-www-zyni-script.tar.gz |
| /edx/app/edxapp/venvs/edxapp/lib/python2.7/site-packages | site-package-backup.tar.gz |
