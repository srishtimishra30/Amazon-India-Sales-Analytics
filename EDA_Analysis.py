import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
import warnings
warnings.filterwarnings('ignore')

# ── CONNECT TO MYSQL ─────────────────────────────────────────
engine = create_engine('mysql+pymysql://root:Srishti123@localhost/amazon_fashion')
df = pd.read_sql("SELECT * FROM orders", engine)
print(f"✅ Data loaded: {df.shape[0]} rows, {df.shape[1]} columns")

# ── BASIC SETUP ───────────────────────────────────────────────
df['order_date'] = pd.to_datetime(df['order_date'])
df['amount'] = pd.to_numeric(df['amount'], errors='coerce').fillna(0)
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 5)

print("\n📊 BASIC STATS:")
print(f"Date range: {df['order_date'].min()} to {df['order_date'].max()}")
print(f"Total Revenue: ₹{df[df['is_cancelled']==0]['amount'].sum():,.0f}")
print(f"Cancellation Rate: {df['is_cancelled'].mean()*100:.2f}%")
print(f"Unique Categories: {df['category'].nunique()}")
print(f"Unique States: {df['ship_state'].nunique()}")

# ═══════════════════════════════════════════════════════════════
# CHART 1: Monthly Revenue Trend
# ═══════════════════════════════════════════════════════════════
monthly = df[df['is_cancelled']==0].groupby('order_month')['amount'].sum().reset_index()
plt.figure(figsize=(12,5))
plt.plot(monthly['order_month'], monthly['amount'], marker='o',
         color='#2196F3', linewidth=2.5, markersize=8)
plt.fill_between(range(len(monthly)), monthly['amount'], alpha=0.1, color='#2196F3')
for i, row in monthly.iterrows():
    plt.annotate(f"₹{row['amount']/100000:.1f}L",
                 (i, row['amount']), textcoords="offset points",
                 xytext=(0,10), ha='center', fontsize=9)
plt.title('Monthly Revenue Trend (Apr–Jun 2022)', fontsize=14, fontweight='bold')
plt.xlabel('Month'); plt.ylabel('Revenue (INR)')
plt.xticks(range(len(monthly)), monthly['order_month'])
plt.tight_layout()
plt.savefig('chart1_monthly_revenue.png', dpi=150, bbox_inches='tight')
plt.show()
print("✅ Chart 1 saved")

# ═══════════════════════════════════════════════════════════════
# CHART 2: Revenue by Category
# ═══════════════════════════════════════════════════════════════
cat_rev = df[df['is_cancelled']==0].groupby('category')['amount']\
          .sum().sort_values(ascending=False).head(10).reset_index()
plt.figure(figsize=(12,5))
bars = plt.bar(cat_rev['category'], cat_rev['amount'],
               color=sns.color_palette("Blues_d", len(cat_rev)))
for bar, val in zip(bars, cat_rev['amount']):
    plt.text(bar.get_x()+bar.get_width()/2, bar.get_height()+50000,
             f'₹{val/100000:.1f}L', ha='center', fontsize=9)
plt.title('Top 10 Categories by Revenue', fontsize=14, fontweight='bold')
plt.xlabel('Category'); plt.ylabel('Revenue (INR)')
plt.xticks(rotation=30, ha='right')
plt.tight_layout()
plt.savefig('chart2_category_revenue.png', dpi=150, bbox_inches='tight')
plt.show()
print("✅ Chart 2 saved")

# ═══════════════════════════════════════════════════════════════
# CHART 3: Cancellation Rate by Category
# ═══════════════════════════════════════════════════════════════
cat_cancel = df.groupby('category').agg(
    total=('order_id','count'),
    cancelled=('is_cancelled','sum')
).reset_index()
cat_cancel['cancel_rate'] = cat_cancel['cancelled']/cat_cancel['total']*100
cat_cancel = cat_cancel[cat_cancel['total']>100].sort_values('cancel_rate', ascending=False).head(10)

plt.figure(figsize=(12,5))
colors = ['#e74c3c' if x > 15 else '#f39c12' if x > 10 else '#2ecc71'
          for x in cat_cancel['cancel_rate']]
