from authlib.integrations.starlette_client import OAuth
# this file is for  Google OAuth / OpenID Connect client configuration.
from core.config import settings

# Authlib OAuth client used to communicate with Google OAuth servers.
oauth = OAuth() # creates a oauth client

# oauth -> authorization and openid connect oidc -> authentication 
# when we request openid google knows this application needs info too that allows google to issue id token which has name email pic subjid

oauth.register( # it registers google as an oauth.openid connect provider
    name="google",
    client_id=settings.GOOGLE_CLIENT_ID, # this appliaction is remindr. since google has milion of apps so how does it now this login request belong to remindr
    client_secret=settings.GOOGLE_CLIENT_SECRET, # if attacker says i am remindr so client secret proves this application is really remindr, our backend knows this only not even frontend
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration", # instead of manually writing authorization , user , toekn url.
                            # google publishes OpenID configuration , authlib downlaod everything automatically
    client_kwargs={
        "scope": ( # our app requests openid, emails, profile , readonly permissions
            "openid "
            "email "
            "profile "
            "https://www.googleapis.com/auth/gmail.readonly"
        )
    },
)