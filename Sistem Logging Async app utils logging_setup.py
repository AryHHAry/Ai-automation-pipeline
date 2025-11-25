import logging
import asyncio
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
import json
from datetime import datetime

class AsyncLogHandler(logging.Handler):
    """Non-blocking log handler for LLM applications[citation:4]"""
    
    def __init__(self):
        super().__init__()
        self.log_queue = Queue()
        self.executor = ThreadPoolExecutor(max_workers=1)
        self.setup_consumer()
    
    def setup_consumer(self):
        """Background log consumer"""
        def consume_logs():
            while True:
                try:
                    record = self.log_queue.get()
                    if record is None:
                        break
                    self.handle_log(record)
                except Exception as e:
                    print(f"Log consumer error: {e}")
        
        asyncio.get_event_loop().run_in_executor(
            self.executor, 
            consume_logs
        )
    
    def handle_log(self, record):
        """Process log record (simpan ke file/database)"""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName
        }
        
        # Simpan ke file JSON
        with open("logs/app.log", "a") as f:
            f.write(json.dumps(log_entry) + "\n")
    
    def emit(self, record):
        """Add log record to queue (non-blocking)"""
        self.log_queue.put(record)

def get_logger(name):
    """Configure and return logger with async handler"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    if not logger.handlers:
        handler = AsyncLogHandler()
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger