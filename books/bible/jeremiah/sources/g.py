import re,sys
f=sys.argv[1]; pat=sys.argv[2]; w=int(sys.argv[3]); n=int(sys.argv[4]) if len(sys.argv)>4 else 1
t=re.sub(r'\s+',' ',open(f,errors='ignore').read())
last=-10**9;c=0
for m in re.finditer(pat,t,re.I):
    if m.start()<last+w: continue
    print('>>',t[max(0,m.start()-100):m.start()+w]);print(); last=m.start(); c+=1
    if c>=n: break
