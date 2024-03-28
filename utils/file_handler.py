from __future__ import annotations

import json
import logging


def temp_store(data, filepath):
    try:
        with open(filepath, 'a') as f:
            json.dump(data, f)
            f.write('\n')
    except IOError as e:
        logging.error(f"Failed to store data: {e}")
