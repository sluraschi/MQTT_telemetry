# Guia de uso

Se recomienda leer toda la guia antes de implementar algun cambio (y no implementarlos a medida que se da la primera lectura) ya que aqui se muestra un ejemplo de como resolver la escalabilidad hacia nuevas aplicaciones pero al final se proponen otra alternativa que surgió luego de la escritura del ejemplo aqui mostrado y puede ser muy interesante manejarlo de ese modo.

# Prerequisitos

1. Es de suma importancia leer en su totalidad el documento presentado como Trabajo Final de carrera ubicado [aqui]() para comprender todas las partes y sus relaciones.

2. Poseer un modulo de sensado cuya salida sea el paquete establecido por puerto serie.

# Primer uso

## Broker MQTT

Lo primero a hacer es crear un broker MQTT. En Heroku esto es fácil: 

1. Primero se crea una nueva aplicación:

![alt text](imagenes/new-app.png)

2. Luego se agrega el broker a la misma yendo a _"Resources"_, buscando _"CloudMQTT"_ y confirmando la selección:

<img src="imagenes/broker.png" alt="drawing" height="350" width="475"/> <img src="imagenes/submit.png" alt="drawing" height="350"/> 

_Más información sobre los planes del broker puede encontrarse en: [https://elements.heroku.com/addons/cloudmqtt](https://elements.heroku.com/addons/cloudmqtt)_

## Inicio de los servicios 

Luego es necesario publicar los 3 servicios de la solucion (publisher, suscriber y API hacia la base de datos) para poder mantener el codigo actualizado y funcionando.

1. Cree un repositorio en Github para el Publisher siguiendo los pasos de [esta guia](https://docs.github.com/en/get-started/quickstart/create-a-repo).

2. Tomar el código de la carpeta [Publisher](/Publisher) y subirlo al repositorio.

3. Repetir los pasos 1 y 2 para el código del [Suscriber](/Suscriber) y de la [API](/API).

Con los códigos ya publicados en un repositorio es necesario poner a funcionar el suscriber y la API. Para eso hay que hostearlas en algun lado, la opción más facil es [Heroku](https://heroku.com/) siguiendo los siguientes pasos:

1. Entrar a Heroku y crear una aplicación como se mostró para el broker.

2. Una vez creada hay que conectar el repositorio creado previamente y activar _deploys_ automaticos:

![connect-repo](imagenes/connect-repo.png)

![auto-deploy](imagenes/auto-deploy.png)

3. Realizar el primer deploy a mano:

![manual-deploy](imagenes/manual-deploy.png)

Si todo salió bien, en la pestaña general deberá ver el build exitoso y deploy completado:

<img src="imagenes/result.png" alt="drawing" height="200"/> 


**IMPORTANTE: ESTO APLICA AL SUSCRIBER Y A LA API, NO AL PUBLISHER.**


# Ejemplo de nueva aplicacion

Se desea utilizar el sistema de telemetría para observar la posición de un cuerpo con movimiento en un único eje y la temperatura del mismo. 

## Paso 1: Conocer el formato del payload que llega desde el módulo de sensado. 

Si bien el formato esta estandarizado, hay un campo que es variable y es el payload, donde van las mediciones. Este cambia con cada aplicación y debe definirse de antemano según la transmisión del módulo de sensado.

Para este ejemplo supondremos que el playload se envia de la siguiente manera:

```
payload: DXXTXX
```

Donde D indica el inicio del dato de la distancia, T la temperatura y XX son los datos respectivamente.

## Paso 2: Nuevo topico en el Broker (Si es necesario)

a. Debo tener un tópico en el broker MQTT. Esto dependerá del broker utilizado pero si se continua con el de Heroku: 

<img src="imagenes/topics.png" alt="drawing" height="300"/> <img src="imagenes/new-topic.png" alt="drawing" height="300"/>

## Paso 3: Crear base de datos - PostgreSQL

1. Luego voy a crear una app en Heroku donde voy a tener la base de datos agregando el recurso al igual que con el broker:

<img src="imagenes/postgres.png" alt="drawing" width="400"/>

2. Una vez creado el recurso, tengo que poder conectarme para crear lo necesario y ver el contenido cuando lo haya. Para esto necesito el software [pgAdmin4](https://www.pgadmin.org/download/).

3. Desde este voy a crear un server:

<img src="imagenes/new-server.png" alt="drawing" width="400"/>

4. Y para los datos necesarios, desde el recurso de Heroku voy a _Settings_ -> _View Credentials_ y completo como muestra debajo. 

_Heroku:_

<img src="imagenes/heroku-db-creds.png" alt="drawing" height="300"/>

_Postgres:_

<img src="imagenes/db-conn-1.png" alt="drawing" width="350"/> <img src="imagenes/db-conn-2.png" alt="drawing" width="350"/>

Si la conexión es exitosa en la ventana de la izqueirda debería ver el servidor y puedo correr queries para crear las tablas:

<img src="imagenes/db-result.png" alt="drawing" height="225"/>

5. Para terminar el armado de la base voy a crear las tablas también desde el PgAdmin. Para esto ya hay un script disponibles para las tablas generales ubicado [aqui](/Db/tables_creator.sql) y solo es necesario modificar el de las tablas especificas para el modelo nuevo. Para este ejemplo, dado que medimos una posición y una temperatura tendremos 2 valores numericos y la creación de esa tabla será:

```
CREATE TABLE measurement (
	payload_uuid UUID NOT NULL DEFAULT uuid_generate_v1(),
	segment_id numeric,
	package_id numeric,
	date TIMESTAMP NOT NULL,
	-- replace here the columns for your use case
	position numeric,
	temperature numeric,
	
	-- this should not be replaced
	PRIMARY KEY (payload_uuid),
	FOREIGN KEY (segment_id) 
		REFERENCES segment(id),
	FOREIGN KEY (package_id) 
		REFERENCES package(id)
);
```

6. Por último, debo encodear las credenciales de conexión a base 64 y agregarlas al proyecto del suscriber para que el mismo pueda usarlas en la inserción de los datos.
    
    a. Para el encodeo puedo utulizar cualquier pagina online como [https://www.base64encode.net/](https://www.base64encode.net/). 

	<a name="credenciales-db"></a>
    b. Luego para que el suscriber pueda utilizarlas voy a abrir su aplicación en Heroku, ir a Settings y agregarlas como variables de configuración que luego serán referenciadas desde el código:
    
    <img src="imagenes/config_vars.png" alt="drawing" height="450"/>  

    ![new-vars](imagenes/new_vars.png)


## Paso 4: Agregar nuevo caso al Publisher

2 Cosas hay que tener en cuenta en el Publisher, a que broker y a que tópico está publicando.

El sistema esta pensado para funcionar con el mismo broker luego de su creación y poder cambiar facilmente el tópico al que publica si se cambiará la aplicación del equipo. 

El broker se configura en el archivo [_config.py_](/Publisher/config.py) con el host y usuario de acceso que se indica en el broker:

![new-vars](imagenes/detail-broker.png)

Por otro lado, el tópico al que se publica se indica por párametro al iniciar el servicio dentro del equipo. Ubicado dentro del directorio, esto se haría con el comando `python3 main.py <topico>` pero dentro del equipo la publicación está automatizada como un servicio del sistema, por lo que hay que crear una unidad de servicio como se indica en la **sección 7.2.5.2 del Trabajo Profesional** presentado y presente en la documentación de este repositorio.

![new-vars](imagenes/service_definition.png)

---

**_TIP_**: _El tópico podria cambiarse remotamente con el telecomando creando un script que frene el servicio actual, reescriba este archivo como se desee y lo inicie nuevamente, de forma que manteniendo el equipo publicador en el campo podría tener una aplicación distinta._

---

## Paso 5: Agregar nuevo caso al codigo del Suscriber 

El Suscriber requiere más actualizacioens para un nuevo uso: 

<a name="nuevo-topico"></a>
1. Lo primero es agregar el nuevo tópico a la lista de tópicos conocidos por el Suscriber. Esto se encuentra en el archivo [topics.py_]() como un **Enum**:

	<img src="imagenes/suscriber-topics.png" alt="drawing" height="150"/>  

En nuestro ejemplo, dado que creamos el topico `/example`, el Enum resultante sería (o podrían quitarse los existentes si es que esas aplicaciones no son más utilizadas, a gusto del consumidor):

```
class Topics(Enum):
    SEISMIC = "/pi/test"
    T_AND_H = "/pi/temp"
    ULTRASOUND = "/pi/ultrasound"
	EXAMPLE = "/example'
```

<a name="nuevo-modelo"></a>

2. Ahora que puede recibir mensajes del tópico es necesario agregar un módelo para validar la recepción. Para eso vamos a crear un archivo *XXXX_payload.py* dentro de la carpeta [model](/Suscriber/model). En nuestro ejemplo lo vamos a llamar *example_payload.py* ([aquí](/Suscriber/model/example_payload.py)) y dentro del mismo es necesario definir su clase **que debe heredar la clase Payload** y tener: 
	a) un metodo _parse_payload()_ que defina como se deben leer los datos del payload, 
	b) un constructor que lo utilice,
	b) una clase Enum con las etiquetas,
	c) un metodo to_dict() que devuelva los atributos de la clase en forma de diccionario, 
	d) un metodo to_tuple() que devuelva los atributos de la clase en forma de n-upla. 

