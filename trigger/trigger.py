import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from celery import chain
from agents.thea_agent.tasks import calculate_vwap_volume
from agents.vwapcross_agent.tasks import check_vwap_cross


class ChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        workflow = chain(
            calculate_vwap_volume.s(),
            check_vwap_cross.s(),
        )
        workflow.apply_async()


def main(path: str = '.'):
    handler = ChangeHandler()
    observer = Observer()
    observer.schedule(handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == '__main__':
    main()
