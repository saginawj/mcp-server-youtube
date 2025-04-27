[![smithery badge](https://smithery.ai/badge/@saginawj/mcp-youtube-companion)](https://smithery.ai/server/@saginawj/mcp-youtube-companion)

# MCP YouTube Companion

An MCP tool that enables natural language interaction with your personal YouTube experience. Fetch trending videos, get recent uploads from your subscribed channels, and interact with YouTube content via your favorite LLM client.

## Overview

This MCP tool allows you to interact with YouTube through natural language queries, providing an easy way to access trending videos and user-specific content, such as recent uploads from subscribed channels, all without needing to manually interact with the YouTube API.

## Example LLM Commands

Here are some example commands you can use with your LLM client:

```python
# Fetch Trending Videos
"Show me the latest trending videos on YouTube"
"What's trending in the US on YouTube?"

# Fetch Subscribed Channel Feeds
"Show me the latest uploads from my subscribed channels"
"What's the most recent video from the 'Tech' channel?"

# User Activity
"What was my latest activity on YouTube?"
"Show me my most recent comments on videos"
"Have I uploaded anything recently?"
```

## Prerequisites

A Google account with YouTube access

YouTube API credentials (Client ID, Client Secret, and Refresh Token)


## Authentication

### Get YouTube API Credentials:

Navigate to the Google Cloud Console.

Create a project and enable the YouTube Data API v3.

Generate OAuth credentials (Client ID, Client Secret) and get your refresh token.

### Set Up OAuth Authentication:

Use/build a frontend/api that OAuth with Google to exchange an access code for a refresh token, then use the refresh token to connect with the MCP Server

