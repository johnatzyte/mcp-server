from fastmcp import FastMCP
import requests
from base64 import b64decode
import os
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field, ValidationError
import logging

class ProductResponse(BaseModel):
    name: Optional[str] = None
    price: Optional[str] = None
    currency: Optional[str] = None
    availability: Optional[str] = None
    sku: Optional[str] = None
    brand: Optional[Dict[str, Any]] = None
    images: Optional[List[Dict[str, Any]]] = None
    description: Optional[str] = None
    url: Optional[str] = None

class HTMLResponse(BaseModel):
    html: str

class ZyteAPIResponse(BaseModel):
    product: Optional[ProductResponse] = None
    httpResponseBody: Optional[str] = None
    browserHtml: Optional[str] = None

class ZyteAPIClient:
    def __init__(self, api_key: str, timeout: int = 30):
        self.api_key = api_key
        self.base_url = "https://api.zyte.com/v1/extract"
        self.timeout = timeout
        self.session = requests.Session()

    def _make_request(self, payload: Dict[str, Any]) -> ZyteAPIResponse:
        logging.info(f"Making request to {self.base_url} for URL: {payload.get('url', 'unknown')}")

        response = self.session.post(
            self.base_url,
            auth=(self.api_key, ""),
            json=payload,
            timeout=self.timeout
        )

        logging.info(f"Response status: {response.status_code}")
        response.raise_for_status()
        return ZyteAPIResponse(**response.json())

    def extract_product(self, url: str) -> ProductResponse:
        payload = {
            "url": url,
            "httpResponseBody": True,
            "product": True,
            "productOptions": {"extractFrom": "httpResponseBody"},
            "followRedirect": True,
        }
        response = self._make_request(payload)
        return response.product or ProductResponse()

    def extract_html(self, url: str) -> HTMLResponse:
        payload = {
            "url": url,
            "httpResponseBody": True,
        }
        response = self._make_request(payload)
        if response.httpResponseBody:
            http_response_body = b64decode(response.httpResponseBody)
            return HTMLResponse(html=http_response_body.decode("utf-8"))
        return HTMLResponse(html="")

    def extract_browser_html(self, url: str) -> HTMLResponse:
        payload = {
            "url": url,
            "browserHtml": True,
        }
        response = self._make_request(payload)
        return HTMLResponse(html=response.browserHtml or "")

mcp = FastMCP("zyte-mcp-server")
API_KEY = os.getenv("ZYTE_API_KEY")
if API_KEY is None:
    raise Exception("ZYTE_API_KEY environment variable is not set")

zyte_client = ZyteAPIClient(API_KEY)


@mcp.tool
def extract_product(url: str) -> dict:
    """
    extract product data from a given URL using Zyte API
    """
    response = zyte_client.extract_product(url)
    return response.model_dump()


@mcp.tool
def extract_html(url: str) -> dict:
    """
    extract page html from a given URL using Zyte API
    """
    response = zyte_client.extract_html(url)
    return response.model_dump()


@mcp.tool
def extract_html_with_browser(url: str) -> dict:
    """
    extract page html from a given URL using Zyte API
    """
    response = zyte_client.extract_browser_html(url)
    return response.model_dump()


if __name__ == "__main__":
    mcp.run()
