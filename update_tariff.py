#!/usr/bin/env python3

import re
import datetime
import argparse
from pathlib import Path

# Current base prices
ATREUS_PRICE = 149
MODEL_100_PRICE = 349

def add_timestamp_update(content, new_tariff_rate, note=""):
    """Add a timestamped update note at the top of the blog post"""
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M PDT")
    
    note_text = f"to reflect new {new_tariff_rate}% tariff rate"
    if note:
        note_text += f" and {note}"
    
    update_line = f'<p><em><strong>Updated {timestamp} {note_text}.</strong></em></p>\n'
    
    # Find the last update note and insert after it
    last_update_pos = content.rfind('<p><em><strong>Updated ')
    if last_update_pos != -1:
        end_pos = content.find('</p>', last_update_pos) + 4
        return content[:end_pos] + '\n' + update_line + content[end_pos:]
    else:
        # If no update notes found, add to the top
        return update_line + content

def update_tariff_rate(content, old_rate, new_rate):
    """Update the tariff rate in the blog post by striking through the old rate"""
    # Look for patterns like: <s>54%</s> <s>104%</s> <s>125%</s> 145%
    main_pattern = f'(<s>.*?</s> <s>.*?</s> <s>.*?</s>) {old_rate}%'
    match = re.search(main_pattern, content)
    
    if match:
        # Update the main occurrences
        prefix = match.group(1)
        updated = f"{prefix} <s>{old_rate}%</s> {new_rate}%"
        content = content.replace(f"{prefix} {old_rate}%", updated)
    
    # Update all remaining standalone instances
    remaining_pattern = f'(?<!<s>){old_rate}%(?!</s>)'
    content = re.sub(remaining_pattern, f'<s>{old_rate}%</s> {new_rate}%', content)
    
    return content

def update_product_prices(content, new_tariff_rate):
    """Update the product prices based on the new tariff rate"""
    # Calculate new tax amounts
    new_atreus_tax = int(ATREUS_PRICE * new_tariff_rate / 100)
    new_model100_tax = int(MODEL_100_PRICE * new_tariff_rate / 100)
    
    # Find the Model 100 tax line
    model100_tax_pattern = r'on a Model 100 \+ additional customs clearance fees\. The new US taxes on the Atreus will be'
    model100_section = content.split(model100_tax_pattern)[0]
    
    model100_tax_line = re.search(r'<s>\$\d+</s> <s>\$\d+</s> <s>\$\d+</s> \$(\d+)', model100_section)
    if model100_tax_line:
        old_tax = model100_tax_line.group(1)
        old_text = f'<s>$188</s> <s>$363</s> <s>$436</s> ${old_tax}'
        new_text = f'<s>$188</s> <s>$363</s> <s>$436</s> <s>${old_tax}</s> ${new_model100_tax}'
        content = content.replace(old_text, new_text)
    
    # Find the Atreus tax line
    atreus_tax_pattern = r'The new US taxes on the Atreus will be <s>\$\d+</s> <s>\$\d+</s> <s>\$\d+</s> \$(\d+)'
    atreus_match = re.search(atreus_tax_pattern, content)
    if atreus_match:
        old_tax = atreus_match.group(1)
        old_text = f'<s>$80</s> <s>$155</s> <s>$186</s> ${old_tax}'
        new_text = f'<s>$80</s> <s>$155</s> <s>$186</s> <s>${old_tax}</s> ${new_atreus_tax}'
        content = content.replace(old_text, new_text)
    
    return content

def main():
    parser = argparse.ArgumentParser(description='Update tariff rates and prices in the blog post')
    parser.add_argument('new_rate', type=int, help='New tariff rate percentage')
    parser.add_argument('--note', type=str, default="", help='Additional note to add to the update message')
    parser.add_argument('--file', type=str, default="post.html", help='Path to the blog post HTML file')
    args = parser.parse_args()
    
    file_path = Path(args.file)
    if not file_path.exists():
        print(f"Error: File {file_path} not found")
        return
    
    # Read the current content
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Find the current tariff rate
    rate_pattern = r'<s>.*?</s> <s>.*?</s> <s>.*?</s> (\d+)%'
    current_rate_match = re.search(rate_pattern, content)
    if current_rate_match:
        current_rate = int(current_rate_match.group(1))
    else:
        print("Could not find current tariff rate in the blog post")
        return
    
    # Create a backup of the original file
    backup_path = file_path.with_suffix('.html.bak')
    with open(backup_path, 'w') as f:
        f.write(content)
    
    # Update the content
    updated_content = add_timestamp_update(content, args.new_rate, args.note)
    updated_content = update_tariff_rate(updated_content, current_rate, args.new_rate)
    updated_content = update_product_prices(updated_content, args.new_rate)
    
    # Write the updated content
    with open(file_path, 'w') as f:
        f.write(updated_content)
    
    print(f"Updated tariff rate from {current_rate}% to {args.new_rate}%")
    print(f"Updated Model 100 tax to ${int(MODEL_100_PRICE * args.new_rate / 100)}")
    print(f"Updated Atreus tax to ${int(ATREUS_PRICE * args.new_rate / 100)}")
    print(f"Backup created at {backup_path}")

if __name__ == "__main__":
    main()