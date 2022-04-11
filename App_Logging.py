import logging
import os.path
        
def logging_file():
    
    if not os.path.isfile('app.log'):
        f= open('app.log', 'w+')
        f.close()
        
def getLogger(fname:str):
    # reset default serverity from warning to debug
    logging.basicConfig(level=logging.NOTSET)
    logger = logging.getLogger(fname)

    s_handler = logging.StreamHandler()
    logging_file()
    f_handler = logging.FileHandler('app.log')

    s_handler.setLevel(logging.INFO)
    f_handler.setLevel(logging.INFO)

    output_format = '[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s'
    s_format = logging.Formatter(output_format)
    f_format = logging.Formatter(output_format)

    s_handler.setFormatter(s_format)
    f_handler.setFormatter(f_format)
    
    logger.propagate = False
    
    logger.addHandler(s_handler)
    logger.addHandler(f_handler)

    return logger
