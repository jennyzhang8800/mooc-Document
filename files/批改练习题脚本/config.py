# coding:utf8

import logging


class Config:
    # log config
    logger = {
        'filename': 'grade.log',
        'format': '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
        'encoding': 'utf8',
        'level': logging.DEBUG,
    }

    repopath = '/home/jennyzhang/answer'

    inteval = {
        'single_answer': 3600 * 24,  # one day
        'true_false': 3600 * 24,  # one day
        'multi_answer': 3600 * 24,  # one day
    }
