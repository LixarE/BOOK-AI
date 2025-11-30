# AI Ebook Generator

A full-stack AI-powered application that generates comprehensive PDF ebooks on any topic using a multi-agent workflow.

## Features

- 🔍 **Web Search**: Gathers real-time information using DuckDuckGo
- 🧠 **AI Analysis**: Structures content using Gemini 2.5 Flash
- 🎨 **Image Generation**: Creates diagrams and graphs using Gemini
- 📝 **Professional Formatting**: Styles content into book layout
- 📄 **PDF Creation**: Generates downloadable PDFs
- ✅ **Verification**: Ensures PDF quality with retry logic (max 3 attempts)
- 🌐 **Modern UI**: React frontend with real-time progress tracking
- 🔌 **MCP Integration**: Model Context Protocol server for AI agent integration

## Architecture

### Backend (Python/FastAPI)
- **Multi-Agent System**: Search, Analyst, Image, Formatter, PDF, Verifier agents
- **API**: RESTful API on port 8000
- **MCP Server**: Exposes `generate_ebook` tool for AI agents

### Frontend (React/Vite)
- **Modern UI**: Built with React and Vite
- **Real-time Updates**: Progress tracking and logs
- **Responsive Design**: Dark theme with animations

## Prerequisites

- Python 3.13+
- Node.js 24+
- Gemini API Key

## Installation

### 1. Clone and Setup

```bash
cd "Ag_3"
```

### 2. Backend Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt
```

### 3. Frontend Setup

```bash
cd frontend
npm install
cd ..
```

### 4. Configure API Key

Edit `backend/.env`:
```
GEMINI_API_KEY=your-api-key-here
```

## Running the Application

### Start Backend (Terminal 1)

```bash
source venv/bin/activate
uvicorn backend.main:app --host 0.0.0.0 --port 8000
```

### Start Frontend (Terminal 2)

```bash
cd frontend
npm run dev
```

The application will be available at:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000

## Usage

1. Open http://localhost:3000 in your browser
2. Enter a topic (e.g., "Introduction to Machine Learning")
3. Click "Generate Ebook"
4. Watch the progress as the AI generates your ebook
5. Download the PDF when complete

## MCP Server

To use the MCP server with AI agents like Claude Desktop:

```bash
python -m backend.mcp_server
```

Add to your MCP client configuration (`mcp_config.json`):

```json
{
  "mcpServers": {
    "EbookGenerator": {
      "command": "python",
      "args": ["-m", "backend.mcp_server"],
      "env": {
        "GEMINI_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

## Project Structure

```
.
├── backend/
│   ├── agents/
│   │   ├── search_agent.py      # Web search & scraping
│   │   ├── analyst_agent.py     # Content structuring
│   │   ├── image_agent.py       # Image generation
│   │   ├── formatter_agent.py   # HTML formatting
│   │   ├── pdf_agent.py         # PDF creation
│   │   ├── verifier_agent.py    # PDF verification
│   │   └── workflow.py          # Orchestration
│   ├── main.py                  # FastAPI app
│   ├── mcp_server.py            # MCP server
│   ├── requirements.txt         # Python dependencies
│   └── .env                     # API keys
├── frontend/
│   ├── src/
│   │   ├── App.jsx              # Main React component
│   │   ├── App.css              # Styles
│   │   └── main.jsx             # Entry point
│   ├── package.json             # Node dependencies
│   └── vite.config.js           # Vite configuration
└── mcp_config.json              # MCP client config

```

## Technologies

- **Backend**: Python, FastAPI, Google Gemini AI, DuckDuckGo Search, BeautifulSoup, WeasyPrint
- **Frontend**: React, Vite, Modern CSS
- **AI**: Gemini 2.5 Flash
- **MCP**: Model Context Protocol (FastMCP)

## Troubleshooting

### Backend Issues
- **API Key Error**: Ensure `GEMINI_API_KEY` is set in `backend/.env`
- **PDF Generation Failed**: Install system dependencies for WeasyPrint (e.g., `libpango`)
- **Search Failed**: Check internet connection

### Frontend Issues
- **Port 3000 in use**: Change port in `frontend/vite.config.js`
- **API Connection Failed**: Ensure backend is running on port 8000

## License

MIT
