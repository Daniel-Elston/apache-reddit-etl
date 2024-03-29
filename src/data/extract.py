from __future__ import annotations

import logging
import time

import praw


class ExtractData:
    def __init__(self, reddit_creds):
        self.reddit = praw.Reddit(**reddit_creds)
        self.logger = logging.getLogger(self.__class__.__name__)

    def stream_comments(self, subreddit_name, callback):
        try:
            for comment in self.reddit.subreddit(subreddit_name).stream.comments(skip_existing=True):
                timestamp = time.time()
                data = {
                    'timestamp': timestamp,
                    'body': comment.body
                }
                callback(data)

        except praw.exceptions.PRAWException as e:
            self.logger.error(f"PRAW exception occurred: {e}")
        except Exception as e:
            self.logger.error(f"An uznexpected error occurred: {e}")
