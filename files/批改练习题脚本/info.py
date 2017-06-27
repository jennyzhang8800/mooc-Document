# coding:utf8
# author:winton

import logging
import re
import argparse
import os
import codecs
import json

from config import Config


class Info:
    '''
    负责自动对选择题评分
    '''
    def __init__(self, config, overwritedInteval=None):
        self.config = config
        self.info = {}

        loggingInfo = config.logger
        logging.basicConfig(
            level=loggingInfo['level'],
            format=loggingInfo['format'],
            # filename=loggingInfo['filename'],
            filename='info.log',
            encoding=loggingInfo['encoding']
        )

    def loadJsonFromFile(self, filepath):
        if not os.path.exists(filepath):
            logging.warning('loading a file not exists [path=%s]' % filepath)
            return None
        f = codecs.open(filepath, encoding='utf8')
        jsonStr = f.read()
        f.close()
        if jsonStr:
            return json.loads(jsonStr)
        else:
            logging.warning('read None content')
            return None

    def saveJsonToFile(self, filepath, event):
        f = codecs.open(filepath, 'w', 'utf8')
        try:
            f.write(json.dumps(event, ensure_ascii=False, indent=4, separators=(',', ':')))
        finally:
            f.close()

    def stat(self):
        for parent, dirnames, filenames in os.walk(self.config.repopath):
            for filename in filenames:
                filepath = os.path.join(parent, filename)
                m = re.search('([0-9a-z]{2})/([^/]+)/([0-9]{1,4})/[0-9]{1,4}.json$', filepath)
                if m:
                    answerInfo = m.groups()
                    qno = int(answerInfo[2])
                    if qno in [1489, 1490, 1491]:
                        data = self.loadJsonFromFile(filepath)
                        self.statInfo(data, qno)
        # TODO 保存数据
        for email in self.info:
            info = self.info[email]
            self.saveJsonToFile(os.path.join(self.config.repopath, 'tool/result/%s.json' % email), info)

    def statInfo(self, data, qno):
        student = data['student']
        email = student['email']
        if email in self.info:
            studentInfo = self.info[email]
        else:
            self.info[email] = {
                'edxEmail': student['email'],
                'edxUsername': student['username']
            }
            studentInfo = self.info[email]
        # 根据题号收集信息
        answer = data['answer'][0]['answer']
        if qno == 1489:
            # 真实姓名
            studentInfo['realName'] = answer
        elif qno == 1490:
            # 学号或学堂在线注册邮箱
            studentInfo['id'] = answer
        elif qno == 1491:
            # gitlab库目录
            studentInfo['gitRepoUrl'] = answer
            m = re.search('([(172\.16\.13\.236)(github\.com)]+)[/:]([^/]+)', answer)
            if m:
                groups = m.groups()
                studentInfo['gitHost'] = 'gitlab' if groups[0] == '172.16.13.236' else 'github'
                studentInfo['gitUsername'] = groups[1]


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description='grade student for teacher/answer')
    args = ap.parse_args()

    test = Info(Config)
    test.stat()
