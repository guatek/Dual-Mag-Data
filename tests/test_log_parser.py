import sys 
sys.path.append('..')

from libs.log_parser import DualMagLog

dl = DualMagLog("..\\resources\\2019-11-06-17-00-28.045872072.log")
dl.parse_lines()
dl.export("..\\resources\\2019-11-06-17-00-28.045872072.csv")