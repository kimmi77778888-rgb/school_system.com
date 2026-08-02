"""
Khmer Text Utilities
====================
Helper functions for handling Khmer Unicode text properly.
"""

import unicodedata
import re


def clean_khmer_text(text):
    """
    Clean Khmer text by removing invisible characters and normalizing Unicode.
    
    Common issues:
    - Zero-Width Space (U+200B)
    - Zero-Width Non-Joiner (U+200C)
    - Zero-Width Joiner (U+200D)
    - Other invisible formatting characters
    
    Args:
        text (str): Input text to clean
        
    Returns:
        str: Cleaned text
    """
    if not text:
        return text
    
    # Remove Zero-Width characters
    text = text.replace('\u200B', '')  # Zero-Width Space
    text = text.replace('\u200C', '')  # Zero-Width Non-Joiner
    text = text.replace('\u200D', '')  # Zero-Width Joiner
    text = text.replace('\uFEFF', '')  # Zero-Width No-Break Space (BOM)
    
    # Remove other invisible/control characters (except normal spaces and newlines)
    text = ''.join(char for char in text if unicodedata.category(char)[0] != 'C' or char in '\n\r\t ')
    
    # Normalize Unicode to NFC (Canonical Composition)
    # This combines separate characters like base + vowel into single code points
    text = unicodedata.normalize('NFC', text)
    
    # Remove multiple consecutive spaces
    text = re.sub(r' +', ' ', text)
    
    # Trim whitespace
    text = text.strip()
    
    return text


def normalize_khmer_name(first_name, last_name):
    """
    Normalize Khmer names by cleaning both first and last names.
    
    Args:
        first_name (str): First name
        last_name (str): Last name
        
    Returns:
        tuple: (cleaned_first_name, cleaned_last_name)
    """
    first_clean = clean_khmer_text(first_name) if first_name else ''
    last_clean = clean_khmer_text(last_name) if last_name else ''
    
    return first_clean, last_clean


def detect_invisible_chars(text):
    """
    Detect invisible characters in text for debugging.
    
    Args:
        text (str): Text to check
        
    Returns:
        list: List of (position, character, unicode_name) tuples
    """
    if not text:
        return []
    
    invisible_chars = []
    zero_width_chars = ['\u200B', '\u200C', '\u200D', '\uFEFF']
    
    for i, char in enumerate(text):
        if char in zero_width_chars or unicodedata.category(char)[0] == 'C':
            try:
                char_name = unicodedata.name(char, 'UNKNOWN')
            except ValueError:
                char_name = 'UNNAMED'
            
            invisible_chars.append((i, repr(char), char_name))
    
    return invisible_chars


def format_khmer_text_html(text):
    """
    Format Khmer text for HTML display with proper styling.
    Returns HTML with appropriate CSS classes.
    
    Args:
        text (str): Khmer text to format
        
    Returns:
        str: HTML formatted text
    """
    cleaned = clean_khmer_text(text)
    # Add CSS class for proper Khmer rendering
    return f'<span class="khmer-text">{cleaned}</span>'


# CSS to add to templates for proper Khmer rendering
KHMER_CSS = """
<style>
.khmer-text {
    font-family: 'Khmer OS Siemreap', 'Khmer OS', 'Hanuman', 'Battambang', sans-serif;
    letter-spacing: 0;
    word-spacing: 0;
}
</style>
"""
