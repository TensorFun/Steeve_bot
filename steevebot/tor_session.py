import requests
from stem import Signal
from stem.control import Controller

def get_tor_session():
    session = requests.session()
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
        controller.signal(Signal.NEWNYM)

    session = get_tor_session()
    newIP = session.get("http://httpbin.org/ip").json()['origin']
    
    while oldIP == newIP:
        with Controller.from_port(port = 9051) as controller:
            controller.authenticate(password='mypassword')
            controller.signal(Signal.NEWNYM)

        newIP = session.get("http://httpbin.org/ip").json()['origin']

    print("New IP: %s" % newIP)
