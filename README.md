# A customized MCP server for Everpure FlashArray operations.

This is a simple MCP server for operating Everpure FlashArray. This MCP server goes through traditional Purity REST API, no Fusion needed.



## Main Files

- server.py
  This is the main program file built using Fastmcp.
- fatools.py
  A Purity REST API wrapper. Built using py-pure-client.
- fainfo.json
  A list of mgmt endpoint and access token of managed FlashArrays.



## How to use

- Create venv:
  ```bash
  uv venv --python 3.12.10
  ```
- Install packages:
  ```bash
  uv add -r requirments.txt
  ```
- Run the server:
  ```bash
  python server.py
  ```
  
