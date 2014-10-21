import logging
import os
import signal
import sys
import subprocess

from time import sleep

from pync import Notifier

from fsevents import Observer, Stream

import daemon

project_path, junk = os.path.split(os.path.dirname(os.path.realpath(__file__)))
littlehelp_script = os.path.join(project_path, 'littlehelp')
del junk

logging.basicConfig(filename=os.path.join(project_path, '.littlehelp/littlehelp.log'),level=logging.INFO)

ignored_suffix = ['.DS_Store','.swp',"littlehelp.log"]

def file_event_callback(event):
    # just worry about the modification events.
    if event.mask == 2:
        for suffix in ignored_suffix:
            if event.name.endswith(suffix):
                print "ignoring file: {0}".format(event.name)
                break
        else:
            file_path, file_name = os.path.split(event.name)
            logging.info("Mask: %s, Cookie: %s, Name: %s" % (event.mask, event.cookie, event.name))
            try:
                subprocess.call('{0} action {1} {2}'.format(littlehelp_script, file_path, file_name), shell=True)
            except:
                logging.exception("Exceptiong whilst running action '{0} action {1} {2}'".format(littlehelp_script, file_path, file_name))
            Notifier.notify('change to file: {0}, triggered action'.format(file_name), title='LittleHelp', subtitle=project_path)

def main():

    def sigterm_handler(_signo, _stack_frame):
        try:
            Notifier.notify('Unregistering fs watch', title='LittleHelp', subtitle=project_path)
        except:
            pass
        logging.info("Sigterm handler called")
        observer.unschedule(stream)
        observer.stop()
        observer.join()
        try:
            Notifier.notify('Unregistered fs watch', title='LittleHelp', subtitle=project_path)
        except:
            pass
        sys.exit(0)

    try:
        Notifier.notify('Registering watch', title='LittleHelp', subtitle=project_path)
        observer = Observer()
        stream = Stream(file_event_callback, project_path, file_events=True)
        observer.schedule(stream)
        observer.start()

        signal.signal(signal.SIGTERM, sigterm_handler)

        while True:
            sleep(0.1)
    except:
        logging.exception("Unhandled exception")

if __name__ == "__main__":
    logging.debug("Project Path: {0}".format(project_path))
    logging.debug("Littlehelp Script: {0}".format(littlehelp_script))

    with daemon.DaemonContext():
        main()
