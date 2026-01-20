"""Text processing utilities."""

import re
from typing import List


def split_text_into_chunks(text: str, max_length: int = 150) -> List[str]:
    """
    Split text into smaller chunks preserving sentence and punctuation structure.
    
    Args:
        text: Input text to split
        max_length: Maximum length of each chunk
        
    Returns:
        List of text chunks
    """
    # Clean up the text first
    text = text.strip()
    if not text:
        return []

    # Split by sentence-ending punctuation while preserving the punctuation
    sentence_pattern = r'([.!?]+)'
    parts = re.split(sentence_pattern, text)

    # Reconstruct sentences with their punctuation
    sentences = []
    i = 0
    while i < len(parts):
        if parts[i].strip():
            sentence = parts[i].strip()
            # Add punctuation if it exists
            if i + 1 < len(parts) and parts[i + 1].strip():
                sentence += parts[i + 1]
                i += 2
            else:
                # If no punctuation follows, add a period (only once)
                if not sentence.endswith(('.', '!', '?')):
                    sentence += '.'
                i += 1
            sentences.append(sentence)
        else:
            i += 1

    # Handle last part if not already included
    if len(parts) > 0 and parts[-1].strip():
        last_part = parts[-1].strip()
        if not any(last_part in s or s.startswith(last_part) for s in sentences):
            if not last_part.endswith(('.', '!', '?')):
                last_part += '.'
            sentences.append(last_part)

    # Group sentences into chunks
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        # If single sentence exceeds max_length, split by commas
        if len(sentence) > max_length:
            comma_parts = re.split(r'(,)', sentence)
            temp_sentence = ""
            
            i = 0
            while i < len(comma_parts):
                part = comma_parts[i].strip()
                comma = comma_parts[i + 1] if i + 1 < len(comma_parts) else ''
                
                # If part is still too long, split by words
                if len(part) > max_length:
                    words = part.split()
                    temp_words = []
                    
                    for word in words:
                        test_chunk = ' '.join(temp_words + [word])
                        if len(test_chunk) > max_length and temp_words:
                            if current_chunk:
                                chunks.append(current_chunk.strip())
                                current_chunk = ""
                            chunks.append(' '.join(temp_words))
                            temp_words = [word]
                        else:
                            temp_words.append(word)
                    
                    if temp_words:
                        part = ' '.join(temp_words) + comma
                        if current_chunk and len(current_chunk + ' ' + part) > max_length:
                            chunks.append(current_chunk.strip())
                            current_chunk = part
                        else:
                            current_chunk += (' ' if current_chunk else '') + part
                else:
                    part_with_comma = part + comma
                    if current_chunk and len(current_chunk + ' ' + part_with_comma) > max_length:
                        chunks.append(current_chunk.strip())
                        current_chunk = part_with_comma
                    else:
                        current_chunk += (' ' if current_chunk else '') + part_with_comma
                
                i += 2 if i + 1 < len(comma_parts) else 1
        else:
            # Normal sentence that fits within limit
            if current_chunk and len(current_chunk + ' ' + sentence) > max_length:
                chunks.append(current_chunk.strip())
                current_chunk = sentence
            else:
                current_chunk += (' ' if current_chunk else '') + sentence

    # Always add remaining chunk at the end
    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    # Filter out empty or duplicate chunks
    final_chunks = []
    for chunk in chunks:
        if chunk.strip() and (not final_chunks or chunk.strip() != final_chunks[-1]):
            final_chunks.append(chunk.strip())

    return final_chunks


def format_time(seconds: float) -> str:
    """
    Format seconds into a readable time string.
    
    Args:
        seconds: Time in seconds
        
    Returns:
        Formatted time string
    """
    if seconds < 60:
        return f"{seconds:.1f} seconds"
    minutes = int(seconds // 60)
    secs = seconds % 60
    return f"{minutes} minute{'s' if minutes != 1 else ''} {secs:.1f} seconds"
