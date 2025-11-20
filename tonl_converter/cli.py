import argparse
import sys
import os
from . import core, converters

def main():
    parser = argparse.ArgumentParser(description="TONL Converter")
    parser.add_argument("input_file", help="Path to input file")
    parser.add_argument("output_file", help="Path to output file")
    parser.add_argument("--format", choices=["json", "yaml", "markdown", "tonl"], help="Output format (default: inferred from extension)")
    
    args = parser.parse_args()
    
    # Read input
    with open(args.input_file, 'r') as f:
        content = f.read()
        
    input_ext = os.path.splitext(args.input_file)[1].lower()
    
    data = None
    if input_ext == '.json':
        data = converters.from_json(content)
    elif input_ext in ['.yaml', '.yml']:
        data = converters.from_yaml(content)
    elif input_ext == '.md':
        data = converters.from_markdown(content)
    elif input_ext == '.tonl':
        data = core.loads(content)
    else:
        print(f"Unsupported input format: {input_ext}")
        sys.exit(1)
        
    # Determine output format
    output_format = args.format
    if not output_format:
        output_ext = os.path.splitext(args.output_file)[1].lower()
        if output_ext == '.json':
            output_format = 'json'
        elif output_ext in ['.yaml', '.yml']:
            output_format = 'yaml'
        elif output_ext == '.md':
            output_format = 'markdown'
        elif output_ext == '.tonl':
            output_format = 'tonl'
        else:
            print(f"Could not infer output format from extension: {output_ext}")
            sys.exit(1)
            
    # Convert
    output_content = ""
    if output_format == 'json':
        output_content = converters.to_json(data, indent=2)
    elif output_format == 'yaml':
        output_content = converters.to_yaml(data)
    elif output_format == 'markdown':
        output_content = converters.to_markdown(data)
    elif output_format == 'tonl':
        output_content = core.dumps(data)
        
    # Write output
    with open(args.output_file, 'w') as f:
        f.write(output_content)
        
    print(f"Converted {args.input_file} to {args.output_file}")

if __name__ == "__main__":
    main()
