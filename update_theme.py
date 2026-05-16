import os
import re

base_dir = r"c:\Users\Shohruh\OneDrive\Desktop\skill"

def replace_in_file(filepath, pattern_replacements):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content = content
        for pattern, replacement in pattern_replacements:
            new_content = re.sub(pattern, replacement, new_content)
            
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Updated {os.path.basename(filepath)}")
    except Exception as e:
        print(f"Error on {filepath}: {e}")

# 1. Update CSS
css_path = os.path.join(base_dir, "static", "css", "style.css")
css_replacements = [
    (r"--bg-primary: #ffffff;", r"--bg-primary: #000000;"),
    (r"--bg-secondary: #f5f5f7;", r"--bg-secondary: #0a0a0c;"),
    (r"--bg-tertiary: #e8e8ed;", r"--bg-tertiary: #141417;"),
    (r"--text-primary: #1d1d1f;", r"--text-primary: #e0e0e0;"),
    (r"--text-secondary: #86868b;", r"--text-secondary: #8a8a93;"),
    (r"--text-inverse: #ffffff;", r"--text-inverse: #000000;"),
    (r"--brand-blue: #0071e3;", r"--brand-blue: #00f0ff;"),
    (r"--brand-blue-hover: #0077ed;", r"--brand-blue-hover: #00d0e0;"),
    (r"--brand-black: #000000;", r"--brand-black: #ffffff;"),
    (r"--border-color: #d2d2d7;", r"--border-color: #1a1a24;"),
    (r"--nav-bg: rgba\(255, 255, 255, 0.72\);", r"--nav-bg: rgba(0, 0, 0, 0.85);"),
    
    (r"--font-stack: 'Inter',", r"--font-stack: 'Orbitron', 'Inter',"),
    
    (r"background-color: rgba\(255, 255, 255, 0.85\);", r"background-color: rgba(0, 0, 0, 0.85);"),
    (r"border-bottom: 1px solid rgba\(0, 0, 0, 0.05\);", r"border-bottom: 1px solid rgba(0, 240, 255, 0.3);box-shadow: 0 4px 15px rgba(0,240,255,0.1);"),
    
    (r"border-radius: var\(--radius-pill\);", r"border-radius: 4px; border: 1px solid var(--brand-blue); position: relative; overflow: hidden;"),
    (r"border-radius: var\(--radius-xl\);", r"border-radius: 8px; border: 1px solid var(--border-color); box-shadow: 0 0 10px rgba(0, 240, 255, 0.05);"),
    (r"border-radius: var\(--radius-lg\);", r"border-radius: 8px;"),
    (r"border-radius: var\(--radius-md\);", r"border-radius: 6px;"),
    (r"border-radius: var\(--radius-sm\);", r"border-radius: 4px;"),
    
    (r"background-color: #f5f5f7;", r"background-color: var(--bg-secondary);"),
    (r"background-color: #fbfbfd;", r"background-color: var(--bg-secondary);"),
    (r"background-color: #fff;", r"background-color: var(--bg-primary);"),
    
    (r"color: rgba\(0, 0, 0, 0.8\);", r"color: rgba(255, 255, 255, 0.8);"),
    (r"color: #1d1d1f;", r"color: #e0e0e0;"),
    (r"color: #86868b;", r"color: #8a8a93;"),
    
    # Specific ROG touches
    (r"\.nav-links a:hover \{", r".nav-links a:hover {\n    color: var(--brand-blue);\n    text-shadow: 0 0 8px rgba(0,240,255,0.8);"),
    (r"\.nav-brand \{", r".nav-brand {\n    text-shadow: 0 0 10px rgba(0,240,255,0.5);\n    font-family: 'Orbitron', sans-serif;\n    font-weight: 700;\n    text-transform: uppercase;\n    letter-spacing: 2px;"),
    
    (r"box-shadow: 0 24px 48px rgba\(0,0,0,0.06\);", r"box-shadow: 0 10px 30px rgba(0, 240, 255, 0.15), 0 0 0 1px rgba(0,240,255,0.3);"),
]

