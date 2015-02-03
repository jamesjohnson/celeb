import instagram
import argparse

INSTAGRAM_KEY = "98b8b06e4cb84826ac625c384c2a3d5d"
INSTAGRAM_SECRET = "4ae0fc9f44bc422d857597131d9457e8"
REDIRECT_URL = "http://localhost:8515/oauth_callback"
SCOPE = ('basic', 'comments', 'relationships', 'likes')

def get_api(access_token=None):
    if access_token is not None:
        # authenticated api
        return InstagramAPI(access_token=access_token)
    else:
        # unauthenticated api
        return instagram.client.InstagramAPI(client_id=INSTAGRAM_KEY,
                            client_secret=INSTAGRAM_SECRET,
                            redirect_uri=REDIRECT_URL)

def signin():
    api = get_api()
    redirect_uri = api.get_authorize_login_url(scope=SCOPE)
    print redirect_uri

def exchange(code):
    unauthenticated_api = get_api()
    access_token, instagram_user = (unauthenticated_api.exchange_code_for_access_token(code))
    print access_token


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--code', action='store_true')
    args = parser.parse_args()

    if args.code:
        exchange("0ee1a1bc5213483cbc791a4591a1e5c5")
    else:
        signin()
