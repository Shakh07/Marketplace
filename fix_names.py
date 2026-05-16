import os
import re

directories = ['templates', 'static/css', 'apps']

replacements = [
    (r'\bonyx-', 'nexus-'),
    (r'\bonyx\.', 'nexus.'),
    (r'\bOnyx\b', 'NEXUS'),
    (r'\bonyx\b', 'nexus'),
    (r'\bONYX\b', 'NEXUS')
]

for d in directories:
    for root, dirs, files in os.walk(d):
        if 'migrations' in root or '__pycache__' in root:
            continue
        for f in files:
            if f.endswith('.html') or f.endswith('.css') or f.endswith('.py') or f.endswith('.js'):
                path = os.path.join(root, f)
                with open(path, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                new_content = content
                for pattern, repl in replacements:
                    new_content = re.sub(pattern, repl, new_content)
                
                if content != new_content:
                    with open(path, 'w', encoding='utf-8') as file:
                        file.write(new_content)
                    print(f'Updated: {path}')
print('Done.')
