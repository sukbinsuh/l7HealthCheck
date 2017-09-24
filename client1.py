import requests
import time
import os
import subprocess
import logging

err_count = 0

def check_health():
    logger.info('check_health() is excuted!')
    global  err_count
    r = None
    try:
        r = requests.get('http://localhost:8000', timeout=10)
    except requests.RequestException as err:
        logger.info(err)
        pass
    except requests.ConnectionError as err:
        logger.info(err)
        pass
    except requests.ReadTimeout as err:
        logger.info(err)
        pass
    except requests.URLRequired as err:
        logger.info(err)
        pass
    except requests.TooManyRedirects as err:
        logger.info(err)
        pass
    except requests.ConnectTimeout as err:
        logger.info(err)
        pass
    finally:
        if (r is not None and r.text == '"OK"'):
            print "OK"
            err_count = 0
            return True
        else:
            err_count = err_count + 1
            return False

def kill_process(app_name):
    proc = subprocess.Popen('ps -aef | grep metatron', stdout=subprocess.PIPE)
    pid = proc.communicate()[0].split()[0]
    os.system("kill -9 " + pid)


if __name__ == "__main__":
    """
    params = dict(
    origin='Chicago,IL',
    destination='Los+Angeles,CA',
    waypoints='Joplin,MO|Oklahoma+City,OK',
    sensor='false'
    )
    
    resp = requests.get(url=url, params=params)
    data = json.loads(resp.text)
    """
    FORMAT = '%(asctime)-15s %(message)s'
    logging.basicConfig(format=FORMAT, filename='client.log', level=logging.INFO)
    logger = logging.getLogger('client')
    logger.info('Start Metatron Health Check Client')

    while True:
        if err_count == 0:
            logger.info('err_count is 0')
            check_health()
            time.sleep(10)
        elif err_count == 1:
            logger.info('err_count is 1')
            check_health()
            time.sleep(20)
        elif err_count == 2:
            logger.info('err_count is 2')
            check_health()
            time.sleep(30)
        elif err_count == 3:
            logger.info('err_count is 3')
            #kill metatron
            kill_process("Metatron")
            exit(1)




