# j2y.py - Pure Python JSON to YAML converter (no libraries)
import sys
import os

def tokenize(json_text):
    i = 0
    length = len(json_text)

    while i < length:
        c = json_text[i]

        if c in ' \n\r\t':
            i += 1
            continue
        elif c in '{},[]:':
            yield c
            i += 1
        elif c == '"':
            i += 1
            start = i
            while json_text[i] != '"':
                if json_text[i] == '\\': i += 1
                i += 1
            yield ("STRING", json_text[start:i])
            i += 1
        elif c.isdigit() or c == '-':
            start = i
            while i < length and (json_text[i].isdigit() or json_text[i] in '.eE+-'):
                i += 1
            yield ("NUMBER", json_text[start:i])
        elif json_text.startswith("true", i):
            yield ("BOOLEAN", "true")
            i += 4
        elif json_text.startswith("false", i):
            yield ("BOOLEAN", "false")
            i += 5
        elif json_text.startswith("null", i):
            yield ("NULL", "null")
            i += 4
        else:
            raise Exception(f"Unexpected character: {c} at position {i}")

def to_yaml(data, indent=0, output_lines=None):
    if output_lines is None:
        output_lines = []

    prefix = '  ' * indent
    if isinstance(data, dict):
        for key, val in data.items():
            if isinstance(val, (dict, list)):
                output_lines.append(f"{prefix}{key}:")
                to_yaml(val, indent + 1, output_lines)
            else:
                value_str = f'"{val}"' if isinstance(val, str) else str(val)
                output_lines.append(f"{prefix}{key}: {value_str}")
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, (dict, list)):
                output_lines.append(f"{prefix}-")
                to_yaml(item, indent + 1, output_lines)
            else:
                value_str = f'"{item}"' if isinstance(item, str) else str(item)
                output_lines.append(f"{prefix}- {value_str}")
    return output_lines

class TokenStream:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0

    def next(self):
        if self.index < len(self.tokens):
            tok = self.tokens[self.index]
            self.index += 1
            return tok
        else:
            raise StopIteration

    def peek(self):
        if self.index < len(self.tokens):
            return self.tokens[self.index]
        else:
            return None

# === Main Execution ===
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Please provide the JSON file path as argument.")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = os.path.splitext(input_file)[0] + "_converted.yaml"

    with open(input_file, "r") as f:
        json_text = f.read()

    tokens = list(tokenize(json_text))
    stream = TokenStream(tokens)

    def parse_value():
        tok = stream.peek()
        if tok == '{':
            stream.next()
            return parse_object()
        elif tok == '[':
            stream.next()
            return parse_array()
        elif isinstance(tok, tuple):
            stream.next()
            if tok[0] == "STRING":
                return tok[1]
            elif tok[0] == "NUMBER":
                try:
                    return int(tok[1])
                except:
                    return float(tok[1])
            elif tok[0] == "BOOLEAN":
                return tok[1] == "true"
            elif tok[0] == "NULL":
                return None
        raise Exception(f"Unexpected token: {tok}")

    def parse_object():
        obj = {}
        tok = stream.peek()
        if tok == '}':
            stream.next()
            return obj
        while True:
            key_tok = stream.next()
            if not isinstance(key_tok, tuple) or key_tok[0] != "STRING":
                raise Exception(f"Expected string key but got {key_tok}")
            if stream.next() != ':':
                raise Exception("Expected ':' after key")
            value = parse_value()
            obj[key_tok[1]] = value
            tok = stream.peek()
            if tok == '}':
                stream.next()
                break
            if tok != ',':
                raise Exception("Expected ',' or '}' in object")
            stream.next()
        return obj

    def parse_array():
        arr = []
        tok = stream.peek()
        if tok == ']':
            stream.next()
            return arr
        while True:
            val = parse_value()
            arr.append(val)
            tok = stream.peek()
            if tok == ']':
                stream.next()
                break
            if tok != ',':
                raise Exception("Expected ',' or ']' in array")
            stream.next()
        return arr

    data = parse_value()
    yaml_lines = to_yaml(data)

    with open(output_file, "w") as f:
        f.write('\n'.join(yaml_lines))

    print(f"YAML conversion complete. Output saved to {output_file}")
