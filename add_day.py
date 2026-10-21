#!/usr/bin/env python3
"""Japanese daily set. Usage: python3 add_day.py new.json [YYYY-MM-DD]  (date defaults to Taipei today; extra sets -> b, c...)
`python3 add_day.py --used` lists used words.  Read curriculum.json first and follow it.
GUIDANCE: learner = total beginner (zh-Hant). Follow curriculum.json stages in order:
 hiragana rows -> katakana rows -> N5 -> N4 -> N3. Introduce ~1 new kana row every 3-4 days (new row <=4 of 10 q),
 rest reviews unlocked rows. After adding a row, update curriculum.json unlocked_kana_rows/previewing.
 Kana words may repeat across days (review); only vocab/grammar/reading `word` must be unique (repeat check skipped for kana/romaji/listen).
Types: kana(prompt kana->romaji options), romaji(prompt romaji->kana options), listen(prompt "", audio=kana/word, kana options),
 meaning, grammar(Japanese sentence with ＿, audio=full sentence), reading(short passage in prompt).
Fields: word,type,prompt,options[4],answer 0-3,example(Japanese),reading(romaji/furigana),exampleZh,note(optional zh tip),audio(optional).
All explanations in Traditional Chinese."""
import json,sys,os,datetime
D=os.path.join(os.path.dirname(os.path.abspath(__file__)),'questions')
m=json.load(open(f'{D}/manifest.json'))
used={q['word'].lower() for d in m['days'] for q in json.load(open(f'{D}/{d}.json'))['questions']}
if sys.argv[1]=='--used': print('\n'.join(sorted(used))); sys.exit()
date=sys.argv[2] if len(sys.argv)>2 else (datetime.datetime.utcnow()+datetime.timedelta(hours=8)).date().isoformat()
if os.path.exists(f'{D}/{date}.json'):  # extra set same day -> 2026-10-21b, c...
    for c in 'bcdefgh':
        if not os.path.exists(f'{D}/{date}{c}.json'): date+=c;break
qs=json.load(open(sys.argv[1]))['questions']
assert len(qs)==10,'need 10'
for q in qs:
    assert len(q['options'])==4 and 0<=q['answer']<=3, q
    assert q['type'] in('kana','romaji','listen') or q['word'].lower() not in used, 'repeat: '+q['word']
    q.setdefault('id',q['word'])
json.dump({'date':date,'questions':qs},open(f'{D}/{date}.json','w'),ensure_ascii=False,indent=1)
if date not in m['days']: m['days'].append(date); m['days'].sort()
json.dump(m,open(f'{D}/manifest.json','w'))
print('added',date)
