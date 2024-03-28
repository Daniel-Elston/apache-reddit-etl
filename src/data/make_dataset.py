from __future__ import annotations

import json
import logging
import os
import time

import praw

from utils.file_handler import temp_store
from utils.setup_env import setup_project_env
project_dir, config, setup_logs = setup_project_env()

CREDS = {
    'client_id': os.getenv('REDDIT_CLIENT_ID'),
    'client_secret': os.getenv('REDDIT_CLIENT_SECRET'),
    'user_agent': os.getenv('REDDIT_USER_AGENT'),
    'username': os.getenv('REDDIT_USERNAME'),
    'password': os.getenv('REDDIT_PASSWORD')
}


class RedditManager:
    def __init__(self, reddit_creds):
        self.reddit = praw.Reddit(**reddit_creds)
        self.logger = logging.getLogger(self.__class__.__name__)

    def stream_comments(self, subreddit_name, filepath):
        try:
            for comment in self.reddit.subreddit(subreddit_name).stream.comments(skip_existing=True):
                timestamp = time.time()
                data = {
                    'timestamp': timestamp,
                    'body': comment.body
                }
                temp_store(data, filepath)

        except praw.exceptions.PRAWException as e:
            self.logger.error(f"PRAW exception occurred: {e}")
        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")

    def temp_store(self, data, filepath):
        with open(filepath, 'w') as f:
            json.dump(data, f)


def main():
    reddit_manager = RedditManager(CREDS)
    subreddit_name = 'funny'
    filepath = f'data/temp/{subreddit_name}.json'
    reddit_manager.stream_comments(subreddit_name, filepath)


if __name__ == '__main__':
    main()
