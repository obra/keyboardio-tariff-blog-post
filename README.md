# Keyboardio Tariff Blog Post Updater

A simple tool to update the tariff rates and product prices in the Keyboardio tariff blog post.

The live blog post can be found at: [An Open Letter to U.S. Customers](https://shop.keyboard.io/blogs/news/an-open-letter-to-u-s-customers)

## Usage

```bash
# Make the script executable
chmod +x update_tariff.py

# Update tariff rate to 150%
./update_tariff.py 150

# Update tariff rate with an additional note
./update_tariff.py 150 --note "add information about import restrictions"

# Specify a different file
./update_tariff.py 150 --file /path/to/post.html
```

## Features

- Adds a timestamped update note at the top of the blog post
- Updates the tariff percentage throughout the post
- Recalculates and updates the tariff amounts for the Atreus ($149) and Model 100 ($349)
- Preserves the history of previous rates by striking through old values

## Requirements

- Python 3.6+