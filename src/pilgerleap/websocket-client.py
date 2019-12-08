import websocket
import logging
import time
import json
from phue import Bridge
import threading

logging.basicConfig(level=logging.INFO)

hue_b = []
pool = []
current_light = []

def maprange( a, b, s):
	(a1, a2), (b1, b2) = a, b
	return  int(b1 + ((s - a1) * (b2 - b1) / (a2 - a1)))


def on_message(ws, message):
    """
    called on message receive
    """
    global hue_b
    global pool
    global current_light

    logging.info(message)

    # create dict form str
    msg_dict = json.loads(message)

    # turn on/off
    if msg_dict['type'] == "power":
        current_state = hue_b.get_light(pool[current_light].name, 'on')
        hue_b.set_light(pool[current_light].name, 'on', not current_state)

    # change brightness
    if msg_dict['type'] == "brightness":
        bri = maprange((0, 100), (0, 254), msg_dict['value'])
        logging.info(bri)
        hue_b.set_light(pool[current_light].name, 'bri', bri)

    # swipe through lights
    if msg_dict['type'] == "swipe":
        if msg_dict['value'] == 'right':
            current_light = (current_light+1) % len(pool)
            logging.info('right' + pool[current_light].name)
            blink_lamp(pool[current_light].name)
        if msg_dict['value'] == 'left':
            current_light = (current_light-1) % len(pool)
            logging.info('right' + pool[current_light].name)
            blink_lamp(pool[current_light].name)


def blink_lamp(lamp):
    global hue_b
    # current_bri = hue_b.get_light(lamp, 'bri')
    hue_b.set_light(lamp, 'bri', 0, transitiontime=1)
    hue_b.set_light(lamp, 'bri', 254, transitiontime=1)
    time.sleep(0.05)
    hue_b.set_light(lamp, 'bri', 0, transitiontime=1)
    hue_b.set_light(lamp, 'bri', 254, transitiontime=1)


def on_error(ws, error):
    """
    called on error
    """
    logging.info(error)


def on_close(ws):
    """
    called on close connection
    """
    logging.info("### closed ###")


def on_open(ws):
    def run(*args):
        for i in range(3):
            time.sleep(1)
            ws.send("asdf")
        time.sleep(1)
        ws.close()
        logging.info("thread terminating...")
    thread.start_new_thread(run, ())


def connect_hue(ip):
    """
    connect to Hue nridge
    """
    b = Bridge(ip)
    # If the app is not registered and the button is not pressed, press the button and call connect() (this only needs to be run a single time)
    b.connect()
    return b


def get_lights(b):
    """
    get list of all lights
    """
    # Get the bridge state (This returns the full dictionary that you can explore)
    # parsed_json = json.loads(b.get_api())
    return b.get_light_objects('list')


def beautify_json(parsed_json):
    """
    make json nice
    """
    logging.info(json.dumps(parsed_json, indent = 4,sort_keys=False))
    return 0


def disco(lightname, hue_b, speed):
    """
    disco light
    """
    counter = 0
    while True:
        counter+=speed
        hue_b.set_light(lightname, 'bri', counter%254)
        if counter > 1000:
            break


def disco_party():
    thread1 = threading.Thread(target = disco, args = (1, hue_b, 10))
    thread2 = threading.Thread(target = disco, args = (2, hue_b, 20))
    thread3 = threading.Thread(target = disco, args = (4, hue_b, 30))
    thread4 = threading.Thread(target = disco, args = (5, hue_b, 40))

    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()


def main():
    global hue_b
    global pool
    global current_light
    # Bridge
    logging.info("Connecting to Hue Bridge")
    ip = '192.168.178.46'
    hue_b = connect_hue(ip)
    # Create iter list
    pool = get_lights(hue_b)
    current_light = 0

    logging.info(pool[0])

    # reset light 1 to full
    blink_lamp(pool[current_light].name)

    # Web Socket
    logging.info("Connecting to Web Socket Server")
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://192.168.178.43:8080",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    # ws.on_open = on_open
    ws.run_forever()

    # # party time
    # disco_party()


if __name__ == "__main__":
    main()
    