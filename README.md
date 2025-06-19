# Project Alice - Roblox AI LLM

**Alice** is a Roblox AI NPC that leverages a powerful cloud-hosted large language model (LLM) backend for intelligent conversations and interactions within Roblox games.

---

## Overview

Alice communicates with Roblox through the built-in `HttpService`, sending and receiving JSON requests to an OpenRouter-compatible API. The AI backend originally ran on Render and Replit but has since migrated to Railway for more stable and scalable hosting.

The language model used is the `deepseek/deepseek-r1-0528-qwen3-8b:free` from OpenRouter, enabling advanced conversational abilities within your Roblox experience.

---

## Features

- Real-time chat interactions with players in Roblox via NPC chat bubbles.
- Uses the `deepseek-r1-0528-qwen3-8b` model hosted on OpenRouter.
- Backend hosted on Railway for uptime and reliability.
- Communication handled via Roblox `HttpService` with JSON.
- Easily extensible to add new behaviors or responses.

---

## Architecture


- **Roblox Client/Server**: Sends user messages and receives AI responses.
- **Backend Server**: Manages API requests and responses, hosted on Railway.
- **OpenRouter API**: Processes natural language requests using the deepseek LLM model.

---

## Setup & Deployment

### Prerequisites

- A Roblox game with scripting access.
- Railway account to host the backend server.
- OpenRouter API key for accessing the `deepseek-r1-0528-qwen3-8b` model.
- Basic knowledge of Lua scripting and backend development.

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/roblox-alice-ai.git
   cd roblox-alice-ai
