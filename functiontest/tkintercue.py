#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# based on <https://stackoverflow.com/a/47920128/4865723>

from tkinter import *
import asyncio
import threading
import random
import queue


class AsyncioThread(threading.Thread):
    def __init__(self, the_queue, max_data):
        self.asyncio_loop = asyncio.get_event_loop()
        self.the_queue = the_queue
        self.max_data = max_data
        threading.Thread.__init__(self)

    def run(self):
        self.asyncio_loop.run_until_complete(self.do_data())

    async def do_data(self):
        """ Creating and starting 'maxData' asyncio-tasks. """
        tasks = [
            self.create_dummy_data(key)
            for key in range(self.max_data)
        ]
        await asyncio.wait(tasks)

    async def create_dummy_data(self, key):
        """ Create data and store it in the queue. """
        sec = random.randint(1, 10)
        data = '{}:{}'.format(key, random.random())
        await asyncio.sleep(sec)

        self.the_queue.put((key, data))


class TheWindow:
    def __init__(self, max_data):
        # thread-safe data storage
        self.the_queue = queue.Queue()

        # the GUI main object
        self.root = Tk()

        # create the data variable
        self.data = []
        for key in range(max_data):
            self.data.append(StringVar())
            self.data[key].set('<default>')

        # Button to start the asyncio tasks
        Button(master=self.root,
               text='Start Asyncio Tasks',
               command=lambda: self.do_asyncio()).pack()
        # Frames to display data from the asyncio tasks
        for key in range(max_data):
            Label(master=self.root, textvariable=self.data[key]).pack()
        # Button to check if the GUI is freezed
        Button(master=self.root,
               text='Freezed???',
               command=self.do_freezed).pack()

    def refresh_data(self):
        """
        """
        # do nothing if the aysyncio thread is dead
        # and no more data in the queue
        if not self.thread.is_alive() and self.the_queue.empty():
            return

        # refresh the GUI with new data from the queue
        while not self.the_queue.empty():
            key, data = self.the_queue.get()
            self.data[key].set(data)

        print('RefreshData...')

        #  timer to refresh the gui with data from the asyncio thread
        self.root.after(1000, self.refresh_data)  # called only once!

    def do_freezed(self):
        """ Button-Event-Handler to see if a button on GUI works.
            The GOAL of this example is to make this button clickable
            while the other thread/asyncio-tasks are working. """
        print('Tkinter is reacting. Thread-ID: {}'
              .format(threading.get_ident()))

    def do_asyncio(self):
        """
            Button-Event-Handler starting the asyncio part in a separate
            thread.
        """
        # create Thread object
        self.thread = AsyncioThread(self.the_queue, len(self.data))

        #  timer to refresh the gui with data from the asyncio thread
        self.root.after(1000, self.refresh_data)  # called only once!

        # start the thread
        self.thread.start()


if __name__ == '__main__':
    window = TheWindow(25)
    window.root.mainloop()