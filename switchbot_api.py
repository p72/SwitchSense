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
    
    # ===== デバイス操作機能 =====
    
    def turn_on_device(self, device_id: str) -> bool:
        """
        Turn on a device
        
        Args:
            device_id: Device ID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            data = {"command": "turnOn", "parameter": "default", "commandType": "command"}
            self._make_request(f'/devices/{device_id}/commands', method='POST', data=data)
            return True
        except Exception as e:
            raise Exception(f"Failed to turn on device {device_id}: {str(e)}")
    
    def turn_off_device(self, device_id: str) -> bool:
        """
        Turn off a device
        
        Args:
            device_id: Device ID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            data = {"command": "turnOff", "parameter": "default", "commandType": "command"}
            self._make_request(f'/devices/{device_id}/commands', method='POST', data=data)
            return True
        except Exception as e:
            raise Exception(f"Failed to turn off device {device_id}: {str(e)}")
    
    # ===== テレビ操作機能 =====
    
    def tv_power(self, device_id: str) -> bool:
        """
        Toggle TV power
        
        Args:
            device_id: TV device ID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            data = {"command": "turnOn", "parameter": "default", "commandType": "command"}
            self._make_request(f'/devices/{device_id}/commands', method='POST', data=data)
            return True
        except Exception as e:
            raise Exception(f"Failed to toggle TV power for {device_id}: {str(e)}")
    
    def tv_volume_up(self, device_id: str) -> bool:
        """
        Increase TV volume
        
        Args:
            device_id: TV device ID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            data = {"command": "volumeAdd", "parameter": "default", "commandType": "command"}
            self._make_request(f'/devices/{device_id}/commands', method='POST', data=data)
            return True
        except Exception as e:
            raise Exception(f"Failed to increase TV volume for {device_id}: {str(e)}")
    
    def tv_volume_down(self, device_id: str) -> bool:
        """
        Decrease TV volume
        
        Args:
            device_id: TV device ID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            data = {"command": "volumeSub", "parameter": "default", "commandType": "command"}
            self._make_request(f'/devices/{device_id}/commands', method='POST', data=data)
            return True
        except Exception as e:
            raise Exception(f"Failed to decrease TV volume for {device_id}: {str(e)}")
    
    def tv_channel_up(self, device_id: str) -> bool:
        """
        Increase TV channel
        
        Args:
            device_id: TV device ID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            data = {"command": "channelAdd", "parameter": "default", "commandType": "command"}
            self._make_request(f'/devices/{device_id}/commands', method='POST', data=data)
            return True
        except Exception as e:
            raise Exception(f"Failed to increase TV channel for {device_id}: {str(e)}")
    
    def tv_channel_down(self, device_id: str) -> bool:
        """
        Decrease TV channel
        
        Args:
            device_id: TV device ID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            data = {"command": "channelSub", "parameter": "default", "commandType": "command"}
            self._make_request(f'/devices/{device_id}/commands', method='POST', data=data)
            return True
        except Exception as e:
            raise Exception(f"Failed to decrease TV channel for {device_id}: {str(e)}")
    
    def tv_set_channel(self, device_id: str, channel: int) -> bool:
        """
        Set TV to specific channel
        
        Args:
            device_id: TV device ID
            channel: Channel number
            
        Returns:
            True if successful, False otherwise
        """
        try:
            data = {"command": "SetChannel", "parameter": str(channel), "commandType": "command"}
            self._make_request(f'/devices/{device_id}/commands', method='POST', data=data)
            return True
        except Exception as e:
            raise Exception(f"Failed to set TV channel for {device_id}: {str(e)}")
    
    def tv_set_volume(self, device_id: str, volume: int) -> bool:
        """
        Set TV volume to specific level
        
        Args:
            device_id: TV device ID
            volume: Volume level (0-100)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            data = {"command": "setVolume", "parameter": str(volume), "commandType": "command"}
            self._make_request(f'/devices/{device_id}/commands', method='POST', data=data)
            return True
        except Exception as e:
            raise Exception(f"Failed to set TV volume for {device_id}: {str(e)}")
    
    # ===== エアコン操作機能 =====
    
    def ac_power(self, device_id: str) -> bool:
        """
        Toggle AC power
        
        Args:
            device_id: AC device ID
            
        Returns:
            True if successful, False otherwise
        """
        try:
            data = {"command": "turnOn", "parameter": "default", "commandType": "command"}
            self._make_request(f'/devices/{device_id}/commands', method='POST', data=data)
            return True
        except Exception as e:
            raise Exception(f"Failed to toggle AC power for {device_id}: {str(e)}")
    
    def ac_set_temperature(self, device_id: str, temperature: int) -> bool:
        """
        Set AC temperature
        
        Args:
            device_id: AC device ID
            temperature: Temperature in Celsius
            
        Returns:
            True if successful, False otherwise
        """
        try:
            data = {"command": "setAll", "parameter": f"25,{temperature},auto", "commandType": "command"}
            self._make_request(f'/devices/{device_id}/commands', method='POST', data=data)
            return True
        except Exception as e:
            raise Exception(f"Failed to set AC temperature for {device_id}: {str(e)}")
    
    def ac_set_mode(self, device_id: str, mode: str) -> bool:
        """
        Set AC mode (cool, heat, auto, fan, dry)
        
        Args:
            device_id: AC device ID
            mode: Mode (cool, heat, auto, fan, dry)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            data = {"command": "setAll", "parameter": f"25,25,{mode}", "commandType": "command"}
            self._make_request(f'/devices/{device_id}/commands', method='POST', data=data)
            return True
        except Exception as e:
            raise Exception(f"Failed to set AC mode for {device_id}: {str(e)}")
    
    # ===== シーン機能 =====
    
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
    
    # ===== デバイス情報取得 =====
    
    def get_device_types(self) -> Dict[str, List[str]]:
        """
        Get supported device types and their commands
        
        Returns:
            Dictionary of device types and their supported commands
        """
        return {
            "TV": ["power", "volume_up", "volume_down", "channel_up", "channel_down", "set_channel", "set_volume"],
            "AC": ["power", "set_temperature", "set_mode"],
            "Light": ["turn_on", "turn_off"],
            "Switch": ["turn_on", "turn_off"],
            "Meter": ["get_status"],
            "MeterPlus": ["get_status"],
            "OutdoorMeter": ["get_status"]
        }
    
    def get_infrared_remotes(self) -> List[Dict]:
        """
        Get list of infrared remote devices
        
        Returns:
            List of infrared remote device information
        """
        try:
            result = self._make_request('/devices')
            if result and 'infraredRemoteList' in result:
                return result['infraredRemoteList']
            return []
        except Exception as e:
            raise Exception(f"Failed to get infrared remotes: {str(e)}")
    
    def get_infrared_remote_status(self, remote_id: str) -> Optional[Dict]:
        """
        Get status of a specific infrared remote device
        
        Args:
            remote_id: Infrared remote device ID
            
        Returns:
            Infrared remote device status data or None if error
        """
        try:
            result = self._make_request(f'/devices/{remote_id}/status')
            return result
        except Exception as e:
            raise Exception(f"Failed to get infrared remote status for {remote_id}: {str(e)}")
    
    def send_infrared_command(self, remote_id: str, command: str, parameter: str = "default") -> bool:
        """
        Send infrared command to a remote device
        
        Args:
            remote_id: Infrared remote device ID
            command: Command to send
            parameter: Command parameter
            
        Returns:
            True if successful, False otherwise
        """
        try:
            data = {"command": command, "parameter": parameter, "commandType": "command"}
            self._make_request(f'/devices/{remote_id}/commands', method='POST', data=data)
            return True
        except Exception as e:
            raise Exception(f"Failed to send infrared command to {remote_id}: {str(e)}")
