"""Compile .po files to .mo without requiring GNU gettext."""
import os
import struct

def compile_po_to_mo(po_path, mo_path):
    """Simple .po to .mo compiler."""
    messages = []
    current_msgid = None
    current_msgstr = None
    in_msgid = False
    in_msgstr = False
    
    with open(po_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith('msgid "'):
                if current_msgid is not None:
                    if current_msgstr or current_msgid == '':
                        messages.append((current_msgid, current_msgstr or ''))
                content = line[7:-1]
                current_msgid = content
                current_msgstr = None
                in_msgid = True
                in_msgstr = False
            elif line.startswith('msgstr "'):
                content = line[8:-1]
                current_msgstr = content
                in_msgid = False
                in_msgstr = True
            elif line.startswith('"') and line.endswith('"'):
                content = line[1:-1]
                if in_msgid:
                    current_msgid += content
                elif in_msgstr:
                    current_msgstr = (current_msgstr or '') + content
            elif line == '' or line.startswith('#'):
                in_msgid = False
                in_msgstr = False
        
        # Don't forget the last entry
        if current_msgid is not None:
            if current_msgstr or current_msgid == '':
                messages.append((current_msgid, current_msgstr or ''))
    
    # Ensure metadata entry exists (empty msgid with charset)
    has_meta = any(msgid == '' for msgid, _ in messages)
    if not has_meta:
        meta = (
            'Content-Type: text/plain; charset=UTF-8\\n'
            'Content-Transfer-Encoding: 8bit\\n'
        )
        messages.insert(0, ('', meta))
    
    # Sort by msgid (required by .mo format) — empty string sorts first
    messages.sort(key=lambda x: x[0].encode('utf-8'))
    
    # Build .mo file
    n = len(messages)
    
    # Header
    keystart = 28 + 8 * n * 2
    valuestart = keystart
    
    # Calculate offsets
    keys = []
    values = []
    for msgid, msgstr in messages:
        # Unescape \n sequences
        keys.append(msgid.replace('\\n', '\n').encode('utf-8'))
        values.append(msgstr.replace('\\n', '\n').encode('utf-8'))
    
    # Key offsets
    key_start_offset = 28 + 8 * n * 2
    
    # First pass: compute key area
    ko = key_start_offset
    key_entries = []
    for k in keys:
        key_entries.append((len(k), ko))
        ko += len(k) + 1  # null terminator
    
    # Values start after all keys
    vo = ko
    val_entries = []
    for v in values:
        val_entries.append((len(v), vo))
        vo += len(v) + 1
    
    # Write the file
    output = []
    output.append(struct.pack('I', 0x950412de))
    output.append(struct.pack('I', 0))
    output.append(struct.pack('I', n))
    output.append(struct.pack('I', 28))
    output.append(struct.pack('I', 28 + 8 * n))
    output.append(struct.pack('I', 0))
    output.append(struct.pack('I', 0))
    
    for length, offset in key_entries:
        output.append(struct.pack('II', length, offset))
    
    for length, offset in val_entries:
        output.append(struct.pack('II', length, offset))
    
    for k in keys:
        output.append(k + b'\x00')
    
    for v in values:
        output.append(v + b'\x00')
    
    with open(mo_path, 'wb') as f:
        f.write(b''.join(output))


if __name__ == '__main__':
    base = os.path.dirname(os.path.abspath(__file__))
    locale_dir = os.path.join(base, 'locale')
    
    for lang in os.listdir(locale_dir):
        po_path = os.path.join(locale_dir, lang, 'LC_MESSAGES', 'django.po')
        mo_path = os.path.join(locale_dir, lang, 'LC_MESSAGES', 'django.mo')
        if os.path.isfile(po_path):
            compile_po_to_mo(po_path, mo_path)
            print(f'Compiled: {lang}/LC_MESSAGES/django.mo')
    
    print('Done!')
