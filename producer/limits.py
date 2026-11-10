import os,platform,resource,signal,threading,time
def start():
    signal.alarm(60)
    scale=1 if platform.system()=='Darwin' else 1024
    def watch():
        while True:
            if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*scale>2*1024**3:
                os.write(2,b'Certificate checker RSS limit 2GiB exceeded\n');os._exit(137)
            time.sleep(0.1)
    threading.Thread(target=watch,daemon=True).start()
