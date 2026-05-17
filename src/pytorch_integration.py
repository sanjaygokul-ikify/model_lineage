import torch.nn as nn


class PyTorchIntegration:
    def __init__(self, lineage):
        self.conn = lineage.conn
        self.cursor = lineage.cursor

    def log_model_architecture(self, model, model_name, model_version):
        if not isinstance(model, nn.Module):
            raise TypeError('model must be an instance of torch.nn.Module')
        self.cursor.execute(
            'CREATE TABLE IF NOT EXISTS pytorch_model_architecture '
            '(model_name TEXT, model_version TEXT, layer_name TEXT, layer_type TEXT, num_parameters INTEGER)'
        )
        for layer_name, module in model.named_modules():
            layer_type = type(module).__name__
            num_parameters = sum(p.numel() for p in module.parameters(recurse=False))
            self.cursor.execute(
                'INSERT INTO pytorch_model_architecture '
                '(model_name, model_version, layer_name, layer_type, num_parameters) VALUES (?, ?, ?, ?, ?)',
                (model_name, model_version, layer_name, layer_type, num_parameters)
            )
        self.conn.commit()

    def log_model_summary(self, model, model_name, model_version):
        if not isinstance(model, nn.Module):
            raise TypeError('model must be an instance of torch.nn.Module')
        total_params = sum(p.numel() for p in model.parameters())
        trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
        self.cursor.execute(
            'CREATE TABLE IF NOT EXISTS pytorch_model_summary '
            '(model_name TEXT, model_version TEXT, total_parameters INTEGER, trainable_parameters INTEGER)'
        )
        self.cursor.execute(
            'INSERT INTO pytorch_model_summary '
            '(model_name, model_version, total_parameters, trainable_parameters) VALUES (?, ?, ?, ?)',
            (model_name, model_version, total_params, trainable_params)
        )
        self.conn.commit()
