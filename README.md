# Royale High API

This is a simple Flask API to fetch Royale High item names and their community values from Traderie.

## Setup Instructions

### Prerequisites

1. **Python 3.x**: Make sure you have Python 3.x installed. You can download it from [python.org](https://www.python.org/).
2. **pip**: Ensure you have pip (Python package installer) installed. It usually comes with Python.

### Installation

1. **Clone the Repository**:

    ```bash
    git clone https://github.com/ProjectAnndromeda/royalehigh-api.git
    cd royalehigh-api
    ```

2. **Create a Virtual Environment** (optional but recommended):

    ```bash
    python -m venv venv
    ```

3. **Activate the Virtual Environment**:

    - **Windows Command Prompt**:

        ```bash
        venv\Scripts\activate
        ```

    - **Windows PowerShell**:

        ```powershell
        .\venv\Scripts\Activate.ps1
        ```

    - **macOS/Linux**:

        ```bash
        source venv/bin/activate
        ```

4. **Install Dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

### Running the API

1. **Run the Flask Application**:

    ```bash
    flask run
    ```

2. **Access the API**:

    Open your web browser or API client (like Postman) and navigate to:

    ```
    http://127.0.0.1:5000/items
    ```

### Example Response

```json
[
    {
        "name": "14 Karat Gold Infinity Chain",
        "value": 14000
    },
    {
        "name": "2019 Party Hat",
        "value": 10000
    },
    {
        "name": "2020 Lunar Rat Ears",
        "value": 4000
    },
    ...
]
```

## Attribution

If you use or modify this code, please include the following attribution in any related documentation or publicly accessible materials: "Powered by Anndromeda™ by Alina."

## License
This code is provided under the terms of the [LICENSE.txt](LICENSE.txt) file included in this distribution.
