import sys
from networksecurity.logging.logger import logging
class NetworkSecurityException(Exception):
    def __init__(self, error_message,error_details: sys):
        self.error_message=error_message
        _,_,exc_tb=error_details.exc_info()
        self.lineno=exc_tb.tb_lineno
        self.filename=exc_tb.tb_frame.f_code.co_filename
    def __str__(self):
        return "Error occured in Python script name [{0}] lineno [{1}] error_message [{2}]".format(
            self.filename,self.lineno,self.error_message
        )
if __name__=="__main__":
    try:
        logging.info("entered into the try block")
        result=2/0
        print(result)
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    