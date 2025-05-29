from requests_oauthlib import OAuth2Session

client_id = ""
client_secret = ""
redirect_uri = "http://localhost"

# Definir los alcances (permisos) necesarios
scope = ["https://www.googleapis.com/auth/userinfo.email", "https://www.googleapis.com/auth/userinfo.profile"]

# Crear sesión OAuth con el scope correcto
google = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)

authorization_url, state = google.authorization_url(
    "https://accounts.google.com/o/oauth2/auth",
    access_type="offline",
    prompt="consent"
)

print(f"Inicia sesión en: {authorization_url}")