Aca es donde se pierde la generalidad del sistema ya que hasta este punto cualquier cosa que se transmita se iba a recibir, peor ahora es cuando se valída la información frente a un modelo de datos.

En nuestro ejemplo, el archivo *example_payload.py* sería:

```
from enum import Enum
from model.payload import Payload


def parse_payload(payload): # (1) Como dijimos, el payload es: DXXTXX, aca lo parseo a 2 variables separadas
    if payload == "FAIL":
        d_measure = None
        t_measure = None
    else:
        d_position = payload.upper().index("D")
        t_position = payload.upper().index("T")
        t_measure = payload[t_position + 1:]
        d_measure = payload[d_position + 1:t_position]
    return [d_measure, t_measure]


class ExamplePayload(Payload):  # (2) Aqui se indica la herencia de la clase Payload

    def __init__(self, payload):  # (3) En el mismo constructor se indican los atributos de la clase y se parsea el paylaod
        self.distance, self.temperature = parse_payload(payload)

    def to_dict(self):  # (4) Devuelve de la forma {tag1: atributo1, tag2: atributo2, ...}
        return {ExamplePayloadTags.distance.name: self.distance,
                ExamplePayloadTags.temperature.name: self.temperature}

    def to_tuple(self): # (5) Devuelve de la forma (atributo1, atributo2, ...)
        return (self.distance,
                self.temperature)


class ExamplePayloadTags(Enum): # (6) Los tags para usar en el diccionario y no manejar stings que llevan a errores humanos
    distance = 1
    temperature = 2

```

