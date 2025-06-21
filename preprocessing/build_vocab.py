"""
Vocabulary Builder for LogBERT

This module builds vocabulary from parsed log templates in data/parsed/
and creates a mapping from template text to token IDs.
"""

import json
from pathlib import Path
from collections import Counter

class VocabularyBuilder:
    """
    Builds vocabulary from parsed log templates.
    """
    
    def __init__(self, min_freq: int = 2, max_vocab_size: int = 50000):
        self.min_freq = min_freq
        self.max_vocab_size = max_vocab_size
        self.vocab = {}
        self.token_to_id = {}
        self.id_to_token = {}
        
    def build_vocab(self, templates: dict) -> dict:
        """Build vocabulary from log templates."""
        # Count template frequencies
        template_counts = {template: data.get('count', 1) for template, data in templates.items()}
        
        # Filter by minimum frequency
        filtered_templates = {template: count for template, count in template_counts.items() if count >= self.min_freq}
        
        # Sort by frequency and limit vocabulary size
        sorted_templates = sorted(filtered_templates.items(), key=lambda x: x[1], reverse=True)
        
        # Add special tokens
        special_tokens = {'<PAD>': 0, '<UNK>': 1, '<MASK>': 2, '<CLS>': 3, '<SEP>': 4}
        self.vocab = special_tokens.copy()
        self.token_to_id = special_tokens.copy()
        
        # Add templates to vocabulary
        for i, (template, count) in enumerate(sorted_templates[:self.max_vocab_size - len(special_tokens)]):
            token_id = len(self.vocab)
            self.vocab[template] = token_id
            self.token_to_id[template] = token_id
            self.id_to_token[token_id] = template
            
        return template_counts
    
    def save_vocab(self, filepath: str):
        """Save vocabulary to JSON file."""
        vocab_data = {
            'vocab': self.vocab,
            'token_to_id': self.token_to_id,
            'id_to_token': self.id_to_token,
            'min_freq': self.min_freq,
            'max_vocab_size': self.max_vocab_size
        }
        with open(filepath, 'w') as f:
            json.dump(vocab_data, f, indent=2)

def load_all_templates():
    """Load all template files from data/parsed/ directory."""
    parsed_dir = Path("data/parsed")
    all_templates = {}
    
    if not parsed_dir.exists():
        print("Error: data/parsed/ directory not found!")
        return all_templates
    
    # Load all template JSON files
    for template_file in parsed_dir.glob("*_templates.json"):
        print(f"Loading templates from {template_file}...")
        with open(template_file, 'r') as f:
            templates = json.load(f)
            
        # Merge templates (handle duplicates by summing counts)
        for template_text, template_data in templates.items():
            if template_text in all_templates:
                all_templates[template_text]['count'] += template_data['count']
                all_templates[template_text]['examples'].extend(template_data['examples'])
            else:
                all_templates[template_text] = template_data
    
    return all_templates

def main():
    """Main function for building vocabulary."""
    print("Starting vocabulary builder...")
    
    # Load all templates
    all_templates = load_all_templates()
    
    if not all_templates:
        print("No templates found. Please run drain_parser.py first.")
        return
    
    print(f"Found {len(all_templates)} unique templates")
    
    # Build vocabulary
    builder = VocabularyBuilder(min_freq=2, max_vocab_size=50000)
    template_counts = builder.build_vocab(all_templates)
    
    # Save vocabulary
    vocab_file = "data/vocab.json"
    Path("data").mkdir(exist_ok=True)
    builder.save_vocab(vocab_file)
    
    print(f"Vocabulary built with {len(builder.vocab)} tokens")
    print(f"Saved vocabulary to {vocab_file}")

if __name__ == "__main__":
    main() 