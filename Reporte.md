# Reporte de proyecto final 18001404

### Video de presentación final: https://youtu.be/N7QnLU8XHbo 

## Obtención de fuente de datos:
Los datos utilizados en el proyecto fueron obtenidos del sitio web de kaggle:
https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce

El dataset consiste en información sobre las ventas realizadas en Olist desde 2016 hasta 2018, la cual es un ecommerce
que conecta pequeñas empresas de todo Brasil con los clientes a través de un contrato. Esos comerciantes pueden vender
sus productos a través de la Tienda Olist y enviarlos directamente a los clientes utilizando los socios logísticos de Olist. Su
funcionamiento es muy similar al de Amazon, con la diferencia que está enfocado primordialmente al transporte dentro
de Brasil.

Después de que un cliente compra el producto de Olist Store, se notifica a un vendedor para cumplir con ese pedido. Una
vez que el cliente recibe el producto, o vence la fecha estimada de entrega, el cliente recibe una encuesta de satisfacción
por correo electrónico donde puede dejar una nota sobre la experiencia de compra y anotar algunos comentarios.
El modelo de datos que contiene la información del sistema, desde la compra hasta el envío y su reseña se puede observar
en el siguiente diagrama:

![esquema original](/imagen/HRhd2Y0.png)

## Preguntas de negocio por responder
Dentro de las preguntas que el modelo dimensional permitirá responder se encuentran:
1. ¿Qué categoría de productos son los que generan la mayor cantidad de ventas?
2. ¿En dónde se encuentra la mayor parte de los clientes (ciudad y estado)?
3. ¿Cuál es la estacionalidad de compra en línea que tienen los usuarios, existen horas dónde hay una mayor
solicitud de ordenes?
4. ¿Cuáles son los productos mejor y peor calificados? En caso a los peor calificados, ¿a qué se debe?
5. ¿Cuál es el método de pago preferido por los clientes?

## Modelo dimensional
![modelo](/imagen/dimensional.png)

## Exploración y limpieza de datos
Se realizo la respectiva exploración y limpieza del conjunto de datos a través de Python. En la que se determinó:

***El siguiente procedimiento se encuentra en el archivo "prepareData.ipynb"***

1. Existe una relación de 1 a 1 entre id de la orden y el id del cliente
>> Se comprobó al realizar inner join entre cliente y orden con el cliente id, si fuera falsa la hipotésis entonces la cantidad original de clientes hubieran sido distinta al resutado obtenido al combinar con orden (referencia archivo "prepareData.ipynb")
2. Una orden puede ser pagada por partes, es decir una parte del total de la orden está ingresada como tarjeta de
crédito mientras que otra parte es transferencia a cuenta. También puede ser un mismo método de pago, pero
ingresado por partes.
>> Se realizó una agrupación por orden y tipo de pago, se obtuvo que para algunas ordenes habia en promedio 2 tipos de pagos distintos (referencia archivo "prepareData.ipynb")
3. Para un mismo código postal, el nombre de ciudad y estado varían debido a que tiene acentos. Por lo que es
necesario eliminar acentos para que exista uniformidad con los datos de cliente y vendedor en relación con su
ubicación.
>> Se comprobó aquellos códigos postales donde el nombre de estado y ciudad para cliente y vendedor eran distintos. Se pudo observar que una gran parte se tenía guardado como diferentes debido al uso de acentos. (referencia archivo "prepareData.ipynb")
4. Los id de cliente, vendedor, orden y producto son de tipo texto de 32 caracteres. Por lo que se propone crear
llave sorrugada para que el rendimiento del tiempo de consulta en la base de datos no se vea afectado, de igual
forma si en algún momento se necesita actualizar o modificar id del usuario o producto se podrá realizar (en
creación de escenario). 
>> (referencia archivo "prepareData.ipynb")
5. Filtración de columnas de interés previo a su ingreso a la base de datos (simulando sistema (escenario)), con la
finalidad de reducir tiempo de ejecución.
>> (referencia archivo "prepareData.ipynb")
6. Adicionalmente se agrega Fake data sobre datos personales (nombre, correo y teléfono) a cliente y vendedor,
con la finalidad de simular el escenario del sistema lo más cercano posible a la realidad. 
>> (referencia archivo "prepareData.ipynb") (data generada desde onlinedatagenerator.com)

