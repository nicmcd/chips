#!/usr/bin/env python3

import matplotlib.pyplot as plt
import matplotlib.ticker as tkr
import matplotlib.lines as lns

import operator
import re
import random

chips = [
  {
    'company': 'Broadcom',
    'chip': 'Tomahawk',
    'year': 2015,
    'bandwidth': 6.4e12  # 32x100G
  },{
    'company': 'Broadom',
    'chip': 'Trident II',
    'year': 2012,
    'bandwidth': 2.56e12  # 32x40G
  },{
    'company': 'Broadcom',
    'chip': 'Trident I',
    'year': 2007,
    'bandwidth': 488e9  # 24x10G + 4x1G
  },{
    'company': 'Mellanox',
    'chip': 'SwitchIB',
    'year': 2015,
    'bandwidth': 7.2e12  # 36x100G
  },{
    'company': 'Mellanox',
    'chip': 'SwitchX-2',
    'year': 2012,
    'bandwidth': 4.032e12  # 36x56G
  },{
    'company': 'Mellanox',
    'chip': 'SwitchX',
    'year': 2011,
    'bandwidth': 4.032e12  # 36x56G
  },{
    'company': 'Mellanox',
    'chip': 'InfiniScale IV',
    'year': 2007,
    'bandwidth': 2.88e12  # 36x40G
  },{
    'company': 'IBM',
    'chip': 'Percs Hub',
    'year': 2010,
    'bandwidth': 1.856e12  # 192GB + 40GB"
  },{
    'company': 'IBM',
    'chip': 'BlueGene Q',
    'year': 2011,
    'bandwidth': 320e9  # 10x16G
  },{
    'company': 'IBM',
    'chip': 'BlueGene P',
    'year': 2007,
    'bandwidth': 40.8e9  # 6x3.4G"
  },{
    'company': 'IBM',
    'chip': 'BlueGene L',
    'year': 2005,
    'bandwidth': 16.8e9  # 6x1.4G"
  },{
    'company': 'Cray',
    'chip': 'Aries',
    'year': 2012,
    'bandwidth': 1.12e12  # 48x14G
  },{
    'company': 'Cray',
    'chip': 'Gemini',
    'year': 2010,
    'bandwidth': 750e9  # 10x12x6.25G
  },{
    'company': 'Cray',
    'chip': 'X2 (BlackWidow)',
    'year': 2006,
    'bandwidth': 1.2e12  # 64x18.75G
  },{
    # below this needs actual data, not estimate from other graph
    'company': 'SGI',
    'chip': 'Altix 3000',
    'year': 2003,
    'bandwidth': 800e9
  },{
    'company': 'IBM',
    'chip': 'HPS',
    'year': 2003,
    'bandwidth': 500e9
  },{
    'company': 'Velio',
    'chip': '3003',
    'year': 2001,
    'bandwidth': 950e9
  },{
    'company': 'Cray',
    'chip': 'X1',
    'year': 2002,
    'bandwidth': 800e9
  },{
    'company': 'Quadrics',
    'chip': 'QsNet',
    'year': 2001,
    'bandwidth': 85e9
  },{
    'company': 'IBM',
    'chip': 'SP Switch2',
    'year': 2000,
    'bandwidth': 90e9
  },{
    'company': 'Alpha',
    'chip': 'Server GS320',
    'year': 1999,
    'bandwidth': 400e9
  },{
    'company': 'SGI',
    'chip': 'Origin 2000',
    'year': 1997,
    'bandwidth': 100e9
  },{
    'company': 'Cray',
    'chip': 'T3E',
    'year': 1995,
    'bandwidth': 90e9
  },{
    'company': 'IBM',
    'chip': 'Vulcan',
    'year': 1994,
    'bandwidth': 8e9
  },{
    'company': 'MIT',
    'chip': 'Alewife',
    'year': 1994,
    'bandwidth': 3e9
  },{
    'company': 'Cray',
    'chip': 'T3D',
    'year': 1993,
    'bandwidth': 40e9
  },{
    'company': 'Intel',
    'chip': 'Paragon XP',
    'year': 1992,
    'bandwidth': 20e9
  },{
    'company': 'MIT',
    'chip': 'CM-5',
    'year': 1992,
    'bandwidth': 2e9
  },{
    'company': 'MIT',
    'chip': 'J-Machine',
    'year': 1992,
    'bandwidth': 5e9
  },{
    'company': 'Intel',
    'chip': 'iPSC/2',
    'year': 1987,
    'bandwidth': 5e9
  },{
    'company': 'Caltech',
    'chip': 'Torus Routing Chip',
    'year': 1986,
    'bandwidth': 0.5e9
  }
]

