import logging

class Logger():
    def __init__(self, logname, loglevel, logger):
        '''
           指定保存日志的文件路径，日志级别，以及调用文件
           将日志存入到指定的文件中
        '''
        format_dict = {
            1 : logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
            2 : logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
            3 : logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
            4 : logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'),
            5 : logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            }
        # 创建一个logger
        self.logger = logging.getLogger(logger)
        self.logger.setLevel(logging.DEBUG)
        
         # 创建一个handler，用于写入日志文件
        fh = logging.FileHandler('log\\'+logname,mode='w',encoding='UTF-8')
        fh.setLevel(logging.DEBUG)
         
         # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
         
        # 定义handler的输出格式
        #formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        formatter = format_dict[int(loglevel)]
        fh.setFormatter(formatter)
        
        # 给logger添加handler
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)

    def getlog(self):
        return self.logger


