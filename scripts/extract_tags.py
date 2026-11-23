import re

tags = set()
for f in ['CHAPTER_01_CONTENT.md', 'CHAPTER_02_CONTENT.md', 'CHAPTER_03_CONTENT.md']:
    with open(f, 'r', encoding='utf-8') as fp:
        t = fp.read()
    found = re.findall(r'\*\*Tags:\*\*\s*(.*)', t)
    for tag_str in found:
        # tag_str may be `tag1`, `tag2`
        extracted = re.findall(r'`([^`]+)`', tag_str)
        for e in extracted:
            tags.add(e.strip())

print(f"Total unique tags: {len(tags)}")
for tag in sorted(list(tags)):
    print(tag)
