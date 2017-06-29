罗富文的选择题批改脚本。

【使用方法】

1. 先clone teacher/answer.git到本地
2. 进入到tool目录
3. 修改conf.py中的repopath为answer仓库的实际地址
4. 运行grade.py批改选择题
5. git push 同步仓库

[罗富文记录的说明文档](https://github.com/Heaven1881/mooc-document/blob/master/%E5%9C%A8%E7%BA%BF%E7%BB%83%E4%B9%A0%E7%9A%84%E6%89%8B%E5%8A%A8%E6%89%B9%E6%94%B9%E6%96%B9%E6%B3%95.md)

更正“罗富文记录的说明文档”中的一个错误

错误为：

使用-s参数指定学生的email，以下命令只会批改email为test@test.com的学生的回答
```
$ python grade.py -s test@test.com
```

更正为：

使用-s参数指定学生的用户名，以下命令只会批改用户名为s0712的学生的回答
```
$ python grade.py -s s0712
```
上述用户名"s0712",可以由edx中的 
```
student = self.runtime.get_real_user(self.runtime.anonymous_student_id)）
student.username
```
获得
