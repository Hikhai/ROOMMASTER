"""
Minify CSS and JS files for production
"""
import os
import re

def minify_css(css_content):
    """Simple CSS minification"""
    # Remove comments
    css_content = re.sub(r'/\*.*?\*/', '', css_content, flags=re.DOTALL)
    
    # Remove whitespace
    css_content = re.sub(r'\s+', ' ', css_content)
    
    # Remove spaces around special characters
    css_content = re.sub(r'\s*([{}:;,>+~])\s*', r'\1', css_content)
    
    # Remove trailing semicolons
    css_content = re.sub(r';}', '}', css_content)
    
    return css_content.strip()


def minify_js(js_content):
    """Simple JS minification"""
    # Remove single-line comments (but keep URLs)
    js_content = re.sub(r'(?<!:)//.*$', '', js_content, flags=re.MULTILINE)
    
    # Remove multi-line comments
    js_content = re.sub(r'/\*.*?\*/', '', js_content, flags=re.DOTALL)
    
    # Remove excessive whitespace
    js_content = re.sub(r'\s+', ' ', js_content)
    
    # Remove spaces around operators
    js_content = re.sub(r'\s*([{}()\[\];,=<>+\-*/!&|?:])\s*', r'\1', js_content)
    
    return js_content.strip()


def process_files():
    """Process all CSS and JS files"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    static_dir = os.path.join(base_dir, 'app', 'static')
    
    print("🎨 Minifying static files...")
    print("=" * 60)
    
    # Process CSS files
    css_dir = os.path.join(static_dir, 'css')
    for filename in os.listdir(css_dir):
        if filename.endswith('.css') and not filename.endswith('.min.css'):
            filepath = os.path.join(css_dir, filename)
            
            # Read original file
            with open(filepath, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            original_size = len(original_content)
            
            # Minify
            minified_content = minify_css(original_content)
            minified_size = len(minified_content)
            
            # Save minified version
            min_filename = filename.replace('.css', '.min.css')
            min_filepath = os.path.join(css_dir, min_filename)
            
            with open(min_filepath, 'w', encoding='utf-8') as f:
                f.write(minified_content)
            
            reduction = ((original_size - minified_size) / original_size) * 100
            
            print(f"✅ {filename}")
            print(f"   Original: {original_size:,} bytes")
            print(f"   Minified: {minified_size:,} bytes")
            print(f"   Saved: {reduction:.1f}%")
            print()
    
    # Process JS files
    js_dir = os.path.join(static_dir, 'js')
    for filename in os.listdir(js_dir):
        if filename.endswith('.js') and not filename.endswith('.min.js'):
            filepath = os.path.join(js_dir, filename)
            
            # Read original file
            with open(filepath, 'r', encoding='utf-8') as f:
                original_content = f.read()
            
            original_size = len(original_content)
            
            # Minify
            minified_content = minify_js(original_content)
            minified_size = len(minified_content)
            
            # Save minified version
            min_filename = filename.replace('.js', '.min.js')
            min_filepath = os.path.join(js_dir, min_filename)
            
            with open(min_filepath, 'w', encoding='utf-8') as f:
                f.write(minified_content)
            
            reduction = ((original_size - minified_size) / original_size) * 100
            
            print(f"✅ {filename}")
            print(f"   Original: {original_size:,} bytes")
            print(f"   Minified: {minified_size:,} bytes")
            print(f"   Saved: {reduction:.1f}%")
            print()
    
    print("=" * 60)
    print("✅ Minification completed!")
    print("\n💡 Note: Update your templates to use .min.css and .min.js in production")


if __name__ == '__main__':
    process_files()
