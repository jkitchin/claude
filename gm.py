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

with open('gm.jsonl', 'a') as f:
    for g in [0, 0.5, 1.0]:
        for i in range(5):        
            d = {'G': g, 'result': gm(g), 'time': time.time()}
            f.write(json.dumps(d) + '\n')


t, g, out = [], [], []            
import matplotlib.pyplot as plt
with open('gm.jsonl', 'r') as f:
    for line in f:
        t += [line['time']]
        g += [line['G']]
        out += [line['result']]

plt.plot(g, out)
plt.xlabel('g')
plt.ylabel('out')
plt.savefig('out-v-g.png')
plt.close()

plt.figure()
plt.plot(t, out)
plt.xlabel('time')
plt.ylabel('out')
plt.savefig('out-v-time.png')
