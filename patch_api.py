import re

with open('frontend/src/services/api.ts', 'r') as f:
    content = f.read()

content = content.replace("setExpenses(response.data.data);", "setExpenses(response.data.data.items || []);")
content = content.replace("setTotal(response.data.total);", "setTotal(response.data.data.total || 0);")
content = content.replace("setBudgets(response.data.data);", "setBudgets(response.data.data.items || []);")

with open('frontend/src/services/api.ts', 'w') as f:
    f.write(content)
