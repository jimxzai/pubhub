import json,sys,re,os
def conv(t):
    t=t.replace('裡','裏').replace('　神','神').replace('─','——')
    t=t.replace('（作神執事的：有古卷是與神同工的）','').replace('（有古卷作：與神同工的）','')
    return t
# Base text: the original 和合本 as printed by ai-eden.com (the house standard)
# and cnbible.com's "繁體中文和合本"; the two agree on all 89 verses including
# punctuation (cuv-verified.json). bible.fhl.net's `unv` is NOT used for this
# letter: it silently mixes in 現代標點和合本 readings (地/嗎/警醒/消滅, and
# 4:14 他們, 5:23 我們主) -- found in the 2026-10-02 second-source audit.
def cuv(ch,a,b):
    d=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'cuv-verified.json')))
    return {int(k.split(':')[1]):conv(t) for k,t in d.items() if int(k.split(':')[0])==ch and a<=int(k.split(':')[1])<=b}
def nasb(ch,a,b):
    d=json.load(open('nasb1995.json'))[str(ch)]
    return {int(k):v for k,v in d.items() if a<=int(k)<=b}
if __name__=='__main__':
    ch,a,b=map(int,sys.argv[1:4])
    print(''.join(f'^{k}^{v}' for k,v in cuv(ch,a,b).items()))
    print()
    print(' '.join(f'^{k}^{v}' for k,v in nasb(ch,a,b).items()))
