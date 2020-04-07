import opencc

char_to_cangjie = {}
seen_start = False
for line in open('cangjie5.dict.yaml'):
  line = line.strip()
  if not seen_start:
    if line == '...':
      seen_start = True
    continue
  if line == '':
    continue
  parts = line.split('\t')
  char = parts[0]
  #char_simp = opencc.convert(word, config='t2s.json')
  char_to_cangjie[char] = []
  for cangjie_code in parts[1:]:
    if "'" in cangjie_code:
      continue
    char_to_cangjie[char].append(cangjie_code)

def cangjie_letter_to_hanzi(letter):
  letters = 'abcdefghijklmnopqrstuvwxyz'
  hanzi   = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
  #hanzi   = '日月金木水火土竹戈十大中一弓人心手口尸廿山女田難卜重'
  #hanzi = "БбГДЖЗИЙЛлПФЦцЧчШшЩщЭэЮюЯя"
  #hanzi = 'ÀÁ'
  return hanzi[letters.index(letter)]
  #return '67ÀÁ'[letters.index(letter) % 4]
  #return '6789'[letters.index(letter) % 4]
  #return '6'
  #return ''

def pinyin_base(letters):
  return letters[0:len(letters)-1]

def pinyin_tone(letters):
  return letters[len(letters)-1:]

header_text = '''---
name: terra_pinyin.cangjie5
version: "2018.04.10"
sort: by_weight
use_preset_vocabulary: true
max_phrase_length: 7
min_phrase_weight: 100
...
'''

outfile = open('../terra_pinyin.cangjie5.dict.yaml', 'wt')
print(header_text, file=outfile)
num_lines = 0
seen_start = False
for line in open('../terra_pinyin.dict.yaml'):
  line = line.strip()
  if not seen_start:
    if line == '...':
      seen_start = True
    continue
  parts = line.split('\t')
  chars_orig = parts[0]
  chars = chars_orig.replace('·', '')
  readings = parts[1]
  readings_list = readings.split(' ')
  readings_list = [x for x in readings_list if x != '·']
  if len(chars) != len(readings_list):
    continue
  #chars_orig_simp = chars_orig
  #chars_simp = chars
  chars_orig_simp = opencc.convert(chars_orig, config='t2s.json')
  chars_simp = chars_orig_simp.replace('·', '')
  cangjie_list = [char_to_cangjie.get(x, [[None]])[0][0] for x in chars]
  cangjie_simp_list = [char_to_cangjie.get(x, [[None]])[0][0] for x in chars_simp]
  output_trad = True
  if None in cangjie_list:
    output_trad = False
  output_simp = True
  if None in cangjie_simp_list:
    output_simp = False
  if cangjie_simp_list == cangjie_list:
    output_simp = False
  if output_trad:
    readings_str = ' '.join([pinyin_base(pinyin)+pinyin_tone(pinyin)+cangjie_letter_to_hanzi(cangjie) for pinyin,cangjie in zip(readings_list, cangjie_list)])
    outline = chars_orig + '\t' + readings_str
    if len(parts) > 2:
      outline += '\t' + ('\t'.join(parts[2:]))
    print(outline, file=outfile)
  if output_simp:
    readings_str = ' '.join([pinyin_base(pinyin)+pinyin_tone(pinyin)+cangjie_letter_to_hanzi(cangjie) for pinyin,cangjie in zip(readings_list, cangjie_simp_list)])
    outline = chars_orig + '\t' + readings_str
    if len(parts) > 2:
      outline += '\t' + ('\t'.join(parts[2:]))
    print(outline, file=outfile)
outfile.close()