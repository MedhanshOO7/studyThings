#!/usr/bin/env python3
"""
Verification script to ensure all HTML files have corresponding MD files.
"""

import os
import glob

def verify_conversion():
    # Find all HTML files
    html_files = glob.glob("/home/medhansh/Downloads/learncpp.com/LearnCPP_Offline/**/*.html", recursive=True)
    
    missing_md = []
    
    for html_file in html_files:
        md_file = html_file.replace('.html', '.md')
        if not os.path.exists(md_file):
            missing_md.append(html_file)
    
    print(f"Total HTML files: {len(html_files)}")
    print(f"Files without corresponding MD: {len(missing_md)}")
    
    if missing_md:
        print("\nMissing conversions:")
        for f in missing_md[:10]:  # Show first 10
            print(f"  - {f}")
        if len(missing_md) > 10:
            print(f"  ... and {len(missing_md) - 10} more")
    else:
        print("\n✅ All HTML files have corresponding MD files!")
    
    # Count MD files
    md_files = glob.glob("/home/medhansh/Downloads/learncpp.com/LearnCPP_Offline/**/*.md", recursive=True)
    print(f"Total MD files: {len(md_files)}")

if __name__ == "__main__":
    verify_conversion()