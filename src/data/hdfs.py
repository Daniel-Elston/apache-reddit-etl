from __future__ import annotations

from pyarrow import fs


class HFSManagement:
    def __init__(self, filepath):
        self.filepath = filepath
        # self.fs = fs.connect()
        self.hdfs = fs.HadoopFileSystem("namenode")

    def save_to_fs(self, data):
        with self.hdfs.open(self.filepath, 'wb') as file:
            file.write(data)

    def read_from_fs(self):
        with self.hdfs.open(self.filepath, 'rb') as file:
            return file.read()
