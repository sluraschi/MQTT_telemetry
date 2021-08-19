from enum import Enum
from model.payload import Payload

EXAMPLE_TABLE_NAME = "measurement"  # (1) Nueva constante con el nombre de la tabla

class ExamplePayload(Payload):  # (2) Aqui se indica la herencia de la clase Payload

    def __init__(self, date, temperature, distance):  # (3) En el mismo constructor se indican los atributos de la clase y se parsea el paylaod
        self.date = datetime.strptime(str(date), '%Y%m%d%H%M%S').strftime('%m/%d/%Y %H:%M:%S')
        self.temperature = temperature
        self.distance = distance

    def to_dict(self):  # (4) Devuelve de la forma {tag1: atributo1, tag2: atributo2, ...}
        return {TemperaturePayloadTags.date.name: self.date,
                ExamplePayloadTags.distance.name: self.distance,
                ExamplePayloadTags.temperature.name: self.temperature}

    def to_tuple(self): # (5) Devuelve de la forma (atributo1, atributo2, ...)
        return (self.date,
                self.distance,
                self.temperature)

    def get_insert_query(self): # (6) Nuevo metodo con la query para insertar en la base de datos
        return f"INSERT INTO {EXAMPLE_TABLE_NAME} (package_id, segment_id, date," \
               f"position, temperature) VALUES (%s,%s,%s,%s,%s)"


class ExamplePayloadTags(Enum): # (7) Los tags para usar en el diccionario y no manejar stings que llevan a errores humanos
    date = 1
    distance = 2
    temperature = 3
