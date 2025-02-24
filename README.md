# County Data API

This API provides access to county health rankings data based on ZIP codes.

## Endpoint: `/county_data`

### Request
- Method: POST
- Content-Type: application/json
- Required fields:
  - `zip`: 5-digit ZIP code
  - `measure_name`: One of the following measures:
    - Violent crime rate
    - Unemployment
    - Children in poverty
    - Diabetic screening
    - Mammography screening
    - Preventable hospital stays
    - Uninsured
    - Sexually transmitted infections
    - Physical inactivity
    - Adult obesity
    - Premature Death
    - Daily fine particulate matter

### Example Request
```json
{
    "zip": "02138",
    "measure_name": "Adult obesity"
}
```

### Response
Returns an array of matching records in JSON format.

### Status Codes
- 200: Success
- 400: Missing required fields or invalid input
- 404: No data found for given ZIP code and measure
- 418: Easter egg (when coffee=teapot is included in request)
- 500: Server error

### Easter Egg
Including `"coffee": "teapot"` in the request body will return a 418 status code.

## Setup
1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
python app.py
```

The server will run on port 5000 by default, or the port specified in the PORT environment variable.
