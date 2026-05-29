import pandas as pd

df = pd.read_csv(r'C:\Users\srish\Desktop\Amazon-fashion\orders.csv')

# Fix all dirty state names
replacements = {
    'RJ': 'RAJASTHAN', 'rajsthan': 'RAJASTHAN', 'Rajshthan': 'RAJASTHAN',
    'Rajasthan': 'RAJASTHAN', 'orissa': 'ODISHA', 'Pondicherry': 'PUDUCHERRY',
    'Punjab/Mohali/...': 'PUNJAB', 'NL': 'NAGALAND', 'PB': 'PUNJAB',
    'AR': 'ARUNACHAL PRADESH', 'New Delhi': 'DELHI'
}
df['ship_state'] = df['ship_state'].replace(replacements)
df.to_csv(r'C:\Users\srish\Desktop\Amazon-fashion\orders.csv', index=False)
print("✅ CSV cleaned!")