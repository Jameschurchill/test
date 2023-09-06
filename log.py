import logging
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%m-%d-%Y %H:%M:%S %p"
logging.basicConfig(level=logging.DEBUG,filename='my.log',datefmt=DATE_FORMAT,format=LOG_FORMAT)   #´ÓdebugÊä³ö
logging.debug('this is a debug!....')
logging.info('this is a info!....')
logging.warning('this is a warning!....')
logging.error('this is a error!....')
logging.critical('this is a critical!....')