bars = plt.bar(cat_cancel['category'], cat_cancel['cancel_rate'], color=colors)
for bar, val in zip(bars, cat_cancel['cancel_rate']):
    plt.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.2,
             f'{val:.1f}%', ha='center', fontsize=9)
plt.axhline(y=14.28, color='black', linestyle='--', label='Avg 14.28%')
plt.title('Cancellation Rate by Category', fontsize=14, fontweight='bold')
plt.xlabel('Category'); plt.ylabel('Cancellation Rate (%)')
plt.xticks(rotation=30, ha='right')
plt.legend(); plt.tight_layout()
plt.savefig('chart3_cancellation_by_category.png', dpi=150, bbox_inches='tight')
plt.show()
print("✅ Chart 3 saved")

# ═══════════════════════════════════════════════════════════════
# CHART 4: Top 10 States by Revenue
# ═══════════════════════════════════════════════════════════════
state_rev = df[df['is_cancelled']==0].groupby('ship_state')['amount']\
            .sum().sort_values(ascending=True).tail(10)
plt.figure(figsize=(12,5))
bars = plt.barh(state_rev.index, state_rev.values,
                color=sns.color_palette("Greens_d", len(state_rev)))
for bar, val in zip(bars, state_rev.values):
    plt.text(bar.get_width()+20000, bar.get_y()+bar.get_height()/2,
             f'₹{val/100000:.1f}L', va='center', fontsize=9)
plt.title('Top 10 States by Revenue', fontsize=14, fontweight='bold')
plt.xlabel('Revenue (INR)'); plt.tight_layout()
plt.savefig('chart4_state_revenue.png', dpi=150, bbox_inches='tight')
plt.show()
print("✅ Chart 4 saved")

# ═══════════════════════════════════════════════════════════════
# CHART 5: Fulfilment Method Comparison
# ═══════════════════════════════════════════════════════════════
ful = df.groupby('fulfilment').agg(
    orders=('order_id','count'),
    revenue=('amount','sum'),
    cancel_rate=('is_cancelled','mean')
).reset_index()
ful['cancel_rate'] = ful['cancel_rate']*100

