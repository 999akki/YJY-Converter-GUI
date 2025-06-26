import sys
import os
import json

def parse_value(val):
    val = val.strip()
    if val.startswith('"') and val.endswith('"'):
        return val[1:-1]
    elif val == "true":
        return True
    elif val == "false":
        return False
    elif val == "null":
        return None
    else:
        try:
            if '.' in val:
                return float(val)
            else:
                return int(val)
        except:
            return val

def parse_yaml(lines):
    root = {}
    stack = [root]
    indent_stack = [0]

    for line in lines:
        if not line.strip():
            continue

        indent = len(line) - len(line.lstrip())
        content = line.strip()

        while len(indent_stack) > 1 and indent < indent_stack[-1]:
            stack.pop()
            indent_stack.pop()

        if content.startswith('-'):
            value = content[1:].strip()

            if not isinstance(stack[-1], list):
                if len(stack) >= 2 and isinstance(stack[-2], dict):
                    parent_dict = stack[-2]
                    current_dict = stack[-1]

                    list_key = None
                    for k, v in parent_dict.items():
                        if v is current_dict:
                            list_key = k
                            break

                    if list_key:
                        parent_dict[list_key] = []
                        stack[-1] = parent_dict[list_key]
                else:
                    new_list = []
                    stack.append(new_list)
                    indent_stack.append(indent)

            if value == "":
                new_dict = {}
                stack[-1].append(new_dict)
                stack.append(new_dict)
                indent_stack.append(indent + 2)
            else:
                stack[-1].append(parse_value(value))

        elif ':' in content:
            key, sep, val = content.partition(':')
            key = key.strip()
            val = val.strip()

            if isinstance(stack[-1], list):
                new_dict = {}
                stack[-1].append(new_dict)
                stack.append(new_dict)
                indent_stack.append(indent)

            if isinstance(stack[-1], dict):
                if val == "":
                    stack[-1][key] = {}
                    stack.append(stack[-1][key])
                    indent_stack.append(indent + 2)
                else:
                    stack[-1][key] = parse_value(val)

    return root

def write_json(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)

# === Main Execution ===
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide the YAML file path as argument.")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = os.path.splitext(input_file)[0] + "_converted.json"

    with open(input_file, "r") as f:
        yaml_lines = f.readlines()

    parsed_data = parse_yaml(yaml_lines)
    write_json(parsed_data, output_file)

    print(f"YAML to JSON conversion complete. Output saved to {output_file}")
