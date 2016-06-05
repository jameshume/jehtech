<?php
require_once('recaptchalib.php');

// OPTIONS - PLEASE CONFIGURE THESE BEFORE USE!

$yourEmail = "james.hume@gmail.com"; // the email address you wish to receive these mails through
$yourWebsite = "http://www.jeh-tech.com"; // the name of your website
$thanksPage = ''; // URL to 'thanks for sending mail' page; leave empty to keep message on the same page 
$maxPoints = 4; // max points a person can hit before it refuses to submit - recommend 4
$requiredFields = "name,email,comments"; // names of the fields you'd like to be required as a minimum, separate each field with a comma


// DO NOT EDIT BELOW HERE
$error_msg = array();
$result = null;

$requiredFields = explode(",", $requiredFields);

function clean($data) {
	$data = trim(stripslashes(strip_tags($data)));
	return $data;
}
function isBot() {
	$bots = array("Indy", "Blaiz", "Java", "libwww-perl", "Python", "OutfoxBot", "User-Agent", "PycURL", "AlphaServer", "T8Abot", "Syntryx", "WinHttp", "WebBandit", "nicebot", "Teoma", "alexa", "froogle", "inktomi", "looksmart", "URL_Spider_SQL", "Firefly", "NationalDirectory", "Ask Jeeves", "TECNOSEEK", "InfoSeek", "WebFindBot", "girafabot", "crawler", "www.galaxy.com", "Googlebot", "Scooter", "Slurp", "appie", "FAST", "WebBug", "Spade", "ZyBorg", "rabaz");

	foreach ($bots as $bot)
		if (stripos($_SERVER['HTTP_USER_AGENT'], $bot) !== false)
			return true;

	if (empty($_SERVER['HTTP_USER_AGENT']) || $_SERVER['HTTP_USER_AGENT'] == " ")
		return true;
	
	return false;
}

if ($_SERVER['REQUEST_METHOD'] == "POST") {
	if (isBot() !== false)
		$error_msg[] = "No bots please! UA reported as: ".$_SERVER['HTTP_USER_AGENT'];
		
	// lets check a few things - not enough to trigger an error on their own, but worth assigning a spam score.. 
	// score quickly adds up therefore allowing genuine users with 'accidental' score through but cutting out real spam :)
	$points = (int)0;
	
	$badwords = array("adult", "beastial", "bestial", "blowjob", "clit", "cum", "cunilingus", "cunillingus", "cunnilingus", "cunt", "ejaculate", "fag", "felatio", "fellatio", "fuck", "fuk", "fuks", "gangbang", "gangbanged", "gangbangs", "hotsex", "hardcode", "jism", "jiz", "orgasim", "orgasims", "orgasm", "orgasms", "phonesex", "phuk", "phuq", "pussies", "pussy", "spunk", "xxx", "viagra", "phentermine", "tramadol", "adipex", "advai", "alprazolam", "ambien", "ambian", "amoxicillin", "antivert", "blackjack", "backgammon", "texas", "holdem", "poker", "carisoprodol", "ciara", "ciprofloxacin", "debt", "dating", "porn", "link=", "voyeur", "content-type", "bcc:", "cc:", "document.cookie", "onclick", "onload", "javascript");

	foreach ($badwords as $word)
		if (
			strpos(strtolower($_POST['comments']), $word) !== false || 
			strpos(strtolower($_POST['name']), $word) !== false
		)
			$points += 2;
	
	if (strpos($_POST['comments'], "http://") !== false || strpos($_POST['comments'], "www.") !== false)
		$points += 2;
	if (isset($_POST['nojs']))
		$points += 1;
	if (preg_match("/(<.*>)/i", $_POST['comments']))
		$points += 2;
	if (strlen($_POST['name']) < 3)
		$points += 1;
	if (strlen($_POST['comments']) < 15 || strlen($_POST['comments'] > 1500))
		$points += 2;
	if (preg_match("/[bcdfghjklmnpqrstvwxyz]{7,}/i", $_POST['comments']))
		$points += 1;
	// end score assignments

	foreach($requiredFields as $field) {
		trim($_POST[$field]);
		
		if (!isset($_POST[$field]) || empty($_POST[$field]) && array_pop($error_msg) != "Please fill in all the required fields and submit again.\r\n")
			$error_msg[] = "Please fill in all the required fields and submit again.";
	}

	if (!empty($_POST['name']) && !preg_match("/^[a-zA-Z-'\s]*$/", stripslashes($_POST['name'])))
		$error_msg[] = "The name field must not contain special characters.\r\n";

	if (!empty($_POST['email']) && !preg_match('/^([a-z0-9])(([-a-z0-9._])*([a-z0-9]))*\@([a-z0-9])(([a-z0-9-])*([a-z0-9]))+' . '(\.([a-z0-9])([-a-z0-9_-])?([a-z0-9])+)+$/i', strtolower($_POST['email'])))
		$error_msg[] = "That is not a valid e-mail address.\r\n";

	if (empty($_POST['email2']) || ($_POST['email'] != $_POST['email2']))
		$error_msg[] = "Email addresses do not match.\r\n";

	if(!isset($_POST['g-recaptcha-response']))
		$error_msg[] = "Please check the reCAPTCHA button to verify you are not a robot :)\r\n";

	$response = 
		json_decode(
			file_get_contents("https://www.google.com/recaptcha/api/siteverify".
			                     "?secret=6LfjlQITAAAAAOEfDheCrsk83J0SgPZ6BUNVMWGp".
			                     "&response=".$_POST['g-recaptcha-response'].
			                     "&remoteip=".$_SERVER['REMOTE_ADDR']), 
			                  true);

	if($response['success'] == false)
		$error_msg[] = "Could not validate your reCAPTCHA. Are you a robot? ;)\r\n";
	
	if ($error_msg == NULL && $points <= $maxPoints) {
		$subject = "Automatic Form Email";
		
		$message = "You received this e-mail message through your website: \n\n";
		foreach ($_POST as $key => $val) {
			if (is_array($val)) {
				foreach ($val as $subval) {
					$message .= ucwords($key) . ": " . clean($subval) . "\r\n";
				}
			} else {
				$message .= ucwords($key) . ": " . clean($val) . "\r\n";
			}
		}
		$message .= "\r\n";
		$message .= 'IP: '.$_SERVER['REMOTE_ADDR']."\r\n";
		$message .= 'Browser: '.$_SERVER['HTTP_USER_AGENT']."\r\n";
		$message .= 'Points: '.$points;

		if (strstr($_SERVER['SERVER_SOFTWARE'], "Win")) {
			$headers   = "From: $yourEmail\r\n";
		} else {
			$headers   = "From: $yourWebsite <$yourEmail>\r\n";	
		}
		$headers  .= "Reply-To: {$_POST['email']}\r\n";

		if (mail($yourEmail,$subject,$message,$headers)) {
			if (!empty($thanksPage)) {
				header("Location: $thanksPage");
				exit;
			} else {
				$result = 'Your mail was successfully sent.';
				$disable = true;
			}
		} else {
			$error_msg[] = 'Your mail could not be sent this time. ['.$points.']';
		}
	} else {
		if (empty($error_msg))
			$error_msg[] = 'Your mail looks too much like spam, and could not be sent this time. ['.$points.']';
	}
}
function get_data($var) {
	if (isset($_POST[$var]))
		echo htmlspecialchars($_POST[$var]);
}
?>
<!DOCTYPE HTML>
<html>
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8"> <!-- HTML 4 -->
	<meta charset="UTF-8">                                              <!-- HTML 5 -->
	<title>Contact JEH-Tech</title>
	<!-- META_INSERT -->
	<!-- CSS_INSERT -->
	<!-- JAVASCRIPT_INSERT -->

	<script src='https://www.google.com/recaptcha/api.js'></script>

	<style type="text/css">
		p.error, p.success {
			font-weight: bold;
			padding: 10px;
			border: 1px solid;
		}
		p.error {
			background: #ffc0c0;
			color: #900;
		}
		p.success {
			background: #b3ff69;
			color: #4fa000;
		}
	</style>
