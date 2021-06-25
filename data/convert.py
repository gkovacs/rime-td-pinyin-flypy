import opencc

converter = opencc.OpenCC('t2s.json')

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
  if char not in char_to_cangjie:
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

def get_all_cangjie_for_each_char(char_list):
  output = []
  for x in char_list:
    cangjie_list = char_to_cangjie.get(x, [])
    first_chars = list(set([x[0] for x in cangjie_list]))
    if len(first_chars) > 1:
      if len([x for x in first_chars if x != 'x']) > 0:
        first_chars = [x for x in first_chars if x != 'x']
    output.append(first_chars)
  return output

def get_all_cangjie_combo_list(char_list):
  cangjie_for_each_char = get_all_cangjie_for_each_char(char_list)
  #print(cangjie_for_each_char)
  mlen = len(cangjie_for_each_char)
  def subr(start_idx=0):
    if start_idx >= mlen:
      return []
    if start_idx == mlen - 1:
      return [[x] for x in cangjie_for_each_char[start_idx]]
    else:
      output = []
      remainder = subr(start_idx + 1)
      for x in cangjie_for_each_char[start_idx]:
        for y in remainder:
          output.append([x] + y)
      return output
  return subr(0)

outfile = open('../terra_pinyin.cangjie5.dict.yaml', 'wt')
print(header_text, file=outfile)
num_lines = 0
seen_start = False
for line in open('./terra_pinyin_fixed.dict.yaml'):
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
  chars_orig_simp = converter.convert(chars_orig)
  chars_simp = chars_orig_simp.replace('·', '')
  cangjie_combo_list = get_all_cangjie_combo_list(chars)
  cangjie_simp_combo_list = get_all_cangjie_combo_list(chars_simp)
  for cangjie_list in cangjie_combo_list:
    if None in cangjie_list:
      continue
    readings_str = ' '.join([pinyin_base(pinyin)+pinyin_tone(pinyin)+cangjie_letter_to_hanzi(cangjie) for pinyin,cangjie in zip(readings_list, cangjie_list)])
    outline = chars_orig + '\t' + readings_str
    if len(parts) > 2:
      outline += '\t' + ('\t'.join(parts[2:]))
    print(outline, file=outfile)
  for cangjie_list in [x for x in cangjie_simp_combo_list if x not in cangjie_combo_list]:
    if None in cangjie_list:
      continue
    readings_str = ' '.join([pinyin_base(pinyin)+pinyin_tone(pinyin)+cangjie_letter_to_hanzi(cangjie) for pinyin,cangjie in zip(readings_list, cangjie_list)])
    outline = chars_orig + '\t' + readings_str
    if len(parts) > 2:
      outline += '\t' + ('\t'.join(parts[2:]))
    print(outline, file=outfile)
outfile.close()