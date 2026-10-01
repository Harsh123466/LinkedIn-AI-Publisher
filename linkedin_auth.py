import os
import urllib.parse
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
import requests

load_dotenv()

app = FastAPI()

CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID")
REDIRECT_URI = os.getenv("LINKEDIN_REDIRECT_URI")

AUTHORIZATION_URL = "https://www.linkedin.com/oauth/v2/authorization"


@app.get("/login")
def login():

    params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": "openid profile email w_member_social"
    }

    url = AUTHORIZATION_URL + "?" + urllib.parse.urlencode(params)

    return RedirectResponse(url)


@app.get("/callback")
def callback(code: str):

    token_url = "https://www.linkedin.com/oauth/v2/accessToken"

    data = {
        "grant_type": "authorization_code",
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": os.getenv("LINKEDIN_CLIENT_SECRET"),
        "redirect_uri": REDIRECT_URI,
    }

    response = requests.post(
        token_url,
        data=data
    )

    print(code)

    if response.status_code != 200:
        return {
            "success": False,
            "error": response.text
        }

    token_data = response.json()

    access_token = token_data.get("access_token")

    if not access_token:
        return {
            "success": False,
            "error": "Access token was not returned."
        }

    # Test the access token
    userinfo_response = requests.get(
        "https://api.linkedin.com/v2/userinfo",
        headers={
            "Authorization": f"Bearer {access_token}"
        }
    )

    if userinfo_response.status_code != 200:
        return {
            "success": False,
            "error": userinfo_response.text
        }

    userinfo = userinfo_response.json()
    member_id = userinfo.get("sub")

    with open(".env", "a", encoding="utf-8") as f:
        f.write(f'\nLINKEDIN_ACCESS_TOKEN="{access_token}"\n')
        f.write(f'LINKEDIN_MEMBER_ID="{member_id}"\n')

    return {
        "success": True,
        "message": "LinkedIn authentication successful!",
        "member_name": userinfo.get("name"),
        "member_id": member_id,
        "expires_in": token_data.get("expires_in"),
        "scope": token_data.get("scope")
    }