3. Una vez creado el modelo y sus reglas de parseo hay que agregar la orden para qu en cada recepción se construya y efectivamente se valide el formato. Esto se hace en el archivo [segments.py](/Suscriber/model/segments.py), en el método `build_payload()`. Nuevamente puede extenderse para funcionar para este modelo y otros o reeplazar alguno de los existentes en el codigo que ya no se utilicen. Si lo extendemos es simplemente agregar las siguientes lineas, donde es importante destacar que se hace referencia al topico agregado [aqui](#nuevo-topico):

```
        elif payload_type == Topics.EXAMPLE.value:
            return example_payload.ExamplePayload(**payload)
```


4. Por último, ya con la recepción y validación del modelo terminado, es necesario enviarlo a almacenar. La encargada de todas las operaciones relacionadas con la base de datos es la API que en este repositorio se encuentra en la carpeta [API](/API). Esto se hace en el método `upload_to_database()` del archivo [upload_database.py](/Suscriber/upload_database.py) y nuevamente podemos extender o reemplazar. Para extender es necesario agregar lo siguiente, donde:

1. El tópico de la priemra linea es el agrgado [aqui](#nuevo-topico).
2. Los nombres de las credenciales de la siguiente línea son [estas](#credenciales-db).
3. Y el `"example"` al final en el endpoint debe representar a esta nueva aplicación, lo referenciaremos en el próximo paso. 

```
    elif topic == mqtt_client.Topics.EXAMPLE.value:
        db_creds = db_credentials.DbCredentials(base64.b64decode(os.environ['EX_USR']).decode('utf-8'),
                                                base64.b64decode(os.environ['EX_SCRT']).decode('utf-8'))
        endpoint = BASE_ENDPOINT + "example"
```


## Paso 6: Agregar comunicación con nueva base de datos en la API

Para terminar la adopción de una nueva aplicación es necesario adaptar la API para que pueda almacenar el nuevo módelo en la nueva base de datos.

1. Lo primero es agregar al enum PaylaodTypes en el archivo de [constants.py](/API/constants.py)

![new-vars](imagenes/topics-api.png)

2. En este archivo de constantes tambien es necesario agregar host y base de datos nuevas a constantes de api de base de datos:



3. Lo primero es, al igual que el suscriber, agregarle la habilidad de recibir este nuevo mensaje. Para eso, al ser una API debemos agrgarle un nuevo _endpoint_. Esto se hace en el archivo principal [app.py](/API/app.py)



4. Lo segundo, tambien siguiendo la línea del suscriber, es sumar el modelo para que pueda validar lo que recibe. Y esto tambien se hace agregando el mismo archivo *example_payload.py* de [aqui](#nuevo-modelo) a la carpeta models con 2 agregados. 

	a. Una constante `EXAMPLE_TABLE_NAME = "measurement"` con el nombre de la tabla donde se insertará. (El mismo sedefinió al correr los scripts de creación de la base).

	b. Y vamos a incluir la query para su inserci[on a la base de datos en un método `get_insert_query()`, en este caso:

```
```

Notar el nombre de las columnas en la query y la nueva variable creada. `%s` en los valores indica...


De esta manera, el archivo quedaría:

```
from enum import Enum
from model.payload import Payload

EXAMPLE_TABLE_NAME = "measurement"  # (1) Nueva constante con el nombre de la tabla


def parse_payload(payload): # (2) Como dijimos, el payload es: DXXTXX, aca lo parseo a 2 variables separadas
    if payload == "FAIL":
        d_measure = None
        t_measure = None
    else:
        d_position = payload.upper().index("D")
        t_position = payload.upper().index("T")
        t_measure = payload[t_position + 1:]
        d_measure = payload[d_position + 1:t_position]
    return [d_measure, t_measure]


class ExamplePayload(Payload):  # (3) Aqui se indica la herencia de la clase Payload

    def __init__(self, payload):  # (4) En el mismo constructor se indican los atributos de la clase y se parsea el paylaod
        self.distance, self.temperature = parse_payload(payload)

    def to_dict(self):  # (5) Devuelve de la forma {tag1: atributo1, tag2: atributo2, ...}
        return {ExamplePayloadTags.distance.name: self.distance,
                ExamplePayloadTags.temperature.name: self.temperature}

    def to_tuple(self): # (6) Devuelve de la forma (atributo1, atributo2, ...)
        return (self.distance,
                self.temperature)

    def get_insert_query(self): # (7) Nuevo metodo con la query para insertar en la base de datos
        return f"INSERT INTO {EXAMPLE_TABLE_NAME} (package_id, segment_id, date," \
               f"position, temperature) VALUES (%s,%s)"


class ExamplePayloadTags(Enum): # (8) Los tags para usar en el diccionario y no manejar stings que llevan a errores humanos
    distance = 1
    temperature = 2
```

5. Agregar al buildPayload(subscriber y API)


# Propuestas

## 1
Otra alternativa que es de mi agrado para manejar los nuevos casos sería:

1. mantener el codigo para un solo caso, es decir por ejemplo, que el Enum de Topicos del suscriber tenga solo 1 aplicacion, Seismic por ejemplo, en los modelos solo este esa aplicacion y lo mismo para la base de datos y el resto de los servicios, solo contar con las cosas de esa aplicación.
2. Crear una [Branch](https://docs.github.com/es/github/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-branches) en GitHub POR CADA APLICACIÓN, y dentro de cada branch contar con el codigo especifico para esa aplicación.
3. Es decir, en cada servicio (publisher, suscriber y API hacia la base de datos) tendrían una branch por aplicación (sensor sismico, nivel de agua, temperatura, etc...) con el código especifico para esa aplicación.

## 2
Si el sistema resulta de valor y se lo continua utilizando se propone también tomarse el tiempo de invetigar la posibilidad de refactorizarlo a lo que se conoce como arquitectura _config oriented_, donde los servicios cargan archivo de configuraciones ubicados en repositorios remotos y en estos archivos (por lo general en algun formato tipo JSON) se encuentra todo lo que hoy cambiamos en el código para un nuevo caso. De esta manera, para una nueva aplicación basta con agrgar archivos nuevos de configuración y no tocar cosas ya existentes.