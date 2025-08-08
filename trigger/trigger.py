import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from celery import chain
from agents.apiprice_agent.tasks import fetch_price
from agents.3emaindicator_agent.tasks import calculate_ema
from agents.bangstate_agent.tasks import check_for_bang


class ChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        workflow = chain(
            fetch_price.s(),
            calculate_ema.s(),
            check_for_bang.s(),
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
