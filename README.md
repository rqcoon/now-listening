# Now Listening API

## Overview
A lightweight Spotify-powered API that exposes the currently playing track of an authenticated user.

This is a small self-hosted microservice designed to be embedded as a widget.

The API authenticates with Spotify via OAuth and provides a simple endpoint that returns the current playback state and track metadata
in JSON format.

## Features
- Spotify OAuth authentication
- Track lookup via Spotify web API
- Lightweight FastAPI backend
- Dockerized deployment
- HTTPS-Ready with Nginx reverse proxy
- Frontend-agnostic JSON API