fig, axes = plt.subplots(1, 3, figsize=(14,5))
axes[0].bar(ful['fulfilment'], ful['orders'], color=['#3498db','#e74c3c'])
axes[0].set_title('Total Orders'); axes[0].set_ylabel('Count')
axes[1].bar(ful['fulfilment'], ful['revenue'], color=['#2ecc71','#f39c12'])
axes[1].set_title('Total Revenue'); axes[1].set_ylabel('INR')
axes[2].bar(ful['fulfilment'], ful['cancel_rate'], color=['#9b59b6','#1abc9c'])
axes[2].set_title('Cancellation Rate %'); axes[2].set_ylabel('%')
fig.suptitle('Amazon vs Merchant Fulfilment Comparison', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('chart5_fulfilment_comparison.png', dpi=150, bbox_inches='tight')
plt.show()
print("✅ Chart 5 saved")

# ═══════════════════════════════════════════════════════════════
# CHART 6: B2B vs B2C
# ═══════════════════════════════════════════════════════════════
b2b = df.groupby('is_b2b').agg(
    orders=('order_id','count'),
    avg_order_value=('amount','mean')
).reset_index()
b2b['type'] = b2b['is_b2b'].map({0:'B2C', 1:'B2B'})

fig, axes = plt.subplots(1, 2, figsize=(10,5))
axes[0].pie(b2b['orders'], labels=b2b['type'], autopct='%1.1f%%',
            colors=['#3498db','#e74c3c'], startangle=90)
axes[0].set_title('Orders: B2B vs B2C')
axes[1].bar(b2b['type'], b2b['avg_order_value'], color=['#3498db','#e74c3c'])
axes[1].set_title('Avg Order Value: B2B vs B2C')
axes[1].set_ylabel('INR')
for bar, val in zip(axes[1].patches, b2b['avg_order_value']):
    axes[1].text(bar.get_x()+bar.get_width()/2, bar.get_height()+5,
                 f'₹{val:.0f}', ha='center')
plt.suptitle('B2B vs B2C Analysis', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('chart6_b2b_vs_b2c.png', dpi=150, bbox_inches='tight')
plt.show()
print("✅ Chart 6 saved")

# ═══════════════════════════════════════════════════════════════
# CHART 7: Correlation Heatmap
# ═══════════════════════════════════════════════════════════════
num_cols = ['qty','amount','is_b2b','is_cancelled','is_returned']
corr = df[num_cols].corr()
plt.figure(figsize=(8,6))
sns.heatmap(corr, annot=True, fmt='.2f', cmap='RdYlGn',
            center=0, square=True, linewidths=0.5)
plt.title('Correlation Heatmap', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('chart7_correlation_heatmap.png', dpi=150, bbox_inches='tight')
plt.show()
print("✅ Chart 7 saved")

# ═══════════════════════════════════════════════════════════════
# ML MODEL: Cancellation Predictor
# ═══════════════════════════════════════════════════════════════
print("\n🤖 Building ML Model...")
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, roc_auc_score
from xgboost import XGBClassifier
import shap

# Feature engineering
ml_df = df[['category','size','fulfilment','service_level',
            'ship_state','is_b2b','qty','amount','is_cancelled']].copy()
ml_df = ml_df.dropna()

# Encode categoricals
le = LabelEncoder()
for col in ['category','size','fulfilment','service_level','ship_state']:
    ml_df[col] = le.fit_transform(ml_df[col].astype(str))

X = ml_df.drop('is_cancelled', axis=1)
y = ml_df['is_cancelled']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)

# Train XGBoost
model = XGBClassifier(n_estimators=100, max_depth=5,
                      scale_pos_weight=5, random_state=42,
                      eval_metric='logloss')
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:,1]
auc = roc_auc_score(y_test, y_prob)
print(f"\n📈 Model Results:")
print(f"AUC-ROC Score: {auc:.4f}")
print(classification_report(y_test, y_pred))

# ═══════════════════════════════════════════════════════════════
# CHART 8: Feature Importance
# ═══════════════════════════════════════════════════════════════
feat_imp = pd.DataFrame({
    'feature': X.columns,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=True)

plt.figure(figsize=(10,6))
plt.barh(feat_imp['feature'], feat_imp['importance'],
         color=sns.color_palette("viridis", len(feat_imp)))
plt.title('XGBoost Feature Importance — What Drives Cancellations?',
          fontsize=14, fontweight='bold')
plt.xlabel('Importance Score')
plt.tight_layout()
plt.savefig('chart8_feature_importance.png', dpi=150, bbox_inches='tight')
plt.show()
print("✅ Chart 8 saved")

# ═══════════════════════════════════════════════════════════════
# CHART 9: SHAP Explainability
# ═══════════════════════════════════════════════════════════════
print("\n🔍 Generating SHAP explanation...")
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test[:500])
plt.figure()
shap.summary_plot(shap_values, X_test[:500], show=False)
plt.title('SHAP — Why Does Each Feature Push Towards Cancellation?',
          fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig('chart9_shap_summary.png', dpi=150, bbox_inches='tight')
plt.show()
print("✅ Chart 9 saved")

# ── SAVE MODEL ────────────────────────────────────────────────
import joblib
joblib.dump(model, 'cancellation_model.pkl')
print("✅ Model saved as cancellation_model.pkl")

# ── WRITE PREDICTIONS BACK TO MYSQL ──────────────────────────
print("\n💾 Writing predictions back to MySQL...")
X_full = ml_df.drop('is_cancelled', axis=1)
ml_df['churn_probability'] = model.predict_proba(X_full)[:,1]
ml_df['predicted_cancelled'] = model.predict(X_full)
ml_df[['churn_probability','predicted_cancelled']]\
    .to_sql('order_predictions', engine, if_exists='replace', index=True)
print("✅ Predictions saved to MySQL table 'order_predictions'")

print("\n" + "="*50)
print("🎉 ALL DONE! 9 charts + ML model + predictions saved!")
print("="*50)
print("Next step: Open Power BI and connect to MySQL")