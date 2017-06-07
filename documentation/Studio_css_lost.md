Studio CSS样式缺失问题。

## 问题描述：
http://cherry.cs.tsinghua.edu.cn:18010 进入Studio页面，但是Studio页面CSS样式缺失。如下图：

![image](https://github.com/jennyzhang8800/mooc-Document/blob/master/pictures/studio_css_lost.png)

通过F12调试，可以发现很多CSS文件和js加载时出现404错误。如下图：

![image](https://github.com/jennyzhang8800/mooc-Document/blob/master/pictures/studio_css_lost_F12.png)

## 解决方法：

通过F12调试时可以看到，Studio加载的静态css和js都是在http://cherry.cs.tsinghua.edu.cn:18010/static/f3089e9eec/这个目录下的。

但是我到edx后台/edx/var/edxapp/staticfiles下面没有找到“f3089e9eec”这个目录。

我找到有f3089e9这个目录，我把f3089e9这个目录下所有的内容都复制到f3089e9eec这个新建的目录下。Studio就可以正常显示了。

![image](https://github.com/jennyzhang8800/mooc-Document/blob/master/pictures/studio_ok.png)