## Creación de escenario
Después de explorar los datos y realizar su limpieza respectiva, se procede a crear la base de datos de PostgreSQL a
través de los servicios que ofrecen AWS Amazon utilizando Python.

***El siguiente procedimiento se encuentra en el archivo "system.ipynb"***

1. Se importa cada una de las librerias a utilizar (pandas, numpy, datetime, boto3, psycopg2, configparser)
2. Inicializan las variables, en este caso el nombre de la instancia de RDS
3. Se lee el archivo de configuraciones en donde se encuentran las credenciales a la base de datos
4. Se crea la instancia de RDS
5. Verificación de las instancias actuales de RDS
6. Creación del servicio RDS
7. Se obtiene URL del Host de la base de datos
8. Conexión a la base de datos y creación de tablas en donde se almacenará la información. Para ello se debe cargar el archivo "sql_queries.py" en donde se tiene información sobre las tablas creadas en la base de datos
9. Insertar datos en tablas, para ello se debe crear el driver que ejecutará cada una de las consultas con la base de datos.
10. Verificación de datos insertados en cada tabla (utilizando DBeaver)

![customer](/imagen/customerlimit.png)

![seller](/imagen/sellerLimit.png)

![review](/imagen/reviewlimit.png)

![orderHead](/imagen/orderheadlimit.png)

![product](/imagen/productlimit.png)

![ventas](/imagen/ventaslimit.png)

## Construcción de datawarehouse
Se lleva a cabo las consultas en la base de datos que contiene el escenario del sistema original y se construyen las
dimensiones para el data warehouse.

***El siguiente procedimiento se encuentra en el archivo "dwh.ipynb"***

1. Se importa cada una de las librerias a utilizar (pandas, numpy, datetime, boto3, psycopg2, configparser)
2. Se lee el archivo de configuraciones en donde se encuentran las credenciales a la base de datos
3. Se escribe la URL del host de la base de datos de PostgreSQL creada anteriormente (el escenario simulado del sistema original)
4. Creación del driver de PostgreSQL
5. Envío de consultas del tipo "SELECT * FROM table_name" para la carga y creación de cada dimensión
6. Creación de la dimensión calendario utilizando python y la fecha de compra de la orden
7. Creación de la tabla de hechos con las llaves de cada dimensión
8. Lectura de archivos desde S3 (tipo de pago y categoria de producto fueron almacenados como Excel y cargados a su respectiva dimension en el data warehouse)
9. Creación de instancia de RDS en MySQL, se colocó como nombre dw-db. El script que contiene las tablas creadas se encuentra en el archivo "create_dw_query.py"
10. Creación del driver de MySQL para comunicarse con la base de datos
11. Modificación del nombre de columna para que coincida con el nombre de columna de la dimension para insertar los datos
12. Verificación a través de DBeaver 

![dimcustomer](/imagen/dimcustomer.png)

![dimseller](/imagen/dimseller.png)

![dimreview](/imagen/dimreview.png)

![dimorderHead](/imagen/dimorder.png)

![dimproduct](/imagen/dimproductcate.png)

![dimpayment](/imagen/dimpaymenttype.png)

![dimcalendar](/imagen/dimcalendar.png)

![dimcategoria](/imagen/dimcategoria.png)

En este caso, algunos productos no tenian especificada una categoría por lo que se optó por colocar -1 para al momento de ser actualizado realizar el cambio respectivo con las llave y nombre de categoria 

![factable](/imagen/factable.png)


