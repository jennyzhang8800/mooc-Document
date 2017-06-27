# coding:utf8
# author:winton

import logging
import re
import argparse
import os
import codecs
import json

from config import Config


class AnswerGrader:
    '''
    负责自动对选择题评分
    '''
    def __init__(self, config, overwritedInteval=None):
        self.config = config
        self.graded = 0
        # if overwritedInteval:
        #     self.intevalSetting = {
        #         'single_answer': int(overwritedInteval),
        #         'true_false': int(overwritedInteval),
        #         'multi_answer': int(overwritedInteval),
        #     }
        # else:
        #     self.intevalSetting = self.config.interval

        loggingInfo = config.logger
        logging.basicConfig(
            level=loggingInfo['level'],
            format=loggingInfo['format'],
            filename=loggingInfo['filename'],
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

    def grade(self, student=None, question=None, force=False, verbose=False):
        for parent, dirnames, filenames in os.walk(self.config.repopath):
            for filename in filenames:
                filepath = os.path.join(parent, filename)
                m = re.search('([0-9a-z]{2})/([^/]+)/([0-9]{1,4})/[0-9]{1,4}.json$', filepath)
                if m:
                    try:
                        answerInfo = m.groups()
                        gradedPath = '%(emailhash)s/%(username)s/%(qno)d/%(qno)d.graded.json' % {
                            'emailhash': answerInfo[0],
                            'username': answerInfo[1],
                            'qno': int(answerInfo[2])
                        }
                        if student and student != answerInfo[1]:
                            continue
                        if question and question != answerInfo[2]:
                            continue
                        if not force and os.path.exists(gradedPath):
                            if verbose:
                                logging.warning('answerInfo has been graded [path=%s]' % filepath)
                            continue
                        # 读取文件内部json，并判断内容是否需要批改
                        self.gradeAnswerFile(filepath, gradedPath, verbose)
                    except:
                        logging.exception(filename)
        logging.info('grading finish,  %d answers graded' % self.graded)

    def gradeAnswerFile(self, answerPath, gradedPath, verbose=False):
        answerInfo = self.loadJsonFromFile(answerPath)
        questionType = answerInfo['question']['type']
        # 如果不是选择题，则取消批改
        if questionType not in ['single_answer', 'multi_answer', 'true_false']:
            if verbose:
                logging.info('skip answer [type=%s]' % questionType)
            return
        # TODO 如果第一次回答的时间还没有超过指定的间隔，则不批改
        # tm = time.strptime(timeStr, '%Y-%m-%d:%H:%M:%S')
        # tms = time.mktime(tm)
        # t = datetime.timedelta(seconds=self.intevalSetting[questionType]) + datetime.datetime.now()
        # time.mktime(t.timetuple())
        # if self.intevalSetting[questionType]
        studentAnswer = answerInfo['answer'][-1]['answer']
        standardAnswer = answerInfo['question']['answer']
        gradedInfo = {
            'q_number': answerInfo['question']['q_number'],
            'student': answerInfo['student'],
            'graded_by': 'system',
            'student_answer': studentAnswer,
            'standard_answer': standardAnswer,
            'score': 1.0 if studentAnswer == standardAnswer else 0,
        }
        if os.path.exists(gradedPath):
            logging.info('force to grade answer [path=%s]' % answerPath)
        else:
            logging.info('grading answer [path=%s]' % answerPath)
        self.graded += 1
        self.saveJsonToFile(os.path.join(self.config.repopath, gradedPath), gradedInfo)


if __name__ == '__main__':
    ap = argparse.ArgumentParser(description='grade student for teacher/answer')
    ap.add_argument('-s', '--student', nargs='?', help='grade special student\'s answer, if not setted, system will grade all')
    ap.add_argument('-q', '--question', nargs='?', help='grade special question\'s answer, if not setted, system will grade all')
    ap.add_argument('-i', '--interval', nargs='?', help='''
        set interval time for grading, only the answer before this time will be graded, default setting is in config.py''')
    ap.add_argument('-f', '--force', action='store_true', help='force to regrade answer')
    args = ap.parse_args()

    grader = AnswerGrader(Config)
    if args.student or args.question:
        grader.grade(student=args.student, question=args.question, force=args.force, verbose=True)
    else:
        grader.grade(force=args.force)
