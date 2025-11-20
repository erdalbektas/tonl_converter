import re
import json

class TONLDocument:
    def __init__(self, data=None):
        self.data = data if data is not None else {}

    @classmethod
    def from_string(cls, content):
        # Basic parser implementation
        # This is a simplified parser focusing on the tabular format shown in examples
        data = {}
        lines = content.strip().split('\n')
        
        current_key = None
        current_schema = []
        current_rows = []
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
                
            # Check for table definition: key[count]{schema}:
            # Regex to match: key[count]{schema}:
            # Example: users[3]{id:u32,name:str,role:str}:
            match = re.match(r'(\w+)\[(\d+)\]\s*\{(.*?)\}:', line)
            if match:
                # Save previous table if exists
                if current_key:
                    data[current_key] = cls._process_rows(current_rows, current_schema)
                
                current_key = match.group(1)
                # count = int(match.group(2)) # unused for now, but could be used for validation
                schema_str = match.group(3)
                current_schema = [s.split(':')[0].strip() for s in schema_str.split(',')]
                current_rows = []
                continue
            
            # Check for simple key-value: key: value
            # Example: version: 1.0
            simple_match = re.match(r'(\w+):\s*(.*)', line)
            if simple_match and not current_key: # Only if not inside a table definition (simplified)
                 # Actually, the example shows nested objects too. 
                 # For MVP, let's stick to the tabular format parsing or simple KV if not in table.
                 # But wait, the example: users[3]... followed by rows.
                 # If we are in a table, lines are rows.
                 pass

            if current_key:
                # Parse row
                # Handle quoted strings, etc. Simplified CSV-like parsing.
                # This is a naive split, needs to handle commas in quotes
                row_values = cls._parse_csv_line(line)
                current_rows.append(row_values)

        # Save last table
        if current_key:
            data[current_key] = cls._process_rows(current_rows, current_schema)
            
        return cls(data)

    @staticmethod
    def _process_rows(rows, schema):
        result = []
        for row in rows:
            obj = {}
            for i, field in enumerate(schema):
                if i < len(row):
                    val = row[i]
                    # Basic type inference or cleanup
                    if val.isdigit():
                        val = int(val)
                    elif val.lower() == 'true':
                        val = True
                    elif val.lower() == 'false':
                        val = False
                    elif val.startswith('"') and val.endswith('"'):
                        val = val[1:-1]
                    obj[field] = val
            result.append(obj)
        return result

    @staticmethod
    def _parse_csv_line(line):
        # A simple CSV parser that handles quoted strings
        values = []
        current_val = []
        in_quote = False
        for char in line:
            if char == '"':
                in_quote = not in_quote
            elif char == ',' and not in_quote:
                values.append("".join(current_val).strip())
                current_val = []
                continue
            current_val.append(char)
        values.append("".join(current_val).strip())
        return values

    def to_string(self):
        output = ["#version 1.0"]
        
        for key, value in self.data.items():
            if isinstance(value, list) and len(value) > 0 and isinstance(value[0], dict):
                # Tabular format
                schema_keys = list(value[0].keys())
                # Infer types for schema (simplified)
                schema_def = []
                for k in schema_keys:
                    # Naive type inference
                    val = value[0][k]
                    type_name = 'str'
                    if isinstance(val, int):
                        type_name = 'u32' # Generic int
                    elif isinstance(val, bool):
                        type_name = 'bool'
                    schema_def.append(f"{k}:{type_name}")
                
                header = f"{key}[{len(value)}] {{{','.join(schema_def)}}}:"
                output.append(header)
                
                for item in value:
                    row = []
                    for k in schema_keys:
                        val = item.get(k, "")
                        if isinstance(val, str):
                            if "," in val or " " in val:
                                val = f'"{val}"'
                        row.append(str(val))
                    output.append(", ".join(row))
            else:
                # Fallback or simple KV (not fully implemented in this MVP)
                pass
                
        return "\n".join(output)

def load(fp):
    return loads(fp.read())

def loads(s):
    doc = TONLDocument.from_string(s)
    return doc.data

def dump(obj, fp):
    fp.write(dumps(obj))

def dumps(obj):
    doc = TONLDocument(obj)
    return doc.to_string()
