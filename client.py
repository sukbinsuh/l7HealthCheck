import requests
import sched, time
import os
import subprocess

err_count = 0

def check_health():
    print "check Health"
    global  err_count
    r = None
    try:
        r = requests.get('http://localhost:8000', timeout=10)
    except requests.RequestException as err:
        print err
        pass
    except requests.ConnectionError as err:
        print err
        pass
    except requests.ReadTimeout as err:
        print err
        pass
    except requests.URLRequired as err:
        print err
        pass
    except requests.TooManyRedirects as err:
        print err
        pass
    except requests.ConnectTimeout as err:
        print err
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
    s = sched.scheduler(time.time, time.sleep)
    while True:
        if err_count == 0:
            print "err_count is 0"
            s.enter(10, 5, check_health, ())
            s.run()
        elif err_count == 1:
            print "err_count is 1"
            s.enter(20, 5, check_health, ())
            s.run()
        elif err_count == 2:
            print "err_count is 2"
            event = s.enter(30, 5, check_health, ())
        elif err_count == 3:
            print "err_count is 3"
            #kill metatron
            kill_process("Metatron")
            exit(1)




