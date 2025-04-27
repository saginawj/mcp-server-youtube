import os
import logging
from typing import Optional
from dotenv import load_dotenv
import aiohttp
from fastmcp import FastMCP
from rich.console import Console

# Load environment variables
load_dotenv()

console = Console()

# Set logging level
logging.basicConfig(level=logging.WARNING)

# Initialize MCP server
mcp = FastMCP("YouTube MCP")

# === Client Helper ===
async def get_youtube_client() -> aiohttp.ClientSession:
    """
    Creates an authenticated YouTube API client using the refresh token.
    No username/password is needed.
    """
    logger = logging.getLogger(__name__)

    refresh_token = os.getenv("YOUTUBE_REFRESH_TOKEN")
    client_id = os.getenv("YOUTUBE_CLIENT_ID")
    client_secret = os.getenv("YOUTUBE_CLIENT_SECRET")

    if not all([refresh_token, client_id, client_secret]):
        logger.error("❌ Missing required YouTube OAuth credentials.")
        raise ValueError("YOUTUBE_REFRESH_TOKEN, CLIENT_ID, and CLIENT_SECRET are all required.")

    logger.info("🔐 Using YouTube OAuth via refresh_token")

    # Refresh the token to get the access token
    token_data = await refresh_youtube_token(client_id, client_secret, refresh_token)

    access_token = token_data['access_token']
    session = aiohttp.ClientSession()
    return session, access_token

async def refresh_youtube_token(client_id: str, client_secret: str, refresh_token: str) -> dict:
    """Refresh the YouTube access token using the provided refresh token."""
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }
    async with aiohttp.ClientSession() as session:
        async with session.post("https://oauth2.googleapis.com/token", data=data) as response:
            if response.status != 200:
                error_text = await response.text()
                console.print(f"[red]Failed to refresh YouTube token: {error_text}[/red]")
                raise Exception(f"Failed to refresh token: {error_text}")
            return await response.json()

# === Helper Functions ===

def format_video(video) -> str:
    """Format YouTube video data for display."""
    return (
        f"Title: {video['snippet']['title']}\n"
        f"Channel: {video['snippet']['channelTitle']}\n"
        f"Published: {video['snippet']['publishedAt']}\n"
        f"Description: {video['snippet'].get('description', '')[:200]}...\n"
        f"Link: https://www.youtube.com/watch?v={video['id']}\n---"
    )

# === Tools ===

@mcp.tool()
async def get_trending_videos(region_code="US", max_results=30) -> str:
    """Fetch trending YouTube videos."""
    session, access_token = await get_youtube_client()

    url = "https://youtube.googleapis.com/youtube/v3/videos"
    params = {
        "part": "snippet",
        "chart": "mostPopular",
        "regionCode": region_code,
        "maxResults": max_results
    }
    headers = {"Authorization": f"Bearer {access_token}"}

    async with session.get(url, headers=headers, params=params) as response:
        if response.status != 200:
            error_text = await response.text()
            console.print(f"[red]Error fetching trending videos: {error_text}[/red]")
            return f"Error: {error_text}"

        data = await response.json()
        videos = data.get("items", [])
        return "\n".join([format_video(video) for video in videos])

@mcp.tool()
async def get_subscribed_channels(max_channels=10) -> str:
    """Fetch the most recent uploads from subscribed YouTube channels."""
    session, access_token = await get_youtube_client()

    url = "https://youtube.googleapis.com/youtube/v3/subscriptions"
    params = {
        "part": "snippet",
        "mine": "true",
        "maxResults": max_channels
    }
    headers = {"Authorization": f"Bearer {access_token}"}

    async with session.get(url, headers=headers, params=params) as response:
        if response.status != 200:
            error_text = await response.text()
            console.print(f"[red]Error fetching subscriptions: {error_text}[/red]")
            return f"Error: {error_text}"

        data = await response.json()
        channels = data.get("items", [])
        return "\n".join([f"Channel: {channel['snippet']['title']}" for channel in channels])

@mcp.tool()
async def get_user_activity(max_results=10) -> str:
    """Fetch the most recent activity from the authenticated user."""
    session, access_token = await get_youtube_client()

    url = "https://youtube.googleapis.com/youtube/v3/activity"
    params = {
        "part": "snippet,contentDetails",
        "mine": "true",
        "maxResults": max_results
    }
    headers = {"Authorization": f"Bearer {access_token}"}

    async with session.get(url, headers=headers, params=params) as response:
        if response.status != 200:
            error_text = await response.text()
            console.print(f"[red]Error fetching user activity: {error_text}[/red]")
            return f"Error: {error_text}"

        data = await response.json()
        activities = data.get("items", [])
        return "\n".join([f"Activity: {activity['snippet']['title']}" for activity in activities])

# === Entry Point ===

if __name__ == "__main__":
    mcp.run(transport="stdio")
