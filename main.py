from fastapi import Cookie, FastAPI
from fastapi.responses import HTMLResponse
import requests
from typing import Union

app = FastAPI()
# 99043
# b200bf015a07ca8c46ec9d2ea626c558384f5b3a

# Initial Settings
client_id = '99043'
client_secret = 'b200bf015a07ca8c46ec9d2ea626c558384f5b3a'
redirect_uri = 'http://127.0.0.1:8000/auth'

# Authorization URL
request_url = f'http://www.strava.com/oauth/authorize?client_id={client_id}' \
                  f'&response_type=code&redirect_uri={redirect_uri}' \
                  f'&approval_prompt=force' \
                  f'&scope=profile:read_all,activity:read_all'

@app.get("/")
async def root(token: Union[str, None] = Cookie(default=None)):
    ads_id: Union[str, None] = Cookie(default=None)
    activities_url = f"https://www.strava.com/api/v3/athlete/activities?" \
                     f"access_token={token}"
    response = requests.get(activities_url)
    return response.json()

@app.get("/login", response_class=HTMLResponse)
async def login():
    html_content = """
    <html>
        <head>
            <title>Workout Analytics</title>
        </head>
        <body>
            <h1>Look ma! HTML!</h1>
            <p>Please click <a href="{request_url}">here</a> to authorize access to your strava data!</p>
        </body>
    </html>
    """.format(request_url=request_url)
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/auth", response_class=HTMLResponse)
async def auth(code: str, state: str, scope: str):
    token = requests.post(url='https://www.strava.com/api/v3/oauth/token',
                          data={'client_id': client_id,
                                'client_secret': client_secret,
                                'code': code,
                                'grant_type': 'authorization_code'})

    # Save json response as a variable
    strava_token = token.json()


    html_content = """
    <html>
        <head>
            <title>Workout Analytics</title>
        </head>
        <body>
            <h1>Response</h1>
            <p>code: {code}</p>
            <p>state: {state}</p>
            <p>scope: {scope}</p>
            <p>token: {strava_token}</p>
        </body>
    </html>
    """.format(code=code,state=state,scope=scope,strava_token=strava_token)

    response = HTMLResponse(content=html_content, status_code=200)
    response.set_cookie('token', strava_token["access_token"])
    return response
