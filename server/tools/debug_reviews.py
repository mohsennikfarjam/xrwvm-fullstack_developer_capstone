import re
import requests

r = requests.get('http://localhost:8000/reviews/dealer/15')
print('status', r.status_code)
match = re.search(r'<pre class="exception_value">(.*?)</pre>', r.text, re.S)
print('exception', match.group(1).strip() if match else 'none')
for line_match in re.finditer(r'<td class="code"><pre>(.*?)</pre></td>', r.text, re.S):
    text = line_match.group(1)
    if 'views.py' in text or 'restapis.py' in text or 'TypeError' in text:
        print(text)
