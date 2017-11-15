#!/usr/bin/perl -w

#----------------------------------------------------------------------------------------------------------------#
# Script de reporte de errores (bugs) que se importan en base de datos redis y se muestran en pantalla.          #
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
	$nombreyapellidos = $query->param('nombreyapellido'); # Guardamos el nombre en una variable
	
	print $query->br;
	print $query->br;
	print $query->label('Email: ');
	print $query->textfield(-name=>'email',
			-size =>25,
			-maxlength=>60);		
	$email = $query->param('email');
	
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
	$categoria = $query->param('categoria');
	
    print $query->br;
    print $query->br;
	print $query->label('Explica brevemente cómo ocurrió el error ');
    print $query->textfield(-name=>'datoserror',
		-override=>1,
		-default=>'Explíquenos cómo ocurrió el error aquí.',
		-size=>50,
		-maxlength=>80);
	$datoserror = $query->param('datoserror');
	print $query->br;
	print $query->br;
	print $query->submit('boton_de_envio','Enviar');
	print $query->reset;
	print $query->end_form;

    # Creamos el hash con los datos introducidos por el usuario. No sé si está bien de sintáxis #
	$redis->hmset("reportes","Error", name $nombreyapellidos email $email categoria $categoria
	datoserror $datoserror);
	
	# Probar luego en redis.cli con un HGETALL datos para comprobar si se guardan.. #


}

# Si se llama al programa con el parámetro 'admin' te permite sacar un listado de los datos por pantalla #
# No se si está bien de sintaxis #
if($query->param('admin')){
    print $query->h3('Datos de la BD Redis');
	print $query->br;
	print $query->br;
	print $query->h5($redis->hgetall("reportes"));
}

# Querría añadir que se creara un fichero de texto con todos los datos del hash creado en la bd redis, pero he 
# buscado documentación y no encuentro nada al respecto.
