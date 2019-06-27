import threading
from Queue import Queue
import paramiko

# Define username and password to login to all routers with
USERNAME = 'ubnt'
PASSWORD = 'ubnt'
PORT = 22
COMMAND = 'set-inform http://p01.hostifi.net:8080/inform'
SUBNET = '192.168.1.'

hostnames = []
ips = range(1,254)
for i in ips:
    hostnames.append(SUBNET + str(i))

def ssh_session(hostname, output_q):
    try:
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.WarningPolicy)

        client.connect(hostname, port=PORT, username=USERNAME, password=PASSWORD)

        stdin, stdout, stderr = client.exec_command(COMMAND)
        print stdout.read(),

    finally:
        client.close()


if __name__ == "__main__":

    output_q = Queue()

    # Start thread for each router in routers list
    for hostname in hostnames:
        my_thread = threading.Thread(target=ssh_session, args=(hostname, output_q))
        my_thread.start()

    # Wait for all threads to complete
    main_thread = threading.currentThread()
    for some_thread in threading.enumerate():
        if some_thread != main_thread:
            some_thread.join()

    # Retrieve everything off the queue - k is the router IP, v is output
    # You could also write this to a file, or create a file for each router

    while not output_q.empty():
        my_dict = output_q.get()
        for k, val in my_dict.iteritems():
            print k
            print val
