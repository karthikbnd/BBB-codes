<html>
<head>
<title>BeagleBone LED Changer</title>
<style type="text/css">
	p { display: table-cell; }
	button { width: 75px; margin: 2px auto; }
</style>
<?php
	if (isset($_GET['led']) && isset($_GET['onOff']))
	{
		$led = $_GET['led'];
		$onOff = $_GET['onOff'];

		exec( "/var/www/cgi-bin/ledctl $led $onOff" );
	}
?>
</head>
<body>
<div style="width: 200px; margin: 0px auto;">
	<div style="width: 100px; float: left;">
		<p>LED #0:</p>
		<button type="button" onclick="location.href='ledctl.php?led=0&onOff=1'">ON</button>
		<button type="button" onclick="location.href='ledctl.php?led=0&onOff=0'">OFF</button>
	</div>
	<div sytle="width: 100px; margin-left: 100px;">
		<p>LED #1:</p>
		<button type="button" onclick="location.href='ledctl.php?led=1&onOff=1'">ON</button>
		<button type="button" onclick="location.href='ledctl.php?led=1&onOff=0'">OFF</button>
	</div>
</div>
</body>
</html>
