# mooc-Document
> 该仓库存放的是与MOOC系统有关的所有文档

<hr/>

**目录**
* [机器列表](#framework)
* [MOOC平台的布署文档及配置文件备份](#mooc)
* [IBM到实验室MOOC平台的数据迁移](#migration)
* [相关链接](#link)
 + [张禹在IBM上的MOOC平台布署](#IBM)
 + [张燕妮的博客](#blog)
 + [张燕妮github](#zyni)
 + [张禹github](#zyu)
 + [罗富文github](#lfwen)
<hr/>

<h2 id="framework">1. 机器列表</h2>

| 名 称  | IP   | 访问链接 |
| :-------------: |:-------------:| :-----:|
| edx (SP)     | 192.168.1.135 | [http://cherry.cs.tsinghua.edu.cn](http://cherry.cs.tsinghua.edu.cn) |
| gitlab (SP)     | 192.168.1.136 | [http://apple.cs.tsinghua.edu.cn](http://apple.cs.tsinghua.edu.cn) |
| shibboleth(IDP)      | 192.168.1.137 |无 |
| LDAP      | 192.168.1.138 |[https://166.111.68.101/mooc/ldapadmin/](https://166.111.68.101/mooc/ldapadmin/) |


<h2 id="mooc">2. MOOC平台的布署文档及配置文件备份</h2>

+ **MOOC平台的布署文档及配置文件备份**：

   涉及的内容有：gitlab的安装，Open edX的安装，利用Shibboleth实现以gitlab和Open edX作为两个SP实现SSO（单点登录）：[点此查看](https://github.com/jennyzhang8800/os_platform)
   
   
<h2 id="migration">3. IBM到实验室MOOC平台的数据迁移</h2>

+ [IBM-data-migration.md](https://github.com/jennyzhang8800/mooc-Document/blob/master/IBM-data-migration.md): 该文档描述的是把布署于IBM的MOOC平台数据迁移到现有实验室MOOC平台的方法


<h2 id="link">4. 相关链接</h2>

+ <h4 id="IBM">张禹在IBM上的MOOC平台布署：</h4>[点此查看](https://github.com/xyongcn/online_experiment_platform)

+ <h4 id="blog">张燕妮的博客：</h4>一些布署的记录，有部分内容己合并到“MOOC平台的布署文档及配置文件备份”

 + [edx有关](http://blog.csdn.net/jenyzhang/article/category/3141095)
 + [shibboleth有关](http://blog.csdn.net/jenyzhang/article/category/6337293)
 
+ <h4 id="zyni">张燕妮github：</h4>[点此查看](https://github.com/jennyzhang8800/) 以mooc开头的仓库

+ <h4 id="zyu">张禹github：</h4>[点此查看](https://github.com/rainymoon911/)

+ <h4 id="lfwen">罗富文github：</h4>[点此查看](https://github.com/Heaven1881/) 以mooc开头的仓库

