import threading
import time

try:
    import winsound
except ImportError:
    winsound = None


class AlarmState:
    def __init__(self):
        self.is_running = False
        self.stop_event = threading.Event()
        self.thread = None


def alarm_worker(stop_event):
    while not stop_event.is_set():
        if winsound is not None:
            winsound.Beep(2500, 700)
        else:
            print("\a", end="", flush=True)
            time.sleep(0.7)
        time.sleep(0.1)


def trigger_alarm(alarm_state):
    if alarm_state.is_running:
        return

    alarm_state.stop_event.clear()
    alarm_state.thread = threading.Thread(
        target=alarm_worker,
        args=(alarm_state.stop_event,),
        daemon=True,
    )
    alarm_state.thread.start()
    alarm_state.is_running = True


def stop_alarm(alarm_state):
    if not alarm_state.is_running:
        return

    alarm_state.stop_event.set()
    alarm_state.is_running = False