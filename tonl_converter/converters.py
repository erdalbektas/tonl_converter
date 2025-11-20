import json
import yaml
import re
from .core import loads, dumps

def to_json(data, **kwargs):
    return json.dumps(data, **kwargs)

def from_json(json_str, **kwargs):
    return json.loads(json_str, **kwargs)

def to_yaml(data, **kwargs):
    return yaml.dump(data, **kwargs)

def from_yaml(yaml_str, **kwargs):
    return yaml.safe_load(yaml_str, **kwargs)

def to_markdown(data):
    # Convert list of dicts to Markdown table
    # Expects data to be a dict where values are lists of dicts (TONL structure)
    # or just a list of dicts
    
    output = []
    
    if isinstance(data, list):
        # Single table
        output.append(_list_to_md_table(data))
    elif isinstance(data, dict):
        for key, value in data.items():
            output.append(f"## {key}")
            if isinstance(value, list) and value and isinstance(value[0], dict):
                output.append(_list_to_md_table(value))
            else:
                output.append(str(value))
            output.append("")
            
    return "\n".join(output)

def _list_to_md_table(data_list):
    if not data_list:
        return ""
    
    headers = list(data_list[0].keys())
    lines = []
    
    # Header row
    lines.append("| " + " | ".join(headers) + " |")
    # Separator row
    lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
    
    # Data rows
    for item in data_list:
        row = []
        for h in headers:
            val = item.get(h, "")
            row.append(str(val))
        lines.append("| " + " | ".join(row) + " |")
        
    return "\n".join(lines)

def from_markdown(md_str):
    # Extract tables from markdown
    # Returns a dict where keys are headers (if present) or generic names
    # and values are lists of dicts
    
    lines = md_str.strip().split('\n')
    data = {}
    current_key = "data"
    current_table_lines = []
    
    for line in lines:
        line = line.strip()
        if line.startswith('#'):
            # New section, save previous table if exists
            if current_table_lines:
                data[current_key] = _parse_md_table(current_table_lines)
                current_table_lines = []
            current_key = line.lstrip('#').strip()
        elif line.startswith('|'):
            current_table_lines.append(line)
        elif not line and current_table_lines:
            # End of table
            data[current_key] = _parse_md_table(current_table_lines)
            current_table_lines = []
            current_key = "data" # Reset or keep? Let's keep for now or reset to generic
            
    if current_table_lines:
        data[current_key] = _parse_md_table(current_table_lines)
        
    return data

def _parse_md_table(table_lines):
    if len(table_lines) < 3:
        return []
    
    # Parse headers
    headers = [h.strip() for h in table_lines[0].strip('|').split('|')]
    
    # Skip separator line (index 1)
    
    result = []
    for line in table_lines[2:]:
        values = [v.strip() for v in line.strip('|').split('|')]
        obj = {}
        for i, h in enumerate(headers):
            if i < len(values):
                # Basic type inference
                val = values[i]
                if val.isdigit():
                    val = int(val)
                elif val.lower() == 'true':
                    val = True
                elif val.lower() == 'false':
                    val = False
                obj[h] = val
        result.append(obj)
        
    return result
