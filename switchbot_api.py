import requests
import json
import time
import hashlib
import hmac
import base64
import uuid
from typing import Dict, List, Optional

class SwitchBotAPI:
    """SwitchBot Open API v1.1 client"""
    
    BASE_URL = "https://api.switch-bot.com/v1.1"
    
    def __init__(self, token: str, secret: str):
        """
        Initialize SwitchBot API client
        
        Args:
            token: SwitchBot API token
            secret: SwitchBot API secret
        """
        self.token = token
        self.secret = secret
    
    def _generate_headers(self) -> Dict[str, str]:
        """Generate authentication headers for API requests"""
        # Generate timestamp and nonce
        t = int(round(time.time() * 1000))
        nonce = str(uuid.uuid4())
        
        # Create signature
        string_to_sign = f"{self.token}{t}{nonce}"
        string_to_sign_bytes = bytes(string_to_sign, 'utf-8')
        secret_bytes = bytes(self.secret, 'utf-8')
        sign = base64.b64encode(
            hmac.new(secret_bytes, msg=string_to_sign_bytes, digestmod=hashlib.sha256).digest()
        ).decode('utf-8')
        
        return {
            'Authorization': self.token,
            'Content-Type': 'application/json',
            'charset': 'utf8',
            't': str(t),
            'sign': sign,
            'nonce': nonce
        }
    
    def _make_request(self, endpoint: str, method: str = 'GET', data: Optional[Dict] = None) -> Optional[Dict]:
        """
        Make authenticated request to SwitchBot API
        
        Args:
            endpoint: API endpoint
            method: HTTP method
            data: Request payload
            
        Returns:
            Response data or None if error
        """
        url = f"{self.BASE_URL}{endpoint}"
        headers = self._generate_headers()
        
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, timeout=10)
            elif method == 'POST':
                response = requests.post(url, headers=headers, json=data, timeout=10)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            response.raise_for_status()
            
            result = response.json()
            
            # Check API response status
            if result.get('statusCode') != 100:
                error_msg = result.get('message', 'Unknown error')
                raise Exception(f"API Error: {error_msg} (Status: {result.get('statusCode')})")
            
            return result.get('body', {})
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Network error: {str(e)}")
        except json.JSONDecodeError:
            raise Exception("Invalid JSON response from API")
        except Exception as e:
            raise Exception(f"API request failed: {str(e)}")
    
    def get_devices(self) -> List[Dict]:
        """
        Get list of all devices
        
        Returns:
            List of device information
        """
        try:
            result = self._make_request('/devices')
            if result and 'deviceList' in result:
                return result['deviceList']
            return []
        except Exception as e:
            raise Exception(f"Failed to get devices: {str(e)}")
    
    def get_device_status(self, device_id: str) -> Optional[Dict]:
        """
        Get status of a specific device
        
        Args:
            device_id: Device ID
            
        Returns:
            Device status data or None if error
        """
        try:
            result = self._make_request(f'/devices/{device_id}/status')
            return result
        except Exception as e:
            raise Exception(f"Failed to get device status for {device_id}: {str(e)}")
    
    def get_scenes(self) -> List[Dict]:
        """
        Get list of all scenes
        
        Returns:
            List of scene information
        """
        try:
            result = self._make_request('/scenes')
            if result and 'sceneList' in result:
                return result['sceneList']
            return []
        except Exception as e:
            raise Exception(f"Failed to get scenes: {str(e)}")
    
    def execute_scene(self, scene_id: str) -> bool:
        """
        Execute a scene
        
        Args:
            scene_id: Scene ID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self._make_request(f'/scenes/{scene_id}/execute', method='POST')
            return True
        except Exception as e:
            raise Exception(f"Failed to execute scene {scene_id}: {str(e)}")
