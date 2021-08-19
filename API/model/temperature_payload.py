from datetime import datetime
from enum import Enum
from model.payload import Payload

TEMPERATURE_TABLE_NAME = "measurement"


class TemperaturePayload(Payload):

    def __init__(self, date, temperature, humidity):
        self.date = datetime.strptime(str(date), '%Y%m%d%H%M%S').strftime('%m/%d/%Y %H:%M:%S')
        self.temperature = temperature
        self.humidity = humidity

    def to_dict(self):
        return {TemperaturePayloadTags.date.name: self.date,
                TemperaturePayloadTags.temperature.name: self.temperature,
                TemperaturePayloadTags.humidity.name: self.humidity}

    def to_tuple(self):
        return self.date, self.temperature, self.humidity

    def get_insert_query(self):
        return f"INSERT INTO {TEMPERATURE_TABLE_NAME} (package_id, segment_id, date," \
               f"temperature, humidity) VALUES (%s,%s,%s,%s,%s)"


class TemperaturePayloadTags(Enum):
    date = 1
    temperature = 2
    humidity = 3
