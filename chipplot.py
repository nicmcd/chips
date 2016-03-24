import chipdb
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr
import matplotlib.lines as lns
import random
import re


def plot_bandwidth(db, plotfile, view=False):
  m = db.matrix()

  # make labels
  m['label'] = []
  for idx in range(len(m[chipdb.ATTR_ID[0]])):
    vals = [str(m[attr][idx]) for attr in chipdb.ATTR_ID]
    m['label'].append(' '.join(vals))

  markers = lns.Line2D.filled_markers
  colors = ['b', 'r', 'g', 'c']
  styles = [(m, c) for m in markers for c in colors]
  random.shuffle(styles)
  markers = [s[0] for s in styles]#[0:len(years)]
  colors = [s[1] for s in styles]#[0:len(years)]

  fig = plt.figure(figsize=(16, 12))
  ax1 = fig.add_subplot(1, 1, 1)

  for idx in range(len(m['label'])):
    ax1.scatter([m['year'][idx]], [m['bandwidth'][idx]], s=160, c=colors[idx],
                marker=markers[idx], label=m['label'][idx])

  ax1.set_yscale('log')

  ax1.set_xlim(min(m['year']) - 1, 2020)
  ax1.set_ylim(min(m['bandwidth']) / 2, max(m['bandwidth']) * 2)

  # set y ticks labels to {M,G,T} bps
  fig.canvas.draw()
  yticklabels = []
  for ylabel in ax1.get_yticklabels():
    ytext = ylabel.get_text()
    if ytext:
      m = re.findall('\d+', ytext)
      exp = int(m[1])
      assert exp >= 0
      for unit in ['bps', 'kbps', 'Mbps', 'Gbps', 'Tbps', 'Pbps', 'Ebps',
                   'Zbps', 'Ybps']:
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
  shrink = 0.40
  box = ax1.get_position()
  ax1.set_position([box.x0, box.y0, box.width * (1.0-shrink), box.height])

  # add legend to the right of plot
  ax1.legend(loc='center left', bbox_to_anchor=(1, 0.5), scatterpoints=1,
             fontsize=12, ncol=2)

  # axis labels and title
  ax1.set_xlabel('Year')
  ax1.set_ylabel('I/O Bandwidth')

  # show in GUI
  if view:
    plt.show()

  # save figure
  fig.savefig(plotfile)
