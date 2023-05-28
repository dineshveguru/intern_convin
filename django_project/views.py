from django.shortcuts import redirect
from django.http import JsonResponse
from google.oauth2 import credentials
from googleapiclient.discovery import build
import requests

from .settings import GOOGLE_API_SCOPE, GOOGLE_OAUTH_CLIENT_SECRET, GOOGLE_OAUTH_REDIRECT_URI, GOOGLE_OAUTH_CLIENT_ID


def GoogleCalendarInitView(request):
    auth_url = f"https://accounts.google.com/o/oauth2/auth?client_id={GOOGLE_OAUTH_CLIENT_ID}&redirect_uri={GOOGLE_OAUTH_REDIRECT_URI}&scope=https://www.googleapis.com/auth/calendar.readonly&response_type=code"
    return redirect(auth_url)

def GoogleCalendarRedirectView(request):
    code = request.GET.get("code")
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": GOOGLE_OAUTH_CLIENT_ID,
        "client_secret": GOOGLE_OAUTH_CLIENT_SECRET,
        "redirect_uri": GOOGLE_OAUTH_REDIRECT_URI,
        "grant_type": "authorization_code",
    }
    response = requests.post(token_url, data=data)
    token_data = response.json()
    access_token = token_data.get("access_token")

    creds = credentials.Credentials(access_token)
    service = build("calendar", "v3", credentials=creds, static_discovery=False)

    events_result = service.events().list(calendarId="primary", maxResults=10).execute()
    events = events_result.get("items", [])
    return JsonResponse({"events": events}, status=200)
