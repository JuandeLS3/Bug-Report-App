#!/usr/bin/perl -w

#----------------------------------------------------------------------------------------------------------------#
# Script de reporte de errores (bugs) que se importan en una BD redis, fichero y muestra en pantalla             #
# Creado por Juan Delgado Salmerón                                                                               #
#----------------------------------------------------------------------------------------------------------------#

# Importamos librerías necesarias y creamos objeto CGI y objeto redis para la conexión #

use CGI;
use Redis;
use Encode;
$query = CGI->new;
$redis = Redis->new;
$cont=$redis->hlen("reportes"); #Determina cuantos reportes se han enviado/creado en la db redis, un length de la bd

# Imprimimos DDT #

print $query->header(-charset => 'utf8');

# Damos un título a nuestro html #

print $query->start_html('Envío de reportes');

# Si se llama al programa sin NINGÚN parámetro, se imprime el formulario #

if (!$query->param) {
	print $query->start_form;
	print $query->h2('Envío de reportes.');
	print $query->label('Tu nombre: ');
	print $query->textfield(-name=>'nombreyapellido',
			-size=>25,
			-maxlength=>50);
	
	print $query->br;
	print $query->br;
	print $query->label('Email: ');
	print $query->textfield(-name=>'email',
			-size =>25,
			-maxlength=>60);		
	
	print $query->br;
	print $query->br;
	print $query->label('Categoría del error: ');
	print $query->scrolling_list(-name=>'categoria',
					 -values=>[
						   'Error de conexión',
						   'Error de código',
						   'Error de seguridad',
						   'Error de redirección',
						   'Error de diseño/estilos',
						   'Error en la pasarela de pagos',
						   'Otro error'],
					 -size=>7,
					 -multiple=>'false',
					 -default=>'Otro error');
	
    print $query->br;
    print $query->br;
    print $query->label('Explica brevemente cómo ocurrió el error ');
    print $query->textfield(-name=>'datoserror',
		-override=>1,
		-default=>'Explíquenos cómo ocurrió el error aquí.',
		-size=>50,
		-maxlength=>80);
	print $query->br;
	print $query->br;
	print $query->submit('boton_de_envio','Enviar');
	print $query->reset;
	print $query->end_form;
} else {
	$nombreyapellido = $query->param('nombreyapellido');
    # Si se llama al programa con el parámetro 'admin' te permite sacar un listado de los datos por pantalla #
    if ($nombreyapellido eq 'admin') {
        print $query->h3('Datos de la BD Redis');
	    print $query->h5("Se han añadido " . $cont . " reportes a la BD");
	    print $query->br;
	    print $query->br;
	    print $query->h5($redis->hgetall("reportes"));
	    print $query->br;

	    # Imprimirá por pantalla los erorres del fichero reporte.txt #
            print $query->h3('Datos del fichero /tmp/reporte.txt');
	    open F, '/tmp/reporte.txt' or die "ERR: El archivo no se puede abrir:$!";
		while(<F>) {
			print "$_ <br>";
		}
		close F;
		# Si no se le llama con el parámetro admin, generará el fichero reportes y creará el hash en redis #
    } else {
		@categoria = $query->param('categoria');
		$datoserror = $query->param('datoserror');
		$email = $query->param('email');
		# Creamos el hash con los datos introducidos por el usuario, con una estructura (':') accesible para otras apps #
                $cont++;
		$redis->hset("reportes","Error:$cont","$nombreyapellido:$email:$categoria[0]:$datoserror");
		# Sobreescribimos/Creamos fichero reporte con los datos introducidos en el formulario. #
		open F, '>>/tmp/reporte.txt' or die "ERR: El archivo no se puede abrir:$!";
		print F "$nombreyapellido:$email:$categoria[0]:$datoserror \n";
		close F; 
	}
}
