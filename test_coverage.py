import os

print('---')
for root, dirs, files in os.walk(os.path.dirname(os.path.abspath(__file__))):
    for file in files:
        if file.endswith('.py') and not file.endswith('_test.py'):
            if file[:-3] + '_test.py' not in files:
                print(os.path.join(root, file))
print('---')
