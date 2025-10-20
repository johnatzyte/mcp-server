# Zyte API MCP Server

This is a demo MCP server used as an example of how to ingrate MCP tools into the Zyte API. However, it will work as is.

clone the repo.

```
    uv venv
    uv sync
```

Add the MCP JSON to .vscode folder (udpate to correct file path)


```
{
  "servers": {
    "Zyte MCP Server": {
      "command": "uv",
      "args": [
        "run",
        "--with",
        "fastmcp",
        "fastmcp",
        "run",
        "/Users/john.rooney/Projects/mcp-server/main.py"
      ],
      "env": {}
    }
  }
}
```

The above should also be able to be transformed into the format you need to work with desktop AI clients, like Claude Code, JanAI, etc.

### API KEY
This repo assumes your Zyte API key is in your environment. However, for desktop AI Clients this will need to be added into the config for the specific client you are using.

For VS Code, it works with the env variables on your machine.

unix:
```
export ZYTE_API_KEY=YOURAPIKEY
```