</head>


<body>
<!--
	The PHP mailing form has been based on the Free PHP Mail Form by Jem Turner:


	Free PHP Mail Form v2.4.4 - Secure single-page PHP mail form for your website
	Copyright (c) Jem Turner 2007-2014
	http://jemsmailform.com/

	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	To read the GNU General Public License, see http://www.gnu.org/licenses/.
-->
	<div id="header">
		-- This is JEHTech --
	</div>

	<div id="sidebar">
		<h1 class="title">Links...</h1>
		<div id="includedContent"></div>
	</div>

	<div id="content">
		<h1 class="title">Contact JEH-Tech</h1>

<?php
if (!empty($error_msg)) {
	echo '<p class="error">ERROR: '. implode("<br />", $error_msg) . "</p>";
}
if ($result != NULL) {
	echo '<p class="success">'. $result . "</p>";
}
?>

		<p>Seen and error or want to comment? Please keep it polite and constructive...</p>
		<form action="<?php echo basename(__FILE__); ?>" method="post">
			<noscript>
				<p><input type="hidden" name="nojs" id="nojs" /></p>
			</noscript>
			<table style="border:0px;">
				<tr><td>Name:</td><td><input type="text" name="name" id="name" value="<?php if ($_SERVER['REQUEST_METHOD'] == "POST") echo $_POST['name'] ?>">
					</input></td></tr>
				<tr><td>Email:</td><td><input type="text" name="email" id="email" value="<?php if ($_SERVER['REQUEST_METHOD'] == "POST") echo $_POST['email'] ?>">
					</input></td></tr>
				<tr><td>Confirm:</td><td><input type="text" name="email2" id="email2" value="<?php if ($_SERVER['REQUEST_METHOD'] == "POST") echo $_POST['email2'] ?>">
					</input></td></tr>
				<tr><td>Message:</td><td><textarea cols="80" rows="10" name="comments" id="comments">
<?php if ($_SERVER['REQUEST_METHOD'] == "POST") echo $_POST['comments'] ?>
					</textarea></td></tr>
<?php if(!isset($disable) || $disable !== true): ?>
				<tr><td></td><td><div class="g-recaptcha" data-sitekey="6LfjlQITAAAAAPlP-_LjYellMnMRynxwIVFLT5gV"></div></td></tr>
				<tr><td colspan="2">
					<input type="submit" name="submit" id="submit" value="Send" />
				</td><tr>
<?php endif; ?>
			</table>
		</form>
		<p>Powered by <a href="http://jemsmailform.com/">Jem's PHP Mail Form</a></p>
	</div>
</body>
</html>
