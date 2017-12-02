# Bug Report App
Reporte de errores a través de un Script CGI Perl y PHP.

# Requisitos
- Servidor web, como por ejemplo Apache 2
- BD Redis
- Cliente web (navegador)

# Instalación
Para usar el script, tan solo hay que seguir unos sencillos pasos:
- Iniciar el servidor redis

      $./redis-server ../redis.conf
      
- Introducir el script bug-report.cgi en la carpeta /cgi-bin de nuestro sistema o el script php en /var/www/html o documentRoot.
- Iniciar el servidor apache 2 o el que usemos. En caso de ejecución de PHP, tener el módulo PHP de Apache correctamente activado.

      #service apache2 start
	  
 - Dar los permisos necesarios
 
	  #chmod 644 bug-report.cgi

 - Iniciar el script mediante un cliente web.
 
# Monitoreo
Podemos monitorear mediante el cliente redis la información que se guarda gracias al script.
 
      $./redis-cli
      > MONITOR
      > OK
 
Una vez escrito monitor, redis-cli estará esperando actualiuzaciones en la bd.