replace_in_file(css_path, css_replacements)

# 2. Update base.html
base_html_path = os.path.join(base_dir, "templates", "base.html")
base_html_replacements = [
    (r"Onyx", r"NEXUS"),
    (r"onyx", r"nexus"),
    (r"font-family: 'Inter'", r"font-family: 'Orbitron'"),
    (r"family=Inter:wght@300;400;500;600;700", r"family=Inter:wght@300;400;500;600;700&family=Orbitron:wght@400;500;700;900"),
    (r"background: #ffffff;", r"background: #000000;"),
    (r"border-top-color: #1d1d1f;", r"border-top-color: #00f0ff;"),
    (r"rgba\(255,255,255,0.92\)", r"rgba(0,0,0,0.9)"),
    (r"rgba\(29,29,31,0.95\)", r"rgba(10,10,12,0.95); border: 1px solid rgba(0,240,255,0.2);"),
    (r"background:#1d1d1f;", r"background:#00f0ff; color:#000; box-shadow: 0 0 10px rgba(0,240,255,0.5);"),
    (r"background:linear-gradient\(135deg,#1d1d1f,#424245\);", r"background:linear-gradient(135deg,#005c66,#00f0ff);"),
    (r"background:rgba\(255,255,255,0.12\)", r"background:rgba(0,240,255,0.05)"),
    (r"border:1px solid rgba\(255,255,255,0.25\)", r"border:1px solid rgba(0,240,255,0.3); box-shadow: 0 0 15px rgba(0,240,255,0.15)"),
]

replace_in_file(base_html_path, base_html_replacements)

# 3. Update home.html
home_html_path = os.path.join(base_dir, "templates", "home.html")
home_html_replacements = [
    (r"Onyx", r"NEXUS"),
    (r"onyx", r"nexus"),
    (r"color: #1d1d1f;", r"color: #ffffff;"),
    (r"background: #f5f5f7;", r"background: #000000;"),
    (r"background: #1d1d1f;", r"background: #0a0a0c;"),
    (r"color: #0071e3;", r"color: #00f0ff;"),
    (r"background: white;", r"background: #0a0a0c;"),
    (r"color: white;", r"color: #ffffff;"),
    (r"rgba\(0, 0, 0, 0.06\)", r"rgba(0, 240, 255, 0.1)"),
    
    # Hero gradient adjustment
    (r"linear-gradient\(135deg, \{% cycle '#1d1d1f' '#0071e3' '#34c759' '#ff9500' '#af52de' '#ff375f' '#007aff' '#5ac8fa' %\} 0%, \{% cycle '#434345' '#5bc0ff' '#8eea9b' '#ffcc00' '#d483f2' '#ff6b6b' '#5bc0ff' '#0071e3' %\} 100%\)", 
     r"linear-gradient(135deg, rgba(0,240,255,0.2) 0%, rgba(0,0,0,0.9) 100%)"),
    
    (r"border-top: 1px solid rgba\(0, 0, 0, 0.06\);", r"border-top: 1px solid rgba(0, 240, 255, 0.2);"),
    (r"border-bottom: 1px solid rgba\(0, 0, 0, 0.06\);", r"border-bottom: 1px solid rgba(0, 240, 255, 0.2);"),
]

replace_in_file(home_html_path, home_html_replacements)

# Iterate through other templates for Onyx->NEXUS replacements
templates_dir = os.path.join(base_dir, "templates")
for root, dirs, files in os.walk(templates_dir):
    for filename in files:
        if filename.endswith(".html") and filename not in ["base.html", "home.html"]:
            filepath = os.path.join(root, filename)
            replace_in_file(filepath, [(r"Onyx", r"NEXUS"), (r"onyx", r"nexus")])

print("Theme update script finished.")
