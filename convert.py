import os
import re

INPUT_DIR = "html"
OUTPUT_DIR = "src/output_jsx"

def remove_html_head_body(html):
    # Remove <html> and </html>
    html = re.sub(r'</?html[^>]*>', '', html, flags=re.IGNORECASE)
    # Remove <head>...</head>
    html = re.sub(r'<head[\s\S]*?</head>', '', html, flags=re.IGNORECASE)
    # Remove <body ...> but keep its content
    html = re.sub(r'<body[^>]*>', '', html, flags=re.IGNORECASE)
    html = re.sub(r'</body>', '', html, flags=re.IGNORECASE)
    return html

def remove_meta_link_script(html):
    # Remove <meta ...>, <link ...>, <script ...>...</script>
    html = re.sub(r'<meta[^>]*>', '', html, flags=re.IGNORECASE)
    html = re.sub(r'<link[^>]*>', '', html, flags=re.IGNORECASE)
    html = re.sub(r'<script[\s\S]*?</script>', '', html, flags=re.IGNORECASE)
    return html

def replace_deprecated_attrs(html):
    # Remove deprecated attributes
    html = re.sub(r'\s(bgcolor|background|link|vlink|alink|text)="[^"]*"', '', html, flags=re.IGNORECASE)
    return html

def font_to_span(html):
    # Replace <font ...> with <span style="...">
    def font_open(match):
        attrs = match.group(1)
        style = []
        size = re.search(r'size="([^"]+)"', attrs)
        color = re.search(r'color="([^"]+)"', attrs)
        if size:
            # crude mapping, can be improved
            size_map = {
                "1": "x-small", "2": "small", "3": "medium",
                "4": "large", "5": "x-large", "6": "xx-large", "7": "xxx-large"
            }
            style.append(f"font-size:{size_map.get(size.group(1), 'medium')}")
        if color:
            style.append(f"color:{color.group(1)}")
        style_str = ';'.join(style)
        return f'<span{" style=\"" + style_str + "\"" if style_str else ""}>'
    html = re.sub(r'<font([^>]*)>', font_open, html, flags=re.IGNORECASE)
    html = re.sub(r'</font>', '</span>', html, flags=re.IGNORECASE)
    return html

def align_to_style(html):
    # Replace align and valign with style
    def align_repl(match):
        tag, attrs = match.group(1), match.group(2)
        align = re.search(r'align="([^"]+)"', attrs)
        valign = re.search(r'valign="([^"]+)"', attrs)
        style = []
        if align:
            style.append(f'text-align:{align.group(1)}')
        if valign:
            style.append(f'vertical-align:{valign.group(1)}')
        attrs = re.sub(r'\s*align="[^"]+"', '', attrs)
        attrs = re.sub(r'\s*valign="[^"]+"', '', attrs)
        if style:
            if 'style="' in attrs:
                attrs = re.sub(r'style="([^"]*)"', lambda m: f'style="{m.group(1)};{";".join(style)}"', attrs)
            else:
                attrs += f' style="{";".join(style)}"'
        return f'<{tag}{attrs}>'
    html = re.sub(r'<(\w+)([^>]*)>', align_repl, html)
    return html

