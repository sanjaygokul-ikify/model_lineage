import os
import pandas as pd
from model_lineage import ModelLineage

def main():
    model_lineage = ModelLineage()
    model_lineage.log_model_metadata(model_name='my_model', model_version='1.0')
if __name__ == '__main__':
    main()