import pandas as pd
from src.database import get_connection
from src.pytorch_integration import PyTorchIntegration

class ModelLineage:
    def __init__(self, backend='sqlite', **config):
        self.conn, self.cursor = get_connection(backend, **config)

    def log_model_metadata(self, model_name, model_version):
        self.cursor.execute('CREATE TABLE IF NOT EXISTS model_metadata (model_name TEXT, model_version TEXT)')
        self.cursor.execute('INSERT INTO model_metadata (model_name, model_version) VALUES (?, ?)', (model_name, model_version))
        self.conn.commit()

    def log_pytorch_model(self, model, model_name, model_version):
        pytorch = PyTorchIntegration(self)
        pytorch.log_model_architecture(model, model_name, model_version)
        pytorch.log_model_summary(model, model_name, model_version)