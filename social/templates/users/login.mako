<%inherit file="/base.mako" />
${c.message}
<form method="POST">
<div><label for="login">Login:</label><input name="login" /></div>
<div><label for="passwd">Hasło:</label><input name="passwd" type="password" /></div>
<input type="submit" />
</form>
