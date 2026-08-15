# A customized MCP server for Everpure FlashArray operations.

This is a simple MCP server for operating Everpure FlashArray. This MCP server goes through traditional Purity REST API, no Fusion needed.



## Main Files

### server.py
  This is the main program file built using Fastmcp.
### fatools.py
  A Purity REST API wrapper. Built using py-pure-client.
### fainfo.json
  A list of mgmt endpoint and access token of managed FlashArrays.
### serverconf.json
  Server parameters needed when starting server. Specify listening IP and port in this file.
  
## How to use

### Config server
Server parameters are saved in a file named serverconf.json. Default value of this file is as below:
```json
{
  "server_ip":"0.0.0.0"
  "server_port":8765
}
```
Change these value if you need to specify listening IP address and port.

### Array information configuration
The information of Managed arrays, including management IP and token, are stored in a file named fainfo.json. A example of this file is as below:
```json
{
    "array_info":
        [
            {
                "array_name":"172.30.5.1",
                "api_token":"0296fea8-2372-4575-4d1a-b4695a2ecfa6"
            },
            {
                "array_name":"172.30.5.2",
                "api_token":"0296fea8-2372-4575-4d1a-b4695a2ecfa6"
            }
        ]
}
```
The array_name should be IP address or FQDN of the management endpoint of the array.
The api_token should be mapped to an array admin user who has enough privileges to operate the array.

### Start the server
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
  
