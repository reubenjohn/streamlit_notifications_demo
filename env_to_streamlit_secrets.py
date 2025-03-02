#!/usr/bin/env python3

import os
import sys
import toml
from pathlib import Path

def main():
    """
    Create a Streamlit secrets.toml file from environment variables.
    Usage: python env_to_streamlit_secrets.py /path/to/secrets.toml
    """
    if len(sys.argv) < 2:
        print("Usage: python env_to_streamlit_secrets.py /path/to/secrets.toml")
        sys.exit(1)
    
    # Get the output file path
    output_file = sys.argv[1]
    
    # Create directory if it doesn't exist
    Path(output_file).parent.mkdir(parents=True, exist_ok=True)
    
    # Get all environment variables
    env_vars = {key: value for key, value in os.environ.items()}
    
    # Write to toml file
    with open(output_file, 'w') as f:
        toml.dump(env_vars, f)
    
    print(f"Environment variables written to {output_file}")

if __name__ == "__main__":
    main()