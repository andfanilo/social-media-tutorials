import time
import random
from datetime import datetime
from h2o_wave import site

def get_browser_data(i):
    current_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    return [
        (current_time, 'Chrome', random.randint(10000, 50000)),
        (current_time, 'Firefox', random.randint(10000, 50000)),
        (current_time, 'Safari', random.randint(10000, 50000)),
    ]

page = site["/"]

counter_card = page["counter"]
plot_card = page['plot']

for counter in range(1, 1000):
    counter_card.data.i = counter
    chrome, firefox, safari = get_browser_data(counter) 
    plot_card.data[-1] = chrome
    plot_card.data[-1] = firefox
    plot_card.data[-1] = safari
    page.save()
    time.sleep(1)
