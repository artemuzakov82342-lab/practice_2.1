def escape(s):
    for ch, esc in [('&', '&amp;'), ('<', '&lt;'), ('>', '&gt;'), ('"', '&quot;'), ("'", '&apos;')]:
        s = s.replace(ch, esc)
    return s


def unescape(s):
    for esc, ch in [('&amp;', '&'), ('&lt;', '<'), ('&gt;', '>'), ('&quot;', '"'), ('&apos;', "'")]:
        s = s.replace(esc, ch)
    return s


def serialize(obj, tag='root', indent=0):
    space = '  ' * indent
    if isinstance(obj, dict):
        res = f"{space}<{tag}>\n"
        for k, v in obj.items():
            res += serialize(v, k, indent + 1)
        res += f"{space}</{tag}>\n"
        return res
    elif isinstance(obj, list):
        res = f"{space}<{tag}>\n"
        for item in obj:
            res += serialize(item, 'item', indent + 1)
        res += f"{space}</{tag}>\n"
        return res
    else:
        return f"{space}<{tag}>{escape(str(obj))}</{tag}>\n"


def deserialize(xml):
    lines = [l.strip() for l in xml.split('\n') if l.strip()]
    stack = []
    root = None

    for line in lines:
        if line.startswith('<?xml'):
            continue
        if line.startswith('</'):
            stack.pop()
        elif line.startswith('<'):
            tag = line[1:line.find('>')]
            if line.endswith('/>'):
                val = None
            else:
                content = line[line.find('>') + 1:line.rfind('<')]
                val = unescape(content) if content else {}
            node = {tag: val}

            if stack:
                parent = stack[-1]
                ptag = list(parent.keys())[0]
                if isinstance(parent[ptag], list):
                    parent[ptag].append(node)
                elif parent[ptag]:
                    parent[ptag] = [parent[ptag], node]
                else:
                    parent[ptag] = node
            else:
                root = node
            if val == {} and not line.endswith('/>'):
                stack.append(node)
    return root


def validate(xml):
    stack = []
    lines = xml.split('\n')
    for i, line in enumerate(lines, 1):
        if '<?xml' in line:
            continue
        if '<' in line:
            tags = []
            pos = 0
            while True:
                start = line.find('<', pos)
                if start == -1:
                    break
                end = line.find('>', start)
                if end == -1:
                    return False, i, f"Unclosed tag at line {i}"
                tag = line[start + 1:end]
                if tag.startswith('/'):
                    if not stack or stack[-1] != tag[1:]:
                        return False, i, f"Closing tag </{tag[1:]}> doesn't match"
                    stack.pop()
                elif not tag.endswith('/'):
                    stack.append(tag)
                pos = end + 1
    if stack:
        return False, 0, f"Unclosed tags: {stack}"
    return True, 0, "Valid XML"


# Тест
data = {"book": {"title": "Война и мир", "author": "Толстой", "year": 1869}}

xml = serialize(data)
print("XML:")
print(xml)

parsed = deserialize(xml)
print("\nParsed:", parsed)

valid, line, msg = validate(xml)
print(f"\nValid: {valid} - {msg}")