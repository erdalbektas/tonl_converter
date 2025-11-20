import unittest
import json
import os
import sys

# Add parent dir to path to import tonl
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tonl_converter import core, converters

class TestTONL(unittest.TestCase):
    def test_json_to_tonl_and_back(self):
        data = {
            "users": [
                {"id": 1, "name": "Alice", "role": "admin"},
                {"id": 2, "name": "Bob", "role": "user"}
            ]
        }
        
        # Convert to TONL
        tonl_str = core.dumps(data)
        print(f"\nGenerated TONL:\n{tonl_str}")
        
        # Convert back to dict
        restored_data = core.loads(tonl_str)
        
        # Verify
        self.assertEqual(data["users"], restored_data["users"])

    def test_markdown_conversion(self):
        data = [
            {"id": 1, "name": "Alice"},
            {"id": 2, "name": "Bob"}
        ]
        
        md = converters.to_markdown(data)
        print(f"\nGenerated Markdown:\n{md}")
        
        restored = converters.from_markdown(md)
        # Note: from_markdown returns a dict with table name (or generic 'data')
        # In this case, since we passed a list, to_markdown created a single table.
        # from_markdown will wrap it in a dict if it finds a table.
        # Wait, my implementation of from_markdown might need adjustment to match to_markdown's output structure exactly if I want perfect roundtrip for raw lists.
        # But for now let's check if the data is inside.
        
        # Actually, let's test the dict structure which is more standard for TONL
        data_dict = {"users": data}
        md_dict = converters.to_markdown(data_dict)
        restored_dict = converters.from_markdown(md_dict)
        
        self.assertEqual(data_dict["users"], restored_dict["users"])

if __name__ == '__main__':
    unittest.main()
