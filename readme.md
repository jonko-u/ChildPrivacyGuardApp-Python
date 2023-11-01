
# Guardian of Innocence: Protecting Children Through Secure Memories

![Screenshot](/screenshots/screenshot1.jpg)



**Introducción:**

En la actualidad, en Europa y específicamente en España, la Ley Orgánica 3/2018 de Protección de Datos Personales y garantía de los derechos digitales es una normativa fundamental. Esta ley establece directrices y salvaguardias para la protección de la privacidad y los derechos digitales de los ciudadanos, en un contexto donde la información personal es cada vez más valiosa y vulnerable a exposiciones no deseadas.

**Problema:**

Uno de los escenarios en los que esta ley plantea desafíos es en las instituciones infantiles, donde los profesores a menudo capturan momentos especiales a través de fotografías. Estas imágenes suelen ser compartidas en plataformas de terceros, como Google Drive, en las cuales la gestión de la privacidad y el control sobre las imágenes pueden ser limitados. Esto plantea preocupaciones de seguridad y privacidad, especialmente cuando se trata de datos personales de niños.

**El Proyecto:**

Para abordar estos desafíos, se ha desarrollado un proyecto con varios objetivos clave:

1. **Autenticación de Profesores:** Se ha implementado un sistema de autenticación que permite a los profesores iniciar sesión. Esto garantiza que solo personal autorizado tenga acceso a la plataforma.

2. **Almacenamiento Seguro de Fotos:** Las fotos se cargan en la plataforma y se cifran para garantizar su seguridad y privacidad. Se almacenan en una base de datos NoSQL MongoDB, lo que facilita su gestión y recuperación.

3. **Reconocimiento Facial:** Se ha incorporado un sistema de reconocimiento facial que permite a los padres y usuarios finales solicitar ver las fotos originales. Esta característica añade una capa adicional de seguridad al proceso.

4. **Autenticación de Usuarios Finales:** Para acceder a las fotos originales, se requiere una autenticación adicional a través de un código temporal de 6 dígitos enviado a los dispositivos móviles personales de los usuarios. Esto garantiza que solo los destinatarios autorizados puedan ver las imágenes.

5. **Registro de Accesos:** Cada solicitud y acceso a las imágenes queda registrado, lo que proporciona un rastro de auditoría para garantizar la trazabilidad y responsabilidad en caso de incidentes.

6. **Marcas de Agua y Metadatos:** Se incorporan marcas de agua en las imágenes y se registran metadatos, como la dirección IP de la persona que accede a las imágenes. Esto proporciona evidencia adicional en caso de un mal uso de las fotos.

**Conclusión:**

Este proyecto demuestra la capacidad de Python como una poderosa herramienta para abordar cuestiones de ciberseguridad y privacidad. A través de la implementación de prácticas sólidas de cifrado, autenticación y registro, se garantiza la confidencialidad y la integridad de las imágenes en un entorno sensible como el de las instituciones infantiles. Además, se promueven prácticas que cumplen con las regulaciones de protección de datos y derechos digitales, como la Ley Orgánica 3/2018 en España. Este enfoque proporciona un equilibrio necesario entre la accesibilidad y la seguridad, garantizando que las imágenes de los niños se gestionen de manera segura y con el respeto que merecen sus derechos digitales.
## Features



-    Almacenamiento Seguro de Fotos: Tu proyecto proporciona un entorno seguro para almacenar fotos, aprovechando MongoDB y GridFS para garantizar la privacidad de los datos.

-    Reconocimiento Facial: Incorporas la tecnología de reconocimiento facial para mejorar la seguridad, permitiendo a usuarios autorizados acceder a imágenes originales mientras proteges la privacidad.

-    Autenticación de Dos Factores (2FA): Los usuarios pueden acceder de forma segura a imágenes originales al recibir una contraseña TOTP temporal (contraseña de un solo uso basada en tiempo) a través de SMS, agregando una capa adicional de seguridad.

-    Cifrado: Las fotos se cifran antes de almacenarse en MongoDB utilizando el cifrado Fernet, lo que garantiza la confidencialidad de los datos.

-    Seguimiento de Metadatos: La aplicación realiza un seguimiento del acceso a las imágenes al incrustar direcciones IP de usuarios en los metadatos de la imagen, lo que permite la trazabilidad.

-    Autenticación de Usuarios: Los profesores y padres tienen inicios de sesión personalizados que les proporcionan acceso a funciones específicas y garantizan la integridad de los datos.

-    SQLite: Utilizas una base de datos relacional SQLite para la gestión de inicio de sesión de usuarios.

-    Marca de Agua en Imágenes: Las imágenes tienen marcas de agua que muestran las direcciones IP de los usuarios, lo que proporciona una capa adicional de seguridad contra el acceso no autorizado.

-    Scripting en el Lado del Servidor: Implementado con Python y el framework Flask, lo que garantiza una funcionalidad sólida de la aplicación y seguridad.

-    Variables de Entorno (dotenv): Utilizas variables de entorno para el almacenamiento seguro de datos de configuración sensibles.

-    Bibliotecas de Python: Aprovechas bibliotecas como Pillow (PIL), NumPy y otras para el procesamiento de imágenes, el reconocimiento facial y funciones criptográficas.

## Future features
-    Aplicación Web Adaptable: La aplicación ofrece una interfaz web amigable que se adapta a diversos dispositivos y tamaños de pantalla.

-    Integración de SMS: Integración de servicios de SMS para enviar de manera segura contraseñas TOTP temporales a los teléfonos móviles de los padres.


## Endpoints


```bash
    /dashboard (POST): Este endpoint se utiliza para que los usuarios, en este caso, los profesores, puedan subir una foto a la base de datos. Es parte de la funcionalidad de carga de imágenes al sistema.

    /get_client_ip (GET): Esta ruta permite a los usuarios obtener la dirección IP del cliente que accede al sistema. Puede ser útil para rastrear y auditar el acceso de los usuarios.

    /picture_process (POST): Aquí se realiza el procesamiento de una imagen. Esta ruta se utiliza para aplicar operaciones como el reconocimiento facial y la posterior encriptación de la imagen antes de almacenarla en la base de datos.

    /display_pictures: En este endpoint, se muestran las imágenes almacenadas en la base de datos. Los usuarios pueden acceder y visualizar las imágenes guardadas.

    /get_original_picture (POST): Permite a los usuarios, generalmente padres, solicitar ver una imagen original. Para acceder a la imagen original, deben proporcionar información adicional, como una contraseña TOTP.

    /check_totp (POST): Esta ruta se utiliza para verificar la contraseña TOTP (Time-Based One-Time Password) proporcionada por los padres. La aplicación valida la contraseña antes de mostrar la imagen original.
```
    
## Usage/Examples

```
pip install -r "requirements.txt"

python run.py
```
