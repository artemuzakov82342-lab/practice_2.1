def serialize(obj, indent=None, level=0):
    if obj is None:
        return 'null'
    if isinstance(obj, bool):
        return 'true' if obj else 'false'
    if isinstance(obj, (int, float)):
        return str(obj)
    if isinstance(obj, str):
        return f'"{escape_string(obj)}"'
    if isinstance(obj, (list, tuple)):
        if indent is None:
            items = [serialize(item, indent, level) for item in obj]
            return '[' + ', '.join(items) + ']'
        else:
            items = [serialize(item, indent, level + 1) for item in obj]
            space = ' ' * indent * (level + 1)
            comma_space = ' ' * indent * level
            if not items:
                return '[]'
            return '[\n' + ',\n'.join([space + item for item in items]) + f'\n{comma_space}]'
    if isinstance(obj, dict):
        if indent is None:
            items = [f'{serialize(k, indent, level)}: {serialize(v, indent, level)}'
                     for k, v in obj.items()]
            return '{' + ', '.join(items) + '}'
        else:
            space = ' ' * indent * (level + 1)
            comma_space = ' ' * indent * level
            items = [f'{space}{serialize(k, indent, level)}: {serialize(v, indent, level)}'
                     for k, v in obj.items()]
            if not items:
                return '{}'
            return '{\n' + ',\n'.join(items) + f'\n{comma_space}}}'
    raise TypeError(f'Object of type {type(obj)} is not JSON serializable')


def escape_string(s):
    s = s.replace('\\', '\\\\')
    s = s.replace('"', '\\"')
    s = s.replace('\n', '\\n')
    s = s.replace('\r', '\\r')
    s = s.replace('\t', '\\t')
    return s


def unescape_string(s):
    s = s.replace('\\n', '\n')
    s = s.replace('\\r', '\r')
    s = s.replace('\\t', '\t')
    s = s.replace('\\"', '"')
    s = s.replace('\\\\', '\\')
    return s


def deserialize(json_str):
    json_str = json_str.strip()
    if not json_str:
        raise ValueError("Empty JSON string")

    if json_str[0] == '{':
        return parse_object(json_str)
    elif json_str[0] == '[':
        return parse_array(json_str)
    elif json_str[0] == '"':
        return parse_string(json_str)
    elif json_str == 'null':
        return None
    elif json_str == 'true':
        return True
    elif json_str == 'false':
        return False
    else:
        return parse_number(json_str)


def parse_object(s):
    s = s.strip()
    if s[0] != '{' or s[-1] != '}':
        raise ValueError("Invalid object")

    if len(s) == 2:
        return {}

    result = {}
    content = s[1:-1].strip()
    pairs = split_json(content)

    for pair in pairs:
        if ':' not in pair:
            raise ValueError("Invalid key-value pair")

        colon_idx = find_first_colon(pair)
        key = pair[:colon_idx].strip()
        value_str = pair[colon_idx + 1:].strip()

        if key[0] != '"' or key[-1] != '"':
            raise ValueError("Key must be string")

        key = unescape_string(key[1:-1])
        result[key] = deserialize(value_str)

    return result


def parse_array(s):
    s = s.strip()
    if s[0] != '[' or s[-1] != ']':
        raise ValueError("Invalid array")

    if len(s) == 2:
        return []

    content = s[1:-1].strip()
    items = split_json(content)
    return [deserialize(item) for item in items]


def parse_string(s):
    if s[0] != '"' or s[-1] != '"':
        raise ValueError("Invalid string")
    return unescape_string(s[1:-1])


def parse_number(s):
    try:
        if '.' in s:
            return float(s)
        return int(s)
    except ValueError:
        raise ValueError(f"Invalid number: {s}")


def split_json(s):
    parts = []
    current = ""
    depth = 0
    in_string = False

    for char in s:
        if char == '"' and not (current and current[-1] == '\\'):
            in_string = not in_string

        if not in_string:
            if char in '{[':
                depth += 1
            elif char in '}]':
                depth -= 1
            elif char == ',' and depth == 0:
                parts.append(current.strip())
                current = ""
                continue

        current += char

    if current.strip():
        parts.append(current.strip())

    return parts


def find_first_colon(s):
    depth = 0
    in_string = False

    for i, char in enumerate(s):
        if char == '"' and not (i > 0 and s[i - 1] == '\\'):
            in_string = not in_string
        if not in_string:
            if char in '{[':
                depth += 1
            elif char in '}]':
                depth -= 1
            elif char == ':' and depth == 0:
                return i
    return -1


def validate_json(json_str):
    lines = json_str.split('\n')

    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if not stripped:
            continue

        bracket_stack = []
        in_string = False
        escape = False

        for j, char in enumerate(line):
            if escape:
                escape = False
                continue

            if char == '\\':
                escape = True
                continue

            if char == '"' and not escape:
                in_string = not in_string
                continue

            if not in_string:
                if char in '{[':
                    bracket_stack.append((char, i, j + 1))
                elif char == '}':
                    if not bracket_stack or bracket_stack[-1][0] != '{':
                        return False, i, f"Unexpected '}}' at line {i}, column {j + 1}"
                    bracket_stack.pop()
                elif char == ']':
                    if not bracket_stack or bracket_stack[-1][0] != '[':
                        return False, i, f"Unexpected ']' at line {i}, column {j + 1}"
                    bracket_stack.pop()

        if in_string:
            return False, i, f"Unclosed string at line {i}"

    if bracket_stack:
        return False, bracket_stack[-1][1], f"Unclosed {bracket_stack[-1][0]} at line {bracket_stack[-1][1]}"

    return True, 0, "Valid JSON"


data = {
    "name": "John",
    "age": 30,
    "city": "New York",
    "hobbies": ["reading", "gaming"],
    "active": True,
    "score": None
}

json_str = serialize(data, indent=2)
print(json_str)
print("\n", deserialize(json_str))
print("\n", validate_json(json_str)[0])
