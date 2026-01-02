#!/usr/bin/env python3
"""
SPEC Engine Compatibility Checker
Version: 2.0
Purpose: Scan existing SPECs and identify v1.x specs that could benefit from v2.0 features

Usage:
    python compatibility_checker.py [path_to_specs_directory]
    
    If no path provided, scans ../SPECs/ relative to this script
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Tuple
import re

def find_spec_directories(base_path: Path) -> List[Path]:
    """Find all directories containing SPEC files"""
    spec_dirs = []
    
    # Look for directories with spec_*.md files
    for root, dirs, files in os.walk(base_path):
        spec_files = [f for f in files if f.startswith('spec_') and f.endswith('.md')]
        if spec_files:
            spec_dirs.append(Path(root))
    
    return spec_dirs

def check_spec_version(spec_dir: Path) -> Dict[str, any]:
    """Determine SPEC version and feature availability"""
    result = {
        'path': str(spec_dir),
        'version': 'unknown',
        'has_notepad_config': False,
        'has_education_config': False,
        'has_notepad_file': False,
        'is_toolspec': False,
        'missing_features': [],
        'recommendations': []
    }
    
    # Check if this is a TOOLSPEC
    if '_TOOLSPECs' in str(spec_dir):
        result['is_toolspec'] = True
    
    # Find parameters file
    params_file = None
    for file in spec_dir.glob('parameters_*.toml'):
        params_file = file
        break
    
    if not params_file:
        result['version'] = 'invalid'
        result['missing_features'].append('No parameters.toml file found')
        return result
    
    # Read parameters file
    try:
        with open(params_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Check for v2.0 features
            if '[knowledge_capture]' in content:
                result['has_notepad_config'] = True
            else:
                result['missing_features'].append('knowledge_capture')
                result['recommendations'].append('Add [knowledge_capture] section for automatic notepad generation')
            
            if '[education]' in content:
                result['has_education_config'] = True
            else:
                result['missing_features'].append('education_mode')
                result['recommendations'].append('Add [education] section to enable learning-focused execution')
            
            # Determine version based on features
            if result['has_notepad_config'] and result['has_education_config']:
                result['version'] = 'v2.0'
            elif '[error_propagation]' in content and 'propagation_strategy' in content:
                result['version'] = 'v1.3'
            elif 'default_mode = "dynamic"' in content:
                result['version'] = 'v1.2-1.3'
            else:
                result['version'] = 'v1.0-1.1'
                
    except Exception as e:
        result['version'] = 'error'
        result['missing_features'].append(f'Error reading parameters file: {str(e)}')
    
    # Check for existing notepad file
    notepad_files = list(spec_dir.glob('notepad_*.md'))
    if notepad_files:
        result['has_notepad_file'] = True
    
    return result

def generate_report(results: List[Dict]) -> str:
    """Generate human-readable compatibility report"""
    report = []
    report.append("=" * 80)
    report.append("SPEC Engine Compatibility Report (v1.x -> v2.0)")
    report.append("=" * 80)
    report.append("")
    
    # Summary statistics
    total = len(results)
    v2_count = sum(1 for r in results if r['version'] == 'v2.0')
    v1_count = total - v2_count
    needs_upgrade = sum(1 for r in results if r['missing_features'])
    
    report.append("SUMMARY")
    report.append("-" * 80)
    report.append(f"Total SPECs Found: {total}")
    report.append(f"  - v2.0 SPECs: {v2_count}")
    report.append(f"  - v1.x SPECs: {v1_count}")
    report.append(f"  - SPECs that could benefit from upgrade: {needs_upgrade}")
    report.append("")
    
    # Categorize by version
    v2_specs = [r for r in results if r['version'] == 'v2.0']
    v1_specs = [r for r in results if r['version'].startswith('v1') or r['version'] == 'unknown']
    
    if v2_specs:
        report.append("v2.0 SPECS (Up to Date)")
        report.append("-" * 80)
        for spec in v2_specs:
            report.append(f"[OK] {spec['path']}")
            if spec['has_notepad_file']:
                report.append(f"   [NOTE] Notepad exists")
        report.append("")
    
    if v1_specs:
        report.append("v1.x SPECS (Backward Compatible, Upgrade Optional)")
        report.append("-" * 80)
        for spec in v1_specs:
            report.append(f"[v1] {spec['path']}")
            report.append(f"   Version: {spec['version']}")
            if spec['missing_features']:
                report.append(f"   Missing: {', '.join(spec['missing_features'])}")
            if spec['recommendations']:
                for rec in spec['recommendations']:
                    report.append(f"   [Tip] {rec}")
            report.append("")
    
    # Upgrade suggestions
    if needs_upgrade > 0:
        report.append("UPGRADE RECOMMENDATIONS")
        report.append("-" * 80)
        report.append("v1.x SPECs are fully functional. Upgrade is OPTIONAL.")
        report.append("")
        report.append("Benefits of upgrading to v2.0:")
        report.append("  - Knowledge capture via notepad.md")
        report.append("  - Education mode for learning-focused execution")
        report.append("  - Access to troubleshooting TOOLSPECs")
        report.append("")
        report.append("To upgrade a SPEC:")
        report.append("  1. See MIGRATION_v1_to_v2.md for manual upgrade steps")
        report.append("  2. Or regenerate SPEC using Commander (preserves goal/tasks)")
        report.append("  3. Or leave as-is (still works perfectly)")
        report.append("")
    
    report.append("=" * 80)
    report.append("All v1.x SPECs remain fully functional in v2.0. Migration is optional.")
    report.append("=" * 80)
    
    return "\n".join(report)

def main():
    """Main compatibility checker execution"""
    
    # Determine base path
    if len(sys.argv) > 1:
        base_path = Path(sys.argv[1])
    else:
        # Default to ../SPECs/ relative to this script
        script_dir = Path(__file__).parent
        base_path = script_dir.parent.parent / 'SPECs'
    
    if not base_path.exists():
        print(f"Error: Path not found: {base_path}")
        print(f"Usage: python {Path(__file__).name} [path_to_specs_directory]")
        sys.exit(1)
    
    print(f"Scanning for SPECs in: {base_path}")
    print("")
    
    # Find all SPEC directories
    spec_dirs = find_spec_directories(base_path)
    
    if not spec_dirs:
        print("No SPEC directories found.")
        print("Looking for directories containing spec_*.md files")
        sys.exit(0)
    
    print(f"Found {len(spec_dirs)} SPEC(s). Analyzing...")
    print("")
    
    # Check each SPEC
    results = []
    for spec_dir in spec_dirs:
        result = check_spec_version(spec_dir)
        results.append(result)
    
    # Generate and print report
    report = generate_report(results)
    print(report)
    
    # Save report to file
    report_file = Path(__file__).parent / 'compatibility_report.txt'
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print("")
    print(f"Report saved to: {report_file}")
    print("")
    print("Next steps:")
    print("  • Review MIGRATION_v1_to_v2.md for upgrade guidance")
    print("  • Try new TOOLSPECs in _TOOLSPECs/ directory")
    print("  • Read GETTING_STARTED_v2.md for v2.0 features")

if __name__ == '__main__':
    main()
