"""
Tokenization and Sequence Windowing for LogBERT

This module converts parsed templates to token IDs and creates
fixed-length sequences for training.
"""

import json
import numpy as np
from pathlib import Path
from typing import List, Tuple
from utils.tokenize_utils import pad_sequences

class LogTokenizer:
    """
    Tokenizer for log templates with sequence windowing.
    """
    
    def __init__(self, vocab_file: str = "data/vocab.json", max_length: int = 512):
        """
        Initialize tokenizer.
        
        Args:
            vocab_file: Path to vocabulary JSON file
            max_length: Maximum sequence length
        """
        self.max_length = max_length
        self.load_vocab(vocab_file)
        
    def load_vocab(self, vocab_file: str):
        """Load vocabulary from JSON file."""
        with open(vocab_file, 'r') as f:
            vocab_data = json.load(f)
            
        self.vocab = vocab_data['vocab']
        self.token_to_id = vocab_data['token_to_id']
        self.id_to_token = vocab_data['id_to_token']
        
    def tokenize(self, template: str) -> int:
        """
        Tokenize a log template.
        
        Args:
            template: Log template string
            
        Returns:
            Token ID
        """
        return self.token_to_id.get(template, self.token_to_id['<UNK>'])
    
    def create_sequences(self, template_ids: List[int], window_size: int = 50) -> List[List[int]]:
        """
        Create sliding window sequences from template IDs.
        
        Args:
            template_ids: List of template token IDs
            window_size: Size of the sliding window
            
        Returns:
            List of fixed-length sequences
        """
        sequences = []
        
        for i in range(0, len(template_ids) - window_size + 1):
            sequence = template_ids[i:i + window_size]
            sequences.append(sequence)
            
        return sequences
    
    def process_templates_to_sequences(self, window_size: int = 50):
        """
        Process all template files and create sequences.
        
        Args:
            window_size: Size of the sliding window
        """
        parsed_dir = Path("data/parsed")
        sequences_dir = Path("data/sequences")
        
        # Create sequences directory
        sequences_dir.mkdir(parents=True, exist_ok=True)
        
        if not parsed_dir.exists():
            print("Error: data/parsed/ directory not found!")
            print("Please run drain_parser.py first.")
            return
        
        # Process each template file
        for template_file in parsed_dir.glob("*_templates.json"):
            print(f"Processing {template_file}...")
            
            # Load templates
            with open(template_file, 'r') as f:
                templates_data = json.load(f)
            
            # Extract template order (assuming templates are in order of appearance)
            template_sequence = []
            for template_text, template_info in templates_data.items():
                count = template_info.get('count', 1)
                # Add template ID repeated by its count
                template_sequence.extend([template_text] * count)
            
            # Convert templates to token IDs
            template_ids = [self.tokenize(template) for template in template_sequence]
            
            # Create sequences
            sequences = self.create_sequences(template_ids, window_size)
            
            # Save sequences
            output_file = sequences_dir / f"{template_file.stem}_sequences.json"
            sequences_data = {
                'sequences': sequences,
                'window_size': window_size,
                'num_sequences': len(sequences),
                'vocab_size': len(self.vocab)
            }
            
            with open(output_file, 'w') as f:
                json.dump(sequences_data, f, indent=2)
            
            print(f"Created {len(sequences)} sequences from {template_file}")
            print(f"Saved sequences to {output_file}")
    
    def create_training_data(self, sequences: List[List[int]]) -> Tuple[np.ndarray, np.ndarray]:
        """
        Create training data from sequences.
        
        Args:
            sequences: List of token ID sequences
            
        Returns:
            Tuple of (input_sequences, target_sequences) for next token prediction
        """
        input_sequences = []
        target_sequences = []
        
        for sequence in sequences:
            # For next token prediction, input is sequence[:-1], target is sequence[1:]
            input_seq = sequence[:-1]
            target_seq = sequence[1:]
            
            # Pad sequences to max_length
            input_seq = input_seq[:self.max_length-1] + [self.token_to_id['<PAD>']] * max(0, self.max_length-1 - len(input_seq))
            target_seq = target_seq[:self.max_length-1] + [self.token_to_id['<PAD>']] * max(0, self.max_length-1 - len(target_seq))
            
            input_sequences.append(input_seq)
            target_sequences.append(target_seq)
        
        return np.array(input_sequences), np.array(target_sequences)

def main():
    """Main function for tokenization and sequence creation."""
    print("Starting tokenization and sequence creation...")
    
    # Check if vocabulary exists
    if not Path("data/vocab.json").exists():
        print("Error: data/vocab.json not found!")
        print("Please run build_vocab.py first.")
        return
    
    # Initialize tokenizer
    tokenizer = LogTokenizer()
    
    # Process templates to sequences
    tokenizer.process_templates_to_sequences(window_size=50)
    
    print("Tokenization and sequence creation completed!")

if __name__ == "__main__":
    main() 