import re

with open('frontend/src/services/api.ts', 'r') as f:
    content = f.read()

content = content.replace("export interface Expense {\n  id: string;", "export interface Expense {\n  id: number;")
content = content.replace("spent: number;", "spent?: number;")

with open('frontend/src/services/api.ts', 'w') as f:
    f.write(content)
