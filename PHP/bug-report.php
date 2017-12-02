<!DOCTYPE html>
<html>
<head>
	<title>Bug-Report App</title>
	<meta charset="utf-8">
</head>
<body>
	<?php 
	$redis = new Redis();
 	$redis -> pconnect("localhost");
	$cont = $redis->hlen("reportes"); #Determina cuantos reportes se han enviado/creado en la db redis, un length de la bd
	if(!isset($_POST['submit'])) { ?>
		<h2>Envío de reportes.</h2>
		<form method="POST">
			<label>Tu nombre: </label>
			<input type="text" name="nombreyapellido"><br>
			<label>Email: </label>
			<input type="email" name="email"><br>
			<label>Categoría del error: </label>
			<select name="categoria">
				<option value="conexion">Error de conexión</option>
				<option value="codigo">Error de código</option>
				<option value="seguridad">Error de seguridad</option>
				<option value="redireccion">Error de redirección</option>
				<option value="diseñoestilos">Error de diseño/estilos</option>
				<option value="pagos">Error en la pasarela de pagos</option>
				<option value="otro">Otro error</option>
			</select><br>
			<label>Explica brevemente cómo ocurrió el error: </label>
			<textfield name="datoserror"></textfield><br>
			<input type="submit" name="enviar" value="Enviar">
			<input type="reset" name="reset" value="Borrar">
		</form>
	<?php } else {
	  $nombreyapellido = $_POST['nombreyapellido'];
	  $email = $_POST['email'];
	  $categoria = $_POST['categoria'];
	  $datoserror = $_POST['datoserror'];
	  $redis->hgetall('reportes');
	  if($nombreyapellido == 'admin') { ?>
			<h3>Datos de la BD Redis</h3>
		  <?php
			echo "<h5>Se han añadido $cont reportes a la BD</h5><br><br><br>"
		   
			echo "<h5>$redis</h5>"
		  }
		  // Imprimimos el fichero reporte.txt
		  $content = $nombreyapellido . ':' . $email . ';' . $categoria . ':' .  $datoserror . "\n";
		  $lines = file_get_contents("/tmp/reporte.txt");
		  if ($lines == false) {	// Si el fichero no existe, lo creamos!
			  file_put_contents("/tmp/reporte.txt",$content,FILE_APPEND);
		  }
		  echo $lines;
		 ?>
	<?php
	$cont++;
	# Creamos el hash con los datos introducidos por el usuario, con una estructura (':') accesible para otras apps #
	   $redis->hset("reportes","Error: $cont", "$nombreyapellido:$email:$categoria[0]:$datoserror");
	   file_put_contents("/tmp/reporte.txt",$content,FILE_APPEND);
	 ?>
</body>
</html>