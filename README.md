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

    Open Google Chrome or API client (like Postman) and navigate to:

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

## Key Considerations

### **API Response Time**

The API currently takes around 250 seconds to return data. This extended response time is due to the time required to fetch and process multiple pages of items.

- **Consideration:** If you encounter timeouts in your API client, consider increasing the timeout settings for your requests. This adjustment will allow the application to handle longer processing times and improve overall stability during data retrieval.

### **Value Retrieval**

The script currently captures the average value from elements on the web page. Both average and community values are located under the same parent class and share the same class name.

- **Consideration:** If community values are needed instead of average values, you may need to review and update the class name selectors. Since both values are under the same parent class and use the same class name, adapting the code to capture community values should be straightforward if the distinction is required.

### **Dependencies and Environment**

- **Dependencies:** Ensure that all required packages listed in `requirements.txt` are installed. Use a virtual environment to manage these dependencies and avoid conflicts with other Python projects.
  
- **WebDriver Management:** The script uses `webdriver-manager` to automatically handle ChromeDriver binaries. Ensure that you have Google Chrome installed, as it is required for Selenium to function correctly.

### **Error Handling and Logging**

The script includes basic error handling and logging configurations. It suppresses warnings from Selenium and other libraries to avoid cluttered logs.

- **Consideration:** Adjust logging levels and error handling according to your debugging needs. More granular error handling might be required based on specific use cases or to improve robustness.

## Attribution

If you use or modify this code, please include the following attribution in any related documentation or publicly accessible materials: "Powered by Anndromeda™ by Alina."

## License
This code is provided under the terms of the [LICENSE.md](LICENSE.md) file included in this distribution.
