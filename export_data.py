import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('mysql+pymysql://root:Srishti123@localhost/amazon_fashion')

tables = ['orders','inventory','pricing','international_sales','order_predictions']
for t in tables:
    df = pd.read_sql(f"SELECT * FROM {t}", engine)
    df.to_csv(rf'C:\Users\srish\Desktop\Amazon-fashion\{t}.csv', index=False)
    print(f"✅ {t}.csv saved — {len(df)} rows")

print("\n🎉 All CSVs ready for Power BI!")