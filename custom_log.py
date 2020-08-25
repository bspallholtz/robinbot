#!/usr/bin/python
import datetime


class Custom_Logger:
    def write_log(self, level, message):
        now = str(datetime.datetime.now())
        message = now + " - " + str(message) + '\n'
        if level == 'INFO' or level == 'WARNING' or level == 'ERROR':
            log_file = 'info.log'
        elif level == 'DEBUG':
            log_file = 'debug.log'
        elif level == 'CRITICAL':
            log_file = 'critical.log'
        elif level == 'TRANSACTION':
            log_file = 'transaction.log'
        elif level == 'ANALYZE':
            log_file = 'analyze.log'
        else:
            log_file = 'debug.log'
        with open(log_file, 'a+') as f:
            f.write(message)
            f.close()
            return True
