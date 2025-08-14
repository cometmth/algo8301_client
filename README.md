# Algo8301 Python Client

A Python client for interacting with the Algo 8301 REST API. This client supports the **Standard HMAC-based authentication** method, optional SSL verification, and provides convenient helper functions for getting and updating device settings. It is designed to be easily importable into other Python scripts.

## Features

- HMAC SHA-256 authentication compatible with Algo 8301 devices
- Automatic handling of payload and no-payload requests
- Optional SSL verification (with self-signed certificate support)
- Debug mode for inspecting HMAC computation and HTTP requests
- Helper functions for getting and updating settings

## Prerequisites

Enable the RESTful API on the Algo 8301 following [Algo's documentation](https://docs.algosolutions.com/docs/restful-api-guide#initial-configuration) 

## Installation

Clone the repository or include the client package in your project:

```bash
git clone https://github.com/cometmth/algo8301_client.git
```

Install required dependencies:

```bash
pip install requests
```

## Usage
### Basic Example

```python
from algo8301_client import Algo8301Client

client = Algo8301Client(
    base_url="https://192.168.1.100",
    api_password="MySecretPassword",
    verify_ssl=False,  # Disable SSL verification for self-signed certs
    debug=True         # Enable debug mode
)

# Retrieve the device information from the About page of the device web interface
about = client.request('GET', '/api/info/about')
print(about.json())

# Play or loop a selected tone
json = {"path": "chime.wav", "loop": True, "mcast": False}
resp = client.request('POST', '/api/controls/tone/start', json=json)

# Get current setting value
current_setting = client.get_setting('mcast.zone13')
print("Current Setting:", current_setting)

# Update a setting
success = client.put_setting('mcast.zone13', '224.0.2.113:50013')
print("Update successful?", success)
```
## Request Function
The request function provides low-level access to the Algo 8301 REST API. It allows you to send arbitrary HTTP requests with full HMAC authentication:
request(method, path)

- method (str): The HTTP method (GET, POST, PUT, DELETE, etc.).
- path (str): The API path relative to the base URL (e.g., /api/settings).
- json (dict, optional): A Python dictionary to send as a JSON payload. The client automatically serializes it and computes the correct HMAC.

Returns: A requests.Response object with the server's response.

## Helper Functions
- get_setting(parameter_name): Fetch specified device setting as a string.
- put_setting(parameter_name, value): Update specified device setting. Returns True if successful.

## Debug Mode
When debug=True is passed to the client constructor, detailed information about the HMAC input, headers, payload, URL, and responses will be printed. This is useful for troubleshooting authentication or payload issues.

## Security Notes
SSL Verification: By default, SSL certificates are verified. Use verify_ssl=False only in trusted networks or lab environments.
Time Synchronization: The HMAC authentication is time-sensitive. Ensure your client machine and the Algo device have synchronized clocks.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
