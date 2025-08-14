import requests
import hashlib
import hmac
import secrets
import time
import json as _json
import urllib3
from typing import Optional, Dict, Any

class Algo8301Client:
    def __init__(self, base_url: str, api_password: str, verify_ssl: bool = True, debug: bool = False):
        self.base_url = base_url.rstrip('/')
        self.api_password = api_password.encode('utf-8')
        self.verify_ssl = verify_ssl
        self.debug = debug

        if not verify_ssl:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def _generate_headers(self, method: str, path: str, body: Optional[bytes]) -> Dict[str, str]:
        nonce = secrets.token_hex(8)
        timestamp = str(int(time.time()))

        if body is not None:
            content_md5 = hashlib.md5(body).hexdigest()
            content_type = 'application/json'
            hmac_input = ":".join([
                method.upper(),
                path,
                content_md5,
                content_type,
                timestamp,
                nonce
            ])
        else:
            content_md5 = None
            content_type = None
            hmac_input = ":".join([
                method.upper(),
                path,
                timestamp,
                nonce
            ])

        digest = hmac.new(self.api_password, hmac_input.encode('utf-8'), hashlib.sha256).hexdigest()
        auth_header = f"hmac admin:{nonce}:{digest}"

        headers = {
            'Authorization': auth_header,
            'Date': time.strftime('%a, %d %b %Y %H:%M:%S GMT', time.gmtime()),
        }

        if body is not None:
            headers.update({
                'Content-Type': content_type,
                'Content-MD5': content_md5
            })

        if self.debug:
            print("\n--- HMAC DEBUG ---")
            print(f"Method: {method.upper()}")
            print(f"Path: {path}")
            print(f"Timestamp: {timestamp}")
            print(f"Nonce: {nonce}")
            print(f"HMAC Input: {hmac_input}")
            print(f"HMAC Digest: {digest}")
            if body:
                print(f"Body Bytes: {body}")
                print(f"MD5: {content_md5}")
            print(f"Headers: {headers}")
            print("--- END DEBUG ---\n")

        return headers

    def request(self, method: str, path: str, json: Optional[Dict[str, Any]] = None) -> requests.Response:
        url = f"{self.base_url}{path}"

        # Prepare payload
        if json is not None:
            # Compact JSON (no spaces) so MD5 matches Algo device
            body_bytes = _json.dumps(json, separators=(',', ':')).encode('utf-8')
        else:
            body_bytes = None

        headers = self._generate_headers(method, path, body_bytes)

        if self.debug:
            print(f"Full URL: {url}")
            print(f"Verify SSL: {self.verify_ssl}")

        resp = requests.request(
            method=method.upper(),
            url=url,
            headers=headers,
            data=body_bytes,
            verify=self.verify_ssl
        )

        if self.debug:
            print(f"Response Status: {resp.status_code}")
            print(f"Response Body: {resp.text}")

        return resp

    # -------------------
    # Helper functions
    # -------------------
    def get_setting(self, param: str) -> Dict[str, Any]:
        """Fetch a single setting from the Algo device."""
        resp = self.request("GET", f"/api/settings/{param}")
        resp.raise_for_status()
        return resp.json()[param]

    def put_setting(self, param: str, value: str) -> bool:
        """Update a single setting on the Algo device."""
        resp = self.request("PUT", "/api/settings", json={param: value})
        if self.debug:
            print(f"PUT /api/settings returned {resp.status_code}")
        resp.raise_for_status()
        return resp.status_code in (200, 204)