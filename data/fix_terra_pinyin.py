outf = open('./terra_pinyin_fixed.dict.yaml', 'wt')
at_start = True
for line in open('../terra_pinyin.dict.yaml'):
  if at_start:
    if line.strip() == '...':
      at_start = False
    outf.write(line)
    continue
  line_parts = line.split('\t')
  if len(line_parts) >= 2:
    pinyin = line_parts[1]
    pinyin_parts = pinyin.split(' ')
    pinyin_parts_fixed = []
    changed_pinyin = False
    for pinyin_part in pinyin_parts:
      if 'r5' == pinyin_part:
        pinyin_part = 'er5'
        changed_pinyin = True
      elif 'r5\n' == pinyin_part:
        pinyin_part = 'er5\n'
        changed_pinyin = True
      pinyin_parts_fixed.append(pinyin_part)
    if changed_pinyin:
      pinyin = ' '.join(pinyin_parts_fixed)
      line_parts[1] = pinyin
  outf.write('\t'.join(line_parts))
