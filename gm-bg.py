import time
import jsonlines
import requests
import json

CLAUDE_IP = 'https://claude-light.cheme.cmu.edu/api'

class GreenMachine1:
    """One input -> one output instrument.
    """    
    def __call__(self, G=0):
        """Run the instrument.
        G : int, setting for the green LED channel.
        Returns the 515nm channel intensity.
        """
        resp = requests.get(CLAUDE_IP, params={'R': 0, 'G': G, 'B': 0})
        data = resp.json()
        return data['out']['515nm']
    
gm = GreenMachine1()

with jsonlines.open('gm-bg.jsonl', 'a') as f:
    for g in [0, 0.5, 1.0]:
        for i in range(5):
            bg = gm(0)
            G = gm(g)
            d = {'G': g, 'result': G - bg, 'time': time.time()}
            f.write(d)


t, g, out = [], [], []            
import matplotlib.pyplot as plt

fig, p1 = plt.subplots(1, 3)
fig.set_figwidth(10)

day = 60 * 60 * 24 # seconds in a day

with jsonlines.open('gm-bg.jsonl', 'r') as f:
    for line in f:
        if line['G'] == 0.0:
            # time is in seconds. I convert to hours, 
            p1[0].plot((line['time'] % day) / 3600, line['result'], 'g.')            
        elif line['G'] == 0.5:
            p1[1].plot((line['time'] % day) / 3600, line['result'], 'g.')
        else:
            p1[2].plot((line['time'] % day) / 3600, line['result'], 'g.')

p1[0].set_title('G=0 vs time')
p1[1].set_title('G=0.5 vs time')
p1[2].set_title('G=1 vs time')
plt.tight_layout()
plt.savefig('out-w-bg-subtraction-v-time.png')
            
