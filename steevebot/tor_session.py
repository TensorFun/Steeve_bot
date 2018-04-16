import requests
from stem import Signal
from stem.control import Controller

def get_tor_session():
    session = requests.Session()
    # Tor uses the 9050 port as the default socks port
    session.proxies = {'http':  'socks5://127.0.0.1:9050',
                       'https': 'socks5://127.0.0.1:9050'}
    return session

session = get_tor_session()

def renewTorIP():
    global session
    oldIP = session.get("http://httpbin.org/ip").json()['origin']
    print("Old IP: %s" % oldIP)

    with Controller.from_port(port = 9051) as controller:
        controller.authenticate(password='mypassword')
        # print("Success!")
        controller.signal(Signal.NEWNYM)
        # print("New Tor connection processed\n")

    session = get_tor_session()
    newIP = session.get("http://httpbin.org/ip").json()['origin']
    print("New IP: %s" % newIP)
    
    if oldIP == newIP:
        renewTorIP()
    else:
        return
