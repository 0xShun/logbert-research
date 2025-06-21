# LogBERT: Log Analysis with BERT-Style Models

A machine learning pipeline for log parsing, template extraction, and anomaly detection using transformer-based models.

## Overview

LogBERT analyzes system logs using NLP techniques:

-   **Log Parsing**: Drain algorithm for template extraction
-   **Tokenization**: BERT-style tokenization for log sequences
-   **Anomaly Detection**: Transformer-based model for unusual patterns
-   **Dashboard**: Web interface for real-time analysis

## Project Structure

```
logbert-capstone/
├── data/
│   ├── raw/                 # Raw log files
│   ├── parsed/              # Parser output
│   └── sequences/           # Tokenized sequences
├── preprocessing/
│   ├── drain_parser.py      # Template extraction
│   ├── build_vocab.py       # Vocabulary builder
│   └── tokenize.py          # Sequence windowing
├── training/
│   └── train.py             # Training loop
├── models/                  # Model checkpoints
├── utils/
│   └── tokenize_utils.py    # Helper functions
├── dashboard/
│   └── app.py               # Flask dashboard
├── requirements.txt         # Dependencies
└── README.md
```

## Quick Start

1. **Install dependencies**

    ```bash
    pip install -r requirements.txt
    ```

2. **Prepare data**

    ```bash
    # Place log files in data/raw/
    cp your_logs.log data/raw/
    ```

3. **Run preprocessing**

    ```bash
    python preprocessing/drain_parser.py
    python preprocessing/build_vocab.py
    python preprocessing/tokenize.py
    ```

4. **Train model**

    ```bash
    python training/train.py
    ```

5. **Launch dashboard**
    ```bash
    python dashboard/app.py
    # Visit http://localhost:5000
    ```

## Features

-   **Drain Parser**: Efficient template extraction from unstructured logs
-   **BERT-Style Model**: Transformer architecture for log sequence understanding
-   **Anomaly Detection**: Identifies unusual log patterns
-   **Real-time Dashboard**: Web interface for log analysis and visualization

## Dependencies

-   torch, transformers, drain3, kafka-python, flask
-   numpy, pandas, scikit-learn
-   See requirements.txt for complete list

## Usage

```python
# Template extraction
from preprocessing.drain_parser import DrainParser
parser = DrainParser()
templates = parser.extract_templates(log_lines)

# Model training
from training.train import LogBERTTrainer
trainer = LogBERTTrainer(model, config)
trainer.train_epoch(dataloader)

# Dashboard API
import requests
response = requests.post('http://localhost:5000/api/analyze',
                        json={'log_entry': 'Your log message'})
```

## Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Open Pull Request

## License

MIT License

---

**Note**: Research project - add testing/validation for production use.