def fix_malformed_tags(html):
    # Fix duplicate closing tags like </b></b>
    html = re.sub(r'</b></b>', '</b>', html, flags=re.IGNORECASE)
    html = re.sub(r'</i></i>', '</i>', html, flags=re.IGNORECASE)
    html = re.sub(r'</span></span>', '</span>', html, flags=re.IGNORECASE)
    # Fix other common duplications
    html = re.sub(r'(</(b|i|span|strong|em)>)\1+', r'\1', html, flags=re.IGNORECASE)
    
    # Fix incorrect nesting order - most common patterns
    html = re.sub(r'</span></b>', '</b></span>', html, flags=re.IGNORECASE)
    html = re.sub(r'</span></i>', '</i></span>', html, flags=re.IGNORECASE)
    html = re.sub(r'</span></strong>', '</strong></span>', html, flags=re.IGNORECASE)
    html = re.sub(r'</span></em>', '</em></span>', html, flags=re.IGNORECASE)
    html = re.sub(r'</a></b>', '</b></a>', html, flags=re.IGNORECASE)
    html = re.sub(r'</a></i>', '</i></a>', html, flags=re.IGNORECASE)
    html = re.sub(r'</a></span>', '</span></a>', html, flags=re.IGNORECASE)
    
    # Fix unclosed tags - add missing closing tags before other closing tags
    html = re.sub(r'<span([^>]*)>([^<]*)</b>', r'<span\1>\2</span></b>', html, flags=re.IGNORECASE)
    html = re.sub(r'<span([^>]*)>([^<]*)</i>', r'<span\1>\2</span></i>', html, flags=re.IGNORECASE)
    html = re.sub(r'<span([^>]*)>([^<]*)</a>', r'<span\1>\2</span></a>', html, flags=re.IGNORECASE)
    html = re.sub(r'<span([^>]*)>([^<]*)</p>', r'<span\1>\2</span></p>', html, flags=re.IGNORECASE)
    html = re.sub(r'<span([^>]*)>([^<]*)</td>', r'<span\1>\2</span></td>', html, flags=re.IGNORECASE)
    html = re.sub(r'<span([^>]*)>([^<]*)</tr>', r'<span\1>\2</span></tr>', html, flags=re.IGNORECASE)
    
    # Fix unclosed <p> tags
    html = re.sub(r'<p([^>]*)>([^<]*)</td>', r'<p\1>\2</p></td>', html, flags=re.IGNORECASE)
    html = re.sub(r'<p([^>]*)>([^<]*)</tr>', r'<p\1>\2</p></tr>', html, flags=re.IGNORECASE)
    html = re.sub(r'<p([^>]*)>([^<]*)</div>', r'<p\1>\2</p></div>', html, flags=re.IGNORECASE)
    
    # Fix unclosed <li> tags
    html = re.sub(r'<li([^>]*)>([^<]*)</ul>', r'<li\1>\2</li></ul>', html, flags=re.IGNORECASE)
    html = re.sub(r'<li([^>]*)>([^<]*)</ol>', r'<li\1>\2</li></ol>', html, flags=re.IGNORECASE)
    html = re.sub(r'<li([^>]*)>([^<]*)<li', r'<li\1>\2</li><li', html, flags=re.IGNORECASE)
    
    # Fix unclosed <td> tags
    html = re.sub(r'<td([^>]*)>([^<]*)</tr>', r'<td\1>\2</td></tr>', html, flags=re.IGNORECASE)
    html = re.sub(r'<td([^>]*)>([^<]*)<td', r'<td\1>\2</td><td', html, flags=re.IGNORECASE)
    
    # Fix unclosed <tr> tags
    html = re.sub(r'<tr([^>]*)>([^<]*)</table>', r'<tr\1>\2</tr></table>', html, flags=re.IGNORECASE)
    html = re.sub(r'<tr([^>]*)>([^<]*)<tr', r'<tr\1>\2</tr><tr', html, flags=re.IGNORECASE)
    
    # Fix unclosed <a> tags - be more specific
    html = re.sub(r'<a([^>]*)>([^<]*)</span>', r'<a\1>\2</a></span>', html, flags=re.IGNORECASE)
    html = re.sub(r'<a([^>]*)>([^<]*)</b>', r'<a\1>\2</a></b>', html, flags=re.IGNORECASE)
    html = re.sub(r'<a([^>]*)>([^<]*)</i>', r'<a\1>\2</a></i>', html, flags=re.IGNORECASE)
    
    # Fix unclosed <b> tags
    html = re.sub(r'<b([^>]*)>([^<]*)</span>', r'<b\1>\2</b></span>', html, flags=re.IGNORECASE)
    html = re.sub(r'<b([^>]*)>([^<]*)</p>', r'<b\1>\2</b></p>', html, flags=re.IGNORECASE)
    html = re.sub(r'<b([^>]*)>([^<]*)</td>', r'<b\1>\2</b></td>', html, flags=re.IGNORECASE)
    
    # Fix unclosed <center> tags
    html = re.sub(r'<center([^>]*)>([^<]*)</td>', r'<center\1>\2</center></td>', html, flags=re.IGNORECASE)
    html = re.sub(r'<center([^>]*)>([^<]*)</tr>', r'<center\1>\2</center></tr>', html, flags=re.IGNORECASE)
    
    # Remove orphaned closing tags at the beginning of lines
    html = re.sub(r'^(\s*)</[^>]+>', r'\1', html, flags=re.MULTILINE)
    
    # Remove malformed anchor tags with quotes
    html = re.sub(r'<a([^>]*)"([^>]*)>', r'<a\1\2>', html, flags=re.IGNORECASE)
    html = re.sub(r'</a([^>]*)>', '</a>', html, flags=re.IGNORECASE)
    
    return html

