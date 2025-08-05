# Overview

This is a SwitchBot Temperature Monitor application built with Streamlit that provides real-time monitoring of SwitchBot thermometer devices. The application displays temperature, humidity, and battery status for multiple SwitchBot devices in an intuitive web interface with temperature conversion between Celsius and Fahrenheit.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
- **Framework**: Streamlit web application framework
- **UI Components**: Card-based layout displaying device metrics with color-coded battery status indicators
- **Data Visualization**: Real-time metrics display with temperature conversion (Celsius to Fahrenheit)
- **Layout**: Wide layout configuration with multi-column card displays for device information

## Backend Architecture
- **API Integration**: Custom SwitchBotAPI class handling authentication and device communication
- **Authentication**: HMAC-SHA256 signature-based authentication with timestamp and nonce generation
- **Data Processing**: Temperature conversion utilities and battery status color coding logic
- **Request Handling**: RESTful API client with proper header generation and error handling

## Data Management
- **Real-time Data**: Live polling of SwitchBot devices for temperature, humidity, and battery metrics
- **Data Format**: JSON-based API responses with device status information
- **State Management**: Streamlit's built-in session state for UI updates

## Security Architecture
- **API Security**: Token-based authentication with HMAC signatures for secure SwitchBot API communication
- **Credential Management**: Environment variable-based configuration for API tokens and secrets

# External Dependencies

## Third-Party Services
- **SwitchBot Open API v1.1**: Primary integration for device data retrieval and control
- **Base URL**: `https://api.switch-bot.com/v1.1`

## Python Libraries
- **streamlit**: Web application framework for the user interface
- **requests**: HTTP client library for API communication
- **hashlib**: Cryptographic hashing for HMAC signature generation
- **hmac**: HMAC authentication implementation
- **base64**: Encoding/decoding for API signatures
- **uuid**: Unique identifier generation for API nonces

## Hardware Integration
- **SwitchBot Thermometer Devices**: Physical IoT sensors providing temperature, humidity, and battery data
- **SwitchBot Hub**: Required for device connectivity and API access