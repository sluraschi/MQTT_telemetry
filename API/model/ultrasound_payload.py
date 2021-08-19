from enum import Enum
from model.payload import Payload

ULTRASOUND_TABLE_NAME = "measurement"


class UltrasoundPayload(Payload):

    def __init__(self, distance):
        self.distance = distance

    def to_dict(self):
        return {UltrasoundPayloadTags.distance.name: self.distance}

    def to_tuple(self):
        return self.distance

    def get_insert_query(self):
        return f"INSERT INTO {ULTRASOUND_TABLE_NAME} (package_id, segment_id, date," \
               f"distance) VALUES (%s,%s,%s,%s)"


class UltrasoundPayloadTags(Enum):
    distance = 1
