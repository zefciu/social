# vim set fileencoding=utf-8
<%inherit file="/base.mako" />
Aby zobaczyć tablicę tego użytkownika musisz zostać jego przyjacielem:
<form action="${url(controller = 'users', action = 'befriend', login=c.login)}" method="POST">
<input type="submit" text="Zaprzyjaźnij się"/>
</form>
