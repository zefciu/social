<%inherit file="/base.mako" />
<form method="POST">
<div><label for="login">Login:</label><input name="login" /></div>
<div><label for="passwd">Hasło:</label><input name="passwd" type="password" /></div>
<div><label for="repeatPasswd">Powtórz hasło:</label><input name="repeatPasswd" type="password" /></div>
<input type="submit" />
</form>
