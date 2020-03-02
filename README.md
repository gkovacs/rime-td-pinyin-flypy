# rime-td-pinyin-flypy

## About

This is a layout for typing in Shuangpin (双拼) with the Flypy (小鹤双拼) layout. Tones can be entered as follows:

* Tone 1: `;`
* Tone 2: `/`
* Tone 3: `,`
* Tone 4: `.`

## Installing

First ensure you have plum installed. For macOS this would be:

```bash
cd ~/Library/Rime
wget https://git.io/rime-install
```

Then install `gkovacs/rime-td-pinyin-flypy` using plum:

```bash
bash rime-install gkovacs/rime-td-pinyin-flypy
```

Finally edit `default.custom.yaml` and add `td_pinyin_flypy` to the schema list:

```bash
patch:
  schema_list:
    - schema: td_pinyin_flypy
```

Now reload RIME and it should appear under your layouts.
