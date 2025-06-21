"""
Drain Parser for Log Template Extraction

This module implements the Drain log parser algorithm for extracting
log templates from raw log files in data/raw/ and saving them to data/parsed/.
"""

import re
import json
import os
from typing import List, Dict, Tuple
import logging
from pathlib import Path

class DrainParser:
    """
    Drain log parser implementation for template extraction.
    """
    
    def __init__(self, depth: int = 4, sim_threshold: float = 0.4):
        """
        Initialize Drain parser.
        
        Args:
            depth: Depth of the parse tree
            sim_threshold: Similarity threshold for template matching
        """
        self.depth = depth
        self.sim_threshold = sim_threshold
        self.parse_tree = {}
        self.templates = {}
        self.template_id = 0
        
    def parse_log(self, log_line: str) -> str:
        """
        Parse a single log line and return its template.
        
        Args:
            log_line: Raw log line to parse
            
        Returns:
            Extracted template for the log line
        """
        # Remove timestamp and other variable parts
        # This is a simplified version - you can enhance this based on your log format
        template = self._extract_template(log_line)
        
        # Add to templates if not seen before
        if template not in self.templates:
            self.templates[template] = {
                'id': self.template_id,
                'count': 1,
                'examples': [log_line]
            }
            self.template_id += 1
        else:
            self.templates[template]['count'] += 1
            self.templates[template]['examples'].append(log_line)
            
        return template
    
    def _extract_template(self, log_line: str) -> str:
        """
        Extract template from log line by removing variable parts.
        
        Args:
            log_line: Raw log line
            
        Returns:
            Template with variable parts replaced by <*> placeholders
        """
        # Remove timestamp patterns (common formats)
        timestamp_patterns = [
            r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}',  # 2024-01-01 10:00:00
            r'\d{2}/\d{2}/\d{4} \d{2}:\d{2}:\d{2}',  # 01/01/2024 10:00:00
            r'\d{10,}',  # Unix timestamp
        ]
        
        template = log_line
        for pattern in timestamp_patterns:
            template = re.sub(pattern, '<timestamp>', template)
        
        # Replace IP addresses
        template = re.sub(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', '<ip>', template)
        
        # Replace numbers (but keep small ones that might be important)
        template = re.sub(r'\b\d{5,}\b', '<number>', template)
        
        # Replace file paths
        template = re.sub(r'/[^\s]+', '<path>', template)
        
        # Replace UUIDs
        template = re.sub(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', '<uuid>', template)
        
        return template.strip()
    
    def extract_templates(self, log_lines: List[str]) -> Dict[str, int]:
        """
        Extract templates from a list of log lines.
        
        Args:
            log_lines: List of raw log lines
            
        Returns:
            Dictionary mapping templates to their frequencies
        """
        for log_line in log_lines:
            self.parse_log(log_line)
            
        return {template: data['count'] for template, data in self.templates.items()}
    
    def save_templates(self, output_file: str):
        """
        Save extracted templates to JSON file.
        
        Args:
            output_file: Path to save templates JSON
        """
        with open(output_file, 'w') as f:
            json.dump(self.templates, f, indent=2)
    
    def load_templates(self, input_file: str):
        """
        Load templates from JSON file.
        
        Args:
            input_file: Path to templates JSON file
        """
        with open(input_file, 'r') as f:
            self.templates = json.load(f)

def process_raw_logs():
    """
    Process all raw log files in data/raw/ and save templates to data/parsed/.
    """
    raw_dir = Path("data/raw")
    parsed_dir = Path("data/parsed")
    
    # Create parsed directory if it doesn't exist
    parsed_dir.mkdir(parents=True, exist_ok=True)
    
    # Process each log file in raw directory
    for log_file in raw_dir.glob("*.log"):
        print(f"Processing {log_file}...")
        
        # Read log lines
        with open(log_file, 'r', encoding='utf-8', errors='ignore') as f:
            log_lines = [line.strip() for line in f if line.strip()]
        
        # Extract templates
        parser = DrainParser()
        templates = parser.extract_templates(log_lines)
        
        # Save templates to JSON
        output_file = parsed_dir / f"{log_file.stem}_templates.json"
        parser.save_templates(str(output_file))
        
        print(f"Extracted {len(templates)} templates from {log_file}")
        print(f"Saved templates to {output_file}")

def main():
    """Main function for processing raw logs."""
    print("Starting Drain parser for log template extraction...")
    
    # Check if raw directory exists
    if not Path("data/raw").exists():
        print("Error: data/raw/ directory not found!")
        print("Please create data/raw/ and place your log files there.")
        return
    
    # Process all raw log files
    process_raw_logs()
    
    print("Template extraction completed!")

if __name__ == "__main__":
    main() 