def make_field_match(field, match):
  def field_match(x):
    return True if re.match(match, x[field]) else False
  return field_match

def make_field_range(field, fmin, fmax):
  assert fmin <= fmax
  def field_range(x):
    return True if x[field] >= fmin and x[field] <= fmax else False
  return field_range

#chips = list(filter(make_field_match('company', 'IBM'), chips))
#chips = list(filter(make_field_match('chip', '.*Blue.*'), chips))
#chips = list(filter(make_field_range('year', 2000, 2009), chips))

sorters = ['company', 'year']
chips.sort(key=operator.itemgetter(*sorters), reverse=False)
for chip in chips:
  print(chip)

chips = sorted(chips, key=lambda k: k['year'])
labels = ['{0} {1}'.format(c['company'], c['chip']) for c in chips]
years = [c['year'] for c in chips]
bandwidths = [c['bandwidth'] for c in chips]
print(years)
print(bandwidths)


markers = lns.Line2D.filled_markers
colors = ['b', 'r', 'g', 'c']
styles = [(m, c) for m in markers for c in colors]
random.shuffle(styles)
markers = [s[0] for s in styles]#[0:len(years)]
colors = [s[1] for s in styles]#[0:len(years)]

fig = plt.figure(figsize=(10, 6))
ax1 = fig.add_subplot(1, 1, 1)

for idx in range(len(labels)):
  print(chips[idx])
  ax1.scatter([years[idx]], [bandwidths[idx]], s=160, c=colors[idx],
              marker=markers[idx], label=labels[idx])

ax1.set_yscale('log')

ax1.set_xlim(min(years) - 1, 2020)
ax1.set_ylim(min(bandwidths) / 2, max(bandwidths) * 2)

# set y ticks labels to {M,G,T} bps
fig.canvas.draw()
yticklabels = []
for ylabel in ax1.get_yticklabels():
  ytext = ylabel.get_text()
  if ytext:
    m = re.search('mathdefault\{10\^\{(.*)\}\}', ytext)
    exp = int(m.group(1))
    assert exp >= 0
    for unit in ['bps', 'kbps', 'Mbps', 'Gbps', 'Tbps', 'Pbps', 'Ebps', 'Zbps',
                 'Ybps']:
      if exp < 3:
        ytext = '{0} {1}'.format(10**exp, unit)
        break
      else:
        exp -= 3
    assert len(ytext) > 0
  yticklabels.append(ytext)
ax1.set_yticklabels(yticklabels)

# add per year minor ticks
#xmin, xmax = ax1.get_xlim()
#ax1.set_xticks(range(int(xmin), int(xmax)+1), minor=True)



ax1.xaxis.grid(b=True, which='major', color='k', linestyle='-')
ax1.xaxis.grid(b=True, which='minor', color='k', linestyle='--')
ax1.yaxis.grid(b=True, which='major', color='k', linestyle='-')

# shrink current x-axis
shrink = 0.30
box = ax1.get_position()
ax1.set_position([box.x0, box.y0, box.width * (1.0-shrink), box.height])

# add legend to the right of plot
ax1.legend(loc='center left', bbox_to_anchor=(1, 0.5), scatterpoints=1)

#plt.tight_layout()
plt.show()
