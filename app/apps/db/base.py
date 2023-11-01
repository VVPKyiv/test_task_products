from abc import ABC, abstractmethod

from fastapi import Depends, HTTPException
from typing import Dict
import json

from app.root.settings.base import get_settings


# Define the path to your JSON file



class JSONFileHandler(ABC):
    def __init__(self, file_path):
        self.file_path = file_path

    @abstractmethod
    def read_data(self):
        pass

    @abstractmethod
    def write_data(self, data):
        pass

    @abstractmethod
    def update_data(self, key, value):
        pass

    @abstractmethod
    def delete_data(self, key):
        pass

    def set_default_structure(self):
        return {
            "products": [],
            "categories": [],
            "reviews": [],
        }


class LocalJSONFileHandler(JSONFileHandler):
    def read_data(self):
        try:
            with open(self.file_path, "r") as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            return self.set_default_structure()

    def write_data(self, data):
        with open(self.file_path, "w") as file:
            json.dump(data, file)

    def update_data(self, key, value):
        data = self.read_data()
        data[key] = value
        self.write_data(data)

    def delete_data(self, key):
        data = self.read_data()
        if key in data:
            del data[key]
            self.write_data(data)


# Implementation for AWS S3 storage
class S3JSONFileHandler(JSONFileHandler):
    def __init__(self, s3_client, bucket_name, object_key):
        self.s3_client = s3_client
        self.bucket_name = bucket_name
        self.object_key = object_key

    # TODO implement all abstract method
    def read_data(self):
        pass

    def write_data(self, data):
        pass

    def update_data(self, key, value):
        pass

    def delete_data(self, key):
        pass


# Dependency to provide the file_db object
def get_file_db():
    settings = get_settings()
    if settings.S3_CLIENT:
        # TODO implement S3
        file_db = S3JSONFileHandler(None, None, None)
    else:
        file_db = LocalJSONFileHandler(settings.JSON_FILE_PATH)
    return file_db
