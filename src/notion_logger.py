import logging
import requests
import datetime
import threading
import sys

class NotionLogger(logging.Handler):
    
    class NotionType:
        INFO = "Инфо"
        DEBUG = "Отладка"
        WARNING = "Предупреждение"
        ERROR = "Ошибка"
    
    def __init__(self, page_id, secret_token):
        super().__init__()
        self.TOKEN = secret_token
        self.PAGE_ID = page_id
        self.BASE_URL = "https://api.notion.com/v1"
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.setFormatter(formatter)
        self.HEADERS = {
            'Authorization': f"Bearer {self.TOKEN}", 
           'Content-Type': 'application/json',
           "Notion-Version": "2022-06-28"
           }
        self.DATABASE_ID = self.__init_db()
    
    def activate_global_handler(self):
        def handler(exc_type, exc_value, exc_traceback):
            if issubclass(exc_type, KeyboardInterrupt):
                sys.__excepthook__(exc_type, exc_value, exc_traceback)
                return
            
            logger = logging.getLogger()
            logger.error("Необработанное исключение", exc_info=(exc_type, exc_value, exc_traceback))
            self.log_to_notion(
                file=exc_traceback.tb_frame.f_code.co_filename,
                string=exc_traceback.tb_lineno,
                type=NotionLogger.NotionType.ERROR,
                message=str(exc_value)
            )
            
        sys.excepthook = handler

    def emit(self, record):
        log_entry = self.format(record)
        if "api.notion.com" not in log_entry and self.DATABASE_ID is not None:
            log_type = getattr(NotionLogger.NotionType, record.levelname, NotionLogger.NotionType.INFO)
            threading.Thread(target=self.log_to_notion, args=(record.filename, record.lineno, log_type, record.getMessage()), daemon=True).start()
                
    def __init_db(self) -> str:
        response = requests.post(
            headers=self.HEADERS,
            url=f"{self.BASE_URL}/databases", json={
                "parent": {
                    "type": "page_id",
                    "page_id": self.PAGE_ID
                },
                "icon": {
                    "type": "emoji",
                    "emoji": "🗃️"
                },
                "title": [
                    {
                        "type": "text",
                        "text": {
                            "content": f"Логи {str(datetime.datetime.now())}"
                        }
                    }
                ],
                "properties": {
                    "Файл": {
                        "title": {}
                    },
                    "Строка": {
                        "number": {}
                    },
                    "Тип": {
                        "select": {
                            "options": [
                                {
                                    "name": "Ошибка",
                                    "color": "red"
                                },
                                {
                                    "name": "Предупреждение",
                                    "color": "yellow"
                                },
                                {
                                    "name": "Отладка",
                                    "color": "green"
                                },
                                {
                                    "name": "Инфо",
                                    "color": "purple"
                                }
                            ]
                        }
                    },
                    "Сообщение": {
                        "rich_text": {}
                    },
                    "Время": {
                        "created_time": {}
                    }
                }
            }
        )
        
        if response.status_code == 429:
            raise Exception("Rate limits!")
        
        return response.json()["id"]
    
    def log_to_notion(self, file: str, string: int, type: NotionType, message: str):
        try:
            response = requests.post(
                headers=self.HEADERS,
                url=f"{self.BASE_URL}/pages", json={
                    "parent": { "database_id": self.DATABASE_ID },
                    "properties": {
                        "Файл": {
                            "title": [
                                {
                                    "text": {
                                        "content": file
                                    }
                                }
                            ]
                        },
                        "Строка": {
                            "number": string
                        },
                        "Тип": {
                            "select": {
                                "name": type
                            }
                        },
                        "Сообщение": {
                            "rich_text": [
                                {
                                    "text": {
                                        "content": message
                                    }
                                }
                            ]
                        }
                    }
                }
            )
            response.raise_for_status()
        except Exception as e:
            print(e)

