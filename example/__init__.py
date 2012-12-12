#
# Copyright 2012 WebFilings, LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""Contained within this module are several working examples showing basic
usage and complex context-based chaining.

The examples demonstrate basic task execution, and also the basics of creating
more complicated processing pipelines.
"""

import logging

import webapp2


class AsyncIntroHandler(webapp2.RequestHandler):
    """Demonstrate the creation and insertion of a single furious task."""
    def get(self):
        from furious.async import Async

        # Instantiate an Async object.
        async_task = Async(
            target=example_function, args=[1], kwargs={'some': 'value'})

        # Insert the task to run the Async object, note that it may begin
        # executing immediately or with some delay.
        async_task.start()

        logging.info('Async job kicked off.')

        self.response.out.write('Successfully inserted Async job.')


class ContextIntroHandler(webapp2.RequestHandler):
    """Demonstrate using a Context to batch insert a group of furious tasks."""
    def get(self):
        from furious.async import Async
        from furious import context

        # Create a new furious Context.
        with context.new() as ctx:
            # "Manually" instantiate and add an Async object to the Context.
            async_task = Async(
                target=example_function, kwargs={'first': 'async'})
            ctx.add(async_task)
            logging.info('Added manual job to context.')

            # Use the shorthand style, note that add returns the Async object.
            for i in xrange(5):
                ctx.add(target=example_function, args=[i])
                logging.info('Added job %d to context.', i)

        # When the Context is exited, the tasks are inserted (if there are no
        # errors).

        logging.info('Async jobs for context batch inserted.')

        self.response.out.write('Successfully inserted a group of Async jobs.')


class AsyncCallbackHandler(webapp2.RequestHandler):
    """Demonstrate setting an Async callback."""
    def get(self):
        from furious.async import Async

        # Instantiate an Async object, specifying a 'success' callback.
        async_task = Async(
            target=example_function, args=[1], kwargs={'some': 'value'},
            callbacks={'success': all_done}
        )

        # Insert the task to run the Async object.  The success callback will
        # be executed in the furious task after the job is executed.
        async_task.start()

        logging.info('Async job kicked off.')

        self.response.out.write('Successfully inserted Async job.')

    def get(self):
        """Create and insert a single furious task."""
        from furious.async import Async

        # Instantiate an Async object.
        async_task = Async(
            target=example_function, args=[1], kwargs={'some': 'value'},
            callbacks={'success': all_done}
        )

        # Insert the task to run the Async object, not that it may begin
        # executing immediately or with some delay.
        async_task.start()

        logging.info('Async job kicked off.')

        self.response.out.write('Successfully inserted Async job.')


def example_function(*args, **kwargs):
    """This function is called by furious tasks to demonstrate usage."""
    logging.info('example_function executed with args: %r, kwargs: %r',
                 args, kwargs)

    return args


def all_done():
    """Will be run if the async task runs successfully."""
    from furious.context import get_current_async

    async = get_current_async()

    logging.info('async task complete, value returned: %r', async.result)


app = webapp2.WSGIApplication([
    ('/', AsyncIntroHandler),
    ('/context', ContextIntroHandler),
    ('/callback', AsyncCallbackHandler),
    ('/callback/async', AsyncAsyncCallbackHandler),
])