def fix_malformed_attributes(html):
    # Skip processing href attributes entirely
    # Fix other common attributes with missing closing quotes
    html = re.sub(r'src="([^"]*?)>', r'src="\1">', html, flags=re.IGNORECASE)
    html = re.sub(r'alt="([^"]*?)>', r'alt="\1">', html, flags=re.IGNORECASE)
    html = re.sub(r'name="([^"]*?)>', r'name="\1">', html, flags=re.IGNORECASE)
    html = re.sub(r'id="([^"]*?)>', r'id="\1">', html, flags=re.IGNORECASE)
    html = re.sub(r'style="([^"]*?)>', r'style="\1">', html, flags=re.IGNORECASE)
    html = re.sub(r'className="([^"]*?)>', r'className="\1">', html, flags=re.IGNORECASE)
    html = re.sub(r'width="([^"]*?)>', r'width="\1">', html, flags=re.IGNORECASE)
    html = re.sub(r'height="([^"]*?)>', r'height="\1">', html, flags=re.IGNORECASE)
    html = re.sub(r'border="([^"]*?)>', r'border="\1">', html, flags=re.IGNORECASE)
    html = re.sub(r'cellpadding="([^"]*?)>', r'cellpadding="\1">', html, flags=re.IGNORECASE)
    html = re.sub(r'cellspacing="([^"]*?)>', r'cellspacing="\1">', html, flags=re.IGNORECASE)
    html = re.sub(r'coords="([^"]*?)>', r'coords="\1">', html, flags=re.IGNORECASE)
    html = re.sub(r'shape="([^"]*?)>', r'shape="\1">', html, flags=re.IGNORECASE)
    
    # Handle cases where attributes are malformed due to missing quotes and spaces
    html = re.sub(r'(\w+)="([^"]*?)\s>', r'\1="\2">', html, flags=re.IGNORECASE)
    
    # Fix cases where multiple malformed attributes exist in the same tag
    def fix_tag_attributes(match):
        tag_content = match.group(1)
        tag_content = re.sub(r'(\w+)="([^"]*?)(?=\s+\w+="|\s*>)', r'\1="\2"', tag_content)
        return f'<{tag_content}>'
    html = re.sub(r'<([^>]*?)>', fix_tag_attributes, html)
    
    return html

def skip_string_processing(html):
    # Use regex to skip processing anything inside quotes
    # Replace attributes with placeholders to avoid processing
    html = re.sub(r'(\w+)="[^"]*"', r'\1="SKIPPED"', html, flags=re.IGNORECASE)
    return html

def html_to_jsx(html):
    html = remove_html_head_body(html)
    html = remove_meta_link_script(html)
    html = replace_deprecated_attrs(html)
    html = font_to_span(html)
    html = align_to_style(html)
    html = skip_string_processing(html)  # Skip processing strings entirely
    html = fix_malformed_tags(html)
    # class -> className, for -> htmlFor
    html = re.sub(r'\bclass="', 'className="', html)
    html = re.sub(r'\bfor="', 'htmlFor="', html)
    
    # Self-close all void elements in one pass
    void_tags = ['area', 'img', 'input', 'br', 'hr', 'meta', 'link']
    for tag in void_tags:
        # Match opening tags that aren't already self-closed
        pattern = rf'<{tag}([^>]*?)(?<!/)>'
        def replace_func(match):
            attrs = match.group(1).rstrip()
            if attrs and not attrs.startswith(' '):
                attrs = ' ' + attrs
            return f'<{tag}{attrs} />'
        html = re.sub(pattern, replace_func, html, flags=re.IGNORECASE)
    
    # Remove comments
    html = re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)
    # Remove trailing </html> or </body> if any remain
    html = re.sub(r'</?(html|body)>', '', html, flags=re.IGNORECASE)
    return html

def to_component_name(filename):
    name = os.path.splitext(os.path.basename(filename))[0]
    return ''.join(word.capitalize() for word in re.split(r'[\W_]+', name))

def process_html_file(src_path, rel_path):
    with open(src_path, 'r', encoding='utf-8') as f:
        html = f.read()
    jsx = html_to_jsx(html)
    comp_name = to_component_name(rel_path)
    jsx_code = f"""import React from "react";

const {comp_name} = () => (
  <>
    {jsx}
  </>
);

export default {comp_name};
"""
    return jsx_code

def main():
    for root, _, files in os.walk(INPUT_DIR):
        for file in files:
            if file.endswith('.html'):
                print(f"Processing {file}...")
                src_path = os.path.join(root, file)
                rel_path = os.path.relpath(src_path, INPUT_DIR)
                out_path = os.path.join(OUTPUT_DIR, os.path.splitext(rel_path)[0] + ".jsx")
                os.makedirs(os.path.dirname(out_path), exist_ok=True)
                jsx_code = process_html_file(src_path, rel_path)
                with open(out_path, 'w', encoding='utf-8') as f:
                    f.write(jsx_code)
    print("Conversion complete.")

if __name__ == "__main__":
    main()