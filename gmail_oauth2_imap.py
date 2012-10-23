__author__ = 'Richie Foreman <richie.foreman@gmail.com>'

import httplib2
from oauth2client.client import SignedJwtAssertionCredentials
import imaplib

KEY = None
SERVICE_ACCOUNT_EMAIL = None
SCOPES = ["https://mail.google.com/"]
IMAP_HOST = 'imap.gmail.com'
IMAP_DEBUG_LEVEL = 0

http = httplib2.Http()

def get_credentials(**kwargs):
    '''
        Get a credentials object from a service account.
    '''
    f = file(KEY, 'rb')
    key = f.read()
    f.close()

    credentials = SignedJwtAssertionCredentials(service_account_name=SERVICE_ACCOUNT_EMAIL,
                                                private_key=key,
                                                scope=" ".join(SCOPES),
                                                **kwargs)

    authorized_http = credentials.authorize(http)
    credentials.refresh(authorized_http)
    return credentials

def GenerateOAuth2String(username, access_token):
    """
    Generates an IMAP OAuth2 authentication string.

    See https://developers.google.com/google-apps/gmail/oauth2_overview

    Args:
      username: the username (email address) of the account to authenticate
      access_token: An OAuth2 access token.
      base64_encode: Whether to base64-encode the output.

    Returns:
      The SASL argument for the OAuth2 mechanism.
    """
    auth_string = 'user=%s\1auth=Bearer %s\1\1' % (username, access_token)
    return auth_string

def get_imap_connection(prn):
    '''
    Get an OAuth2 authorized IMAP4_SSL connection

    Args:
        prn: the username (email address) of the account to authenticate

    Returns:
        IMAP4_SSL connection
    '''

    credentials = get_credentials(prn=prn)
    auth_string = GenerateOAuth2String(username=prn, access_token=credentials.access_token)

    conn = GMail_IMAP(IMAP_HOST)
    conn.debug = IMAP_DEBUG_LEVEL
    conn.authenticate('XOAUTH2', lambda x: auth_string)
    return conn

class GMail_IMAP(imaplib.IMAP4_SSL):
    # I might put stuff here later...  GMail does some cool searching stuff.
    pass