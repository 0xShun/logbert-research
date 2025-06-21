"""
Tokenization Utilities for LogBERT

Helper functions for tokenization, padding, and sequence processing.
"""

import numpy as np
from typing import List, Tuple, Union
import torch

def pad_sequences(sequences: List[List[int]], max_length: int, 
                  padding_value: int = 0) -> np.ndarray:
    """
    Pad sequences to the same length.
    
    Args:
        sequences: List of token sequences
        max_length: Maximum sequence length
        padding_value: Value to use for padding
        
    Returns:
        Padded sequences as numpy array
    """
    padded = []
    for seq in sequences:
        if len(seq) > max_length:
            seq = seq[:max_length]
        else:
            seq = seq + [padding_value] * (max_length - len(seq))
        padded.append(seq)
    return np.array(padded)

def create_attention_mask(sequences: np.ndarray, padding_value: int = 0) -> np.ndarray:
    """
    Create attention mask for padded sequences.
    
    Args:
        sequences: Padded sequences
        padding_value: Value used for padding
        
    Returns:
        Attention mask (1 for real tokens, 0 for padding)
    """
    mask = (sequences != padding_value).astype(np.int64)
    return mask

def create_masked_lm_labels(sequences: np.ndarray, mask_prob: float = 0.15,
                           vocab_size: int = 50000) -> Tuple[np.ndarray, np.ndarray]:
    """
    Create masked language modeling labels.
    
    Args:
        sequences: Input sequences
        mask_prob: Probability of masking tokens
        vocab_size: Size of vocabulary
        
    Returns:
        Tuple of (masked_sequences, labels)
    """
    masked_sequences = sequences.copy()
    labels = np.full_like(sequences, -100)  # -100 is ignored in loss computation
    
    for i in range(len(sequences)):
        for j in range(len(sequences[i])):
            if np.random.random() < mask_prob:
                labels[i, j] = sequences[i, j]
                masked_sequences[i, j] = 2  # MASK token ID
                
    return masked_sequences, labels

def truncate_sequences(sequences: List[List[int]], max_length: int) -> List[List[int]]:
    """
    Truncate sequences to maximum length.
    
    Args:
        sequences: List of token sequences
        max_length: Maximum allowed length
        
    Returns:
        Truncated sequences
    """
    return [seq[:max_length] for seq in sequences]

def tokenize_text(text: str, vocab: dict, max_length: int = None) -> List[int]:
    """
    Simple tokenization function.
    
    Args:
        text: Input text
        vocab: Vocabulary dictionary
        max_length: Maximum sequence length
        
    Returns:
        List of token IDs
    """
    # Simple word-level tokenization
    tokens = text.split()
    token_ids = [vocab.get(token, vocab.get('<UNK>', 1)) for token in tokens]
    
    if max_length:
        token_ids = token_ids[:max_length]
        
    return token_ids

def batch_encode(sequences: List[str], vocab: dict, max_length: int = 512) -> np.ndarray:
    """
    Encode a batch of text sequences.
    
    Args:
        sequences: List of text sequences
        vocab: Vocabulary dictionary
        max_length: Maximum sequence length
        
    Returns:
        Encoded sequences as numpy array
    """
    encoded = [tokenize_text(seq, vocab, max_length) for seq in sequences]
    return pad_sequences(encoded, max_length) 