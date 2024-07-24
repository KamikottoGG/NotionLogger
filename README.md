# Notion Logger

The `NotionLogger` package provides a custom logging handler that sends log entries to a specified Notion database. This tool is useful for centralizing logs from different applications and tracking errors, warnings, and other log messages in Notion.

## Features

- 📄 **Log to Notion:** Directly send log messages to a Notion database.
- ⚙️ **Custom Log Types:** Support for various log types including INFO, DEBUG, WARNING, and ERROR.
- 🌐 **Global Exception Handling:** Automatically logs uncaught exceptions to Notion.

## Installation

```bash
pip install requests
```

## Usage

### Basic Setup

First, import the necessary modules and set up your logger:

```python
import logging
from notion_logger import NotionLogger

# Replace with your own Notion page ID and secret token
PAGE_ID = "your_page_id"
SECRET_TOKEN = "your_secret_token"

notion_handler = NotionLogger(page_id=PAGE_ID, secret_token=SECRET_TOKEN)
logging.getLogger().addHandler(notion_handler)
logging.getLogger().setLevel(logging.DEBUG)

# Activate global exception handler
notion_handler.activate_global_handler()
```

### Logging Messages

Now you can log messages as usual, and they will be sent to your Notion database:

```python
logger = logging.getLogger(__name__)

logger.info("This is an informational message 📄")
logger.debug("This is a debug message 🐞")
logger.warning("This is a warning message ⚠️")
logger.error("This is an error message ❌")
```

### Example

Here's a complete example including the setup and logging messages:

```python
import logging
from notion_logger import NotionLogger

# Replace with your own Notion page ID and secret token
PAGE_ID = "your_page_id"
SECRET_TOKEN = "your_secret_token"

# Initialize the Notion logger
notion_handler = NotionLogger(page_id=PAGE_ID, secret_token=SECRET_TOKEN)
logging.getLogger().addHandler(notion_handler)
logging.getLogger().setLevel(logging.DEBUG)

# Activate global exception handler
notion_handler.activate_global_handler()

# Log some messages
logger = logging.getLogger(__name__)

logger.info("This is an informational message 📄")
logger.debug("This is a debug message 🐞")
logger.warning("This is a warning message ⚠️")
logger.error("This is an error message ❌")

# Example of an unhandled exception
def divide(a, b):
    return a / b

try:
    divide(1, 0)
except ZeroDivisionError:
    logger.exception("An exception occurred")
```

## How It Works

### Initialization

The `NotionLogger` class is initialized with a Notion page ID and a secret token. It sets up the necessary headers and creates a database in Notion to store the logs.

### Logging

When a log message is emitted, the `emit` method formats the message and sends it to Notion using the `log_to_notion` method. Each log entry includes the file name, line number, log type, and the message content.

### Exception Handling

The `activate_global_handler` method sets a global exception handler that catches uncaught exceptions and logs them to Notion.

## Requirements

- Python 3.6+
- `requests` library

## Contributing

Contributions are welcome! Please open an issue or submit a pull request on GitHub.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

Feel free to reach out with any questions or feedback! Happy logging 📋✨