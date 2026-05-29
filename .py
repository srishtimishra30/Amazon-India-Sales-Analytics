import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('mysql+pymysql://root:Srishti123@localhost/amazon_fashion')
print("Connected to MySQL successfully!")

# ── TABLE 1: orders ──────────────────────────────────────────
print("Importing orders...")
df = pd.read_csv(r"C:\Users\srish\Downloads\archive\Amazon Sale Report.csv",
                 encoding='unicode_escape', low_memory=False)
df = df.drop(columns=[c for c in df.columns if 'Unnamed' in str(c)])
df = df.drop(columns=['promotion-ids'], errors='ignore')
df = df.rename(columns={
    'Order ID':'order_id','Date':'order_date','Status':'status',
    'Fulfilment':'fulfilment','Sales Channel ':'sales_channel',
    'ship-service-level':'service_level','Style':'style','SKU':'sku',
    'Category':'category','Size':'size','ASIN':'asin',
    'Courier Status':'courier_status','Qty':'qty','currency':'currency',
    'Amount':'amount','ship-city':'ship_city','ship-state':'ship_state',
    'ship-postal-code':'ship_postal_code','ship-country':'ship_country',
    'B2B':'is_b2b','fulfilled-by':'fulfilled_by'
})
df['order_date'] = pd.to_datetime(df['order_date'], format='%m-%d-%y', errors='coerce')
cols = ['order_id','order_date','status','fulfilment','sales_channel',
        'service_level','style','sku','category','size','asin',
        'courier_status','qty','currency','amount','ship_city',
        'ship_state','ship_postal_code','ship_country','is_b2b','fulfilled_by']
df[cols].drop_duplicates('order_id').to_sql('orders', engine, if_exists='replace', index=False)
print(f"✅ Orders imported: {len(df)} rows")

# ── TABLE 2: inventory ───────────────────────────────────────
print("Importing inventory...")
df2 = pd.read_csv(r"C:\Users\srish\Downloads\archive\Sale Report.csv",
                  encoding='unicode_escape', low_memory=False)
df2 = df2.rename(columns={
    'SKU Code':'sku_code','Design No.':'design_no',
    'Stock':'stock','Category':'category','Size':'size','Color':'color'
})
df2[['sku_code','design_no','stock','category','size','color']]\
    .drop_duplicates('sku_code')\
    .to_sql('inventory', engine, if_exists='replace', index=False)
print(f"✅ Inventory imported: {len(df2)} rows")

# ── TABLE 3: pricing ─────────────────────────────────────────
print("Importing pricing...")
df3 = pd.read_csv(r"C:\Users\srish\Downloads\archive\May-2022.csv",
                  encoding='unicode_escape', low_memory=False)
df3 = df3.rename(columns={
    'Sku':'sku','Style Id':'style_id','Catalog':'catalog',
    'Category':'category','Weight':'weight','TP':'cost_price',
    'Final MRP Old':'final_mrp','Amazon MRP':'amazon_mrp',
    'Amazon FBA MRP':'amazon_fba_mrp','Flipkart MRP':'flipkart_mrp',
    'Myntra MRP':'myntra_mrp','Ajio MRP':'ajio_mrp',
    'Limeroad MRP':'limeroad_mrp','Paytm MRP':'paytm_mrp',
    'Snapdeal MRP':'snapdeal_mrp'
})
for col in ['weight','cost_price','final_mrp','amazon_mrp','amazon_fba_mrp',
            'flipkart_mrp','myntra_mrp','ajio_mrp','limeroad_mrp','paytm_mrp','snapdeal_mrp']:
    df3[col] = pd.to_numeric(df3[col], errors='coerce')
df3[['sku','style_id','catalog','category','weight','cost_price','final_mrp',
     'amazon_mrp','amazon_fba_mrp','flipkart_mrp','myntra_mrp','ajio_mrp',
     'limeroad_mrp','paytm_mrp','snapdeal_mrp']]\
    .drop_duplicates('sku')\
    .to_sql('pricing', engine, if_exists='replace', index=False)
print(f"✅ Pricing imported: {len(df3)} rows")

# ── TABLE 4: international_sales ─────────────────────────────
print("Importing international sales...")
df4 = pd.read_csv(r"C:\Users\srish\Downloads\archive\International sale Report.csv",
                  encoding='unicode_escape', low_memory=False)
df4 = df4.rename(columns={
    'DATE':'sale_date','Months':'month_label','CUSTOMER':'customer',
    'Style':'style','SKU':'sku','Size':'size',
    'PCS':'pieces','RATE':'rate','GROSS AMT':'gross_amt'
})
for col in ['pieces','rate','gross_amt']:
    df4[col] = pd.to_numeric(df4[col], errors='coerce')
df4[['sale_date','month_label','customer','style','sku',
     'size','pieces','rate','gross_amt']]\
    .to_sql('international_sales', engine, if_exists='replace', index=False)
print(f"✅ International sales imported: {len(df4)} rows")

print("\n🎉 ALL DONE! Run this in Workbench to verify:")
print("SELECT 'orders', COUNT(*) FROM orders")
print("UNION ALL SELECT 'inventory', COUNT(*) FROM inventory")
print("UNION ALL SELECT 'pricing', COUNT(*) FROM pricing")
print("UNION ALL SELECT 'international_sales', COUNT(*) FROM international_sales;")