import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileCreatedEventHandler(FileSystemEventHandler):
    def __init__(self, on_created):
        self.on_created = on_created

    def on_created(self, event):
        super(FileCreatedEventHandler, self).on_created(event)
        if not event.is_directory:
            self.on_created(event.src_path)

def start_monitoring(path, on_created):
    event_handler = FileCreatedEventHandler(on_created=on_created)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()