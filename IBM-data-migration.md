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

1. Mongo数据迁移

2. xblock迁移

   xblock无法迁移，需要重新安装。下面是MOOC平台中XBlcok安装的帮助：
   
 * [Piazza](https://github.com/jennyzhang8800/mooc-PiazzaXBlock)
  
 * [练习题](https://github.com/jennyzhang8800/mooc-Quizzes2XBlock)
 * [题库编辑](https://github.com/jennyzhang8800/mooc-ExerciseMdf)
 * [代码浏览与编辑](https://github.com/xyongcn/online_experiment_platform/tree/master/XBlock)
    
