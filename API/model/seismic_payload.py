from enum import Enum
from model.payload import Payload

SEISMIC_TABLE_NAME = "measurement"


class SeismicPayload(Payload):

    def __init__(self, date, magnetic_field_x, magnetic_field_y, magnetic_field_z, acceleration):
        self.date = date
        self.magnetic_field_x = magnetic_field_x
        self.magnetic_field_y = magnetic_field_y
        self.magnetic_field_z = magnetic_field_z
        self.acceleration = acceleration

    def to_dict(self):
        return {SeismicPayloadTags.date.name: self.date,
                SeismicPayloadTags.magnetic_field_x.name: self.magnetic_field_x,
                SeismicPayloadTags.magnetic_field_y.name: self.magnetic_field_y,
                SeismicPayloadTags.magnetic_field_z.name: self.magnetic_field_z,
                SeismicPayloadTags.acceleration.name: self.acceleration}

    def to_tuple(self):
        return (self.date, self.acceleration, self.magnetic_field_x,
                self.magnetic_field_y, self.magnetic_field_z)

    def get_insert_query(self):
        return f"INSERT INTO {SEISMIC_TABLE_NAME} (package_id, segment_id, date," \
               f"acceleration, magnetic_field_x, magnetic_field_y, magnetic_field_z) VALUES (%s,%s,%s,%s,%s,%s,%s)"


class SeismicPayloadTags(Enum):
    date = 1
    magnetic_field_x = 2
    magnetic_field_y = 3
    magnetic_field_z = 4
    acceleration = 5
