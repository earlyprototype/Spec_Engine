import yaml

# Read the YAML file
try:
    with open('docker-mcp-catalog.yaml', 'r', encoding='utf-8', errors='ignore') as f:
        data = yaml.safe_load(f)
except Exception as e:
    print(f"Error reading file: {e}")
    exit(1)

# Extract MCP count and categories
mcps = data.get('registry', {})
print(f'Total MCPs: {len(mcps)}')
print('=' * 60)

# Count by category
categories = {}
for name, mcp in mcps.items():
    cat = mcp.get('metadata', {}).get('category', 'uncategorized')
    if cat not in categories:
        categories[cat] = []
    categories[cat].append({
        'name': name,
        'title': mcp.get('title', name),
        'pulls': mcp.get('metadata', {}).get('pulls', 0),
        'stars': mcp.get('metadata', {}).get('githubStars', 0),
        'tools_count': len(mcp.get('tools', [])),
        'description': mcp.get('description', '')[:100]
    })

# Sort categories by MCP count
print('\nCategories (sorted by count):')
print('=' * 60)
for cat in sorted(categories.keys(), key=lambda x: len(categories[x]), reverse=True):
    print(f'{cat:25s}: {len(categories[cat]):3d} MCPs')

print('\n' + '=' * 60)
print('Top 10 MCPs by popularity (pulls):')
print('=' * 60)

# Flatten all MCPs and sort by pulls
all_mcps = []
for cat, mcp_list in categories.items():
    for mcp in mcp_list:
        mcp['category'] = cat
        all_mcps.append(mcp)

all_mcps_sorted = sorted(all_mcps, key=lambda x: x['pulls'], reverse=True)

for i, mcp in enumerate(all_mcps_sorted[:10], 1):
    print(f"{i:2d}. {mcp['title']:30s} - {mcp['pulls']:,} pulls, {mcp['tools_count']:2d} tools ({mcp['category']})")

print('\n' + '=' * 60)
print('Writing detailed catalog...')

# Write detailed output
with open('mcp_catalog_analysis.txt', 'w', encoding='utf-8') as f:
    for cat in sorted(categories.keys()):
        f.write(f'\n\n### {cat.upper()} ({len(categories[cat])} MCPs)\n')
        f.write('=' * 80 + '\n')
        
        # Sort by pulls within category
        sorted_mcps = sorted(categories[cat], key=lambda x: x['pulls'], reverse=True)
        
        for mcp in sorted_mcps:
            f.write(f"\n{mcp['title']}\n")
            f.write(f"  Name: {mcp['name']}\n")
            f.write(f"  Tools: {mcp['tools_count']}\n")
            f.write(f"  Pulls: {mcp['pulls']:,}\n")
            f.write(f"  Stars: {mcp['stars']:,}\n")
            f.write(f"  Description: {mcp['description']}\n")

print('Done! Check mcp_catalog_analysis.txt for full details')



