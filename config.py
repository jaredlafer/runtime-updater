import logging

class Config(object):

    logging.basicConfig(filename='logs/updater.log', 
                    level=logging.INFO, 
                    format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
