"""
Online Course Completion Prediction System
Predicts course completion using student learning activities and engagement metrics
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix, roc_curve
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10

def generate_course_dataset(n_samples=1000, random_state=42):
    """Generate synthetic student course completion dataset"""
    np.random.seed(random_state)
    
    data = {
        'Student_ID': [f'STU{i:04d}' for i in range(n_samples)],
        'Course_Duration_Weeks': np.random.randint(4, 16, n_samples),
        'Login_Frequency_Per_Week': np.random.randint(1, 8, n_samples),
        'Course_Progress_Percentage': np.random.uniform(0, 100, n_samples),
        'Assignments_Submitted': np.random.randint(0, 20, n_samples),
        'Quiz_Attempts': np.random.randint(0, 15, n_samples),
        'Quiz_Average_Score': np.random.uniform(0, 100, n_samples),
        'Discussion_Posts': np.random.randint(0, 50, n_samples),
        'Video_Viewing_Hours': np.random.exponential(5, n_samples),
        'Days_Since_Last_Activity': np.random.randint(0, 30, n_samples),
        'Learning_Consistency_Score': np.random.uniform(0, 1, n_samples),
        'Student_Age': np.random.randint(18, 65, n_samples),
        'Prior_Experience': np.random.choice(['None', 'Some', 'Extensive'], n_samples),
    }
    
    df = pd.DataFrame(data)
    
    # Create completion outcome based on features
    completion_prob = (
        0.3 +
        (df['Login_Frequency_Per_Week'] > 3) * 0.15 +
        (df['Course_Progress_Percentage'] > 50) * 0.2 +
        (df['Assignments_Submitted'] > 10) * 0.15 +
        (df['Quiz_Average_Score'] > 70) * 0.1 +
        (df['Discussion_Posts'] > 10) * 0.08 +
        (df['Video_Viewing_Hours'] > 10) * 0.12 +
        (df['Days_Since_Last_Activity'] < 7) * 0.15 +
        df['Learning_Consistency_Score'] * 0.1
    )
    
    df['Course_Completed'] = (np.random.rand(n_samples) < completion_prob).astype(int)
    
    return df

def preprocess_data(df):
    """Preprocess course completion data"""
    df_processed = df.copy()
    
    # Encode categorical variables
    prior_exp_dummies = pd.get_dummies(df_processed['Prior_Experience'], prefix='Prior_Exp')
    df_processed = pd.concat([df_processed, prior_exp_dummies], axis=1)
    
    # Select features
    feature_cols = [col for col in df_processed.columns if col not in 
                   ['Student_ID', 'Prior_Experience', 'Course_Completed']]
    
    return df_processed, feature_cols

def train_models(X_train, X_test, y_train, y_test):
    """Train multiple course completion prediction models"""
    models = {}
    results = []
    
    # Logistic Regression
    print("Training Logistic Regression...")
    lr = LogisticRegression(max_iter=1000, random_state=42)
    lr.fit(X_train, y_train)
    y_pred_lr = lr.predict(X_test)
    y_proba_lr = lr.predict_proba(X_test)[:, 1]
    
    models['Logistic Regression'] = lr
    results.append({
        'Model': 'Logistic Regression',
        'Accuracy': accuracy_score(y_test, y_pred_lr),
        'Precision': precision_score(y_test, y_pred_lr, zero_division=0),
        'Recall': recall_score(y_test, y_pred_lr, zero_division=0),
        'F1-Score': f1_score(y_test, y_pred_lr, zero_division=0),
        'ROC-AUC': roc_auc_score(y_test, y_proba_lr)
    })
    
    # Random Forest
    print("Training Random Forest...")
    rf = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    rf.fit(X_train, y_train)
    y_pred_rf = rf.predict(X_test)
    y_proba_rf = rf.predict_proba(X_test)[:, 1]
    
    models['Random Forest'] = rf
    results.append({
        'Model': 'Random Forest',
        'Accuracy': accuracy_score(y_test, y_pred_rf),
        'Precision': precision_score(y_test, y_pred_rf, zero_division=0),
        'Recall': recall_score(y_test, y_pred_rf, zero_division=0),
        'F1-Score': f1_score(y_test, y_pred_rf, zero_division=0),
        'ROC-AUC': roc_auc_score(y_test, y_proba_rf)
    })
    
    # Gradient Boosting
    print("Training Gradient Boosting...")
    gb = GradientBoostingClassifier(n_estimators=100, random_state=42)
    gb.fit(X_train, y_train)
    y_pred_gb = gb.predict(X_test)
    y_proba_gb = gb.predict_proba(X_test)[:, 1]
    
    models['Gradient Boosting'] = gb
    results.append({
        'Model': 'Gradient Boosting',
        'Accuracy': accuracy_score(y_test, y_pred_gb),
        'Precision': precision_score(y_test, y_pred_gb, zero_division=0),
        'Recall': recall_score(y_test, y_pred_gb, zero_division=0),
        'F1-Score': f1_score(y_test, y_pred_gb, zero_division=0),
        'ROC-AUC': roc_auc_score(y_test, y_proba_gb)
    })
    
    return models, pd.DataFrame(results), y_pred_rf, y_proba_rf

def plot_completion_distribution(df):
    """Plot course completion distribution"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    completion_counts = df['Course_Completed'].value_counts()
    colors = ['#e74c3c', '#2ecc71']
    
    axes[0].bar(['Not Completed', 'Completed'], completion_counts.values, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    axes[0].set_ylabel('Count', fontsize=11, fontweight='bold')
    axes[0].set_title('Course Completion Distribution', fontsize=12, fontweight='bold')
    axes[0].grid(axis='y', alpha=0.3)
    
    for i, v in enumerate(completion_counts.values):
        axes[0].text(i, v + 10, str(v), ha='center', fontweight='bold')
    
    # Completion rate by prior experience
    completion_by_exp = df.groupby('Prior_Experience')['Course_Completed'].agg(['sum', 'count'])
    completion_by_exp['Completion_Rate'] = (completion_by_exp['sum'] / completion_by_exp['count'] * 100).round(2)
    
    axes[1].bar(completion_by_exp.index, completion_by_exp['Completion_Rate'], color=['#3498db', '#e74c3c', '#2ecc71'], 
               alpha=0.8, edgecolor='black', linewidth=1.5)
    axes[1].set_ylabel('Completion Rate (%)', fontsize=11, fontweight='bold')
    axes[1].set_title('Completion Rate by Prior Experience', fontsize=12, fontweight='bold')
    axes[1].grid(axis='y', alpha=0.3)
    
    for i, v in enumerate(completion_by_exp['Completion_Rate']):
        axes[1].text(i, v + 1, f'{v:.1f}%', ha='center', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/course_completion_distribution.png', dpi=300, bbox_inches='tight')
    print("Saved: course_completion_distribution.png")
    plt.close()

def plot_model_comparison(results_df):
    """Plot model performance comparison"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    metrics = ['Accuracy', 'Precision', 'Recall', 'F1-Score', 'ROC-AUC']
    x = np.arange(len(results_df))
    width = 0.15
    
    for idx, metric in enumerate(metrics):
        axes[0].bar(x + idx * width, results_df[metric], width, label=metric, alpha=0.8, edgecolor='black', linewidth=1.5)
    
    axes[0].set_xlabel('Model', fontsize=11, fontweight='bold')
    axes[0].set_ylabel('Score', fontsize=11, fontweight='bold')
    axes[0].set_title('Model Performance Comparison', fontsize=12, fontweight='bold')
    axes[0].set_xticks(x + width * 2)
    axes[0].set_xticklabels(results_df['Model'], fontsize=10)
    axes[0].legend(fontsize=9, loc='lower right')
    axes[0].grid(axis='y', alpha=0.3)
    axes[0].set_ylim([0, 1.1])
    
    # ROC-AUC comparison
    colors = ['#3498db', '#e74c3c', '#2ecc71']
    axes[1].bar(results_df['Model'], results_df['ROC-AUC'], color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    axes[1].set_ylabel('ROC-AUC Score', fontsize=11, fontweight='bold')
    axes[1].set_title('Model ROC-AUC Comparison', fontsize=12, fontweight='bold')
    axes[1].grid(axis='y', alpha=0.3)
    axes[1].set_ylim([0, 1.1])
    
    for i, v in enumerate(results_df['ROC-AUC']):
        axes[1].text(i, v + 0.02, f'{v:.3f}', ha='center', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/course_model_comparison.png', dpi=300, bbox_inches='tight')
    print("Saved: course_model_comparison.png")
    plt.close()

def plot_confusion_matrices(models, X_test, y_test):
    """Plot confusion matrices"""
    fig, axes = plt.subplots(1, 3, figsize=(14, 4))
    
    for idx, (model_name, model) in enumerate(models.items()):
        y_pred = model.predict(X_test)
        cm = confusion_matrix(y_test, y_pred)
        
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[idx],
                   xticklabels=['Not Completed', 'Completed'], yticklabels=['Not Completed', 'Completed'],
                   cbar=False, annot_kws={'fontsize': 11, 'fontweight': 'bold'})
        axes[idx].set_title(f'{model_name}', fontsize=12, fontweight='bold')
        axes[idx].set_ylabel('True Label', fontsize=10, fontweight='bold')
        axes[idx].set_xlabel('Predicted Label', fontsize=10, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/course_confusion_matrices.png', dpi=300, bbox_inches='tight')
    print("Saved: course_confusion_matrices.png")
    plt.close()

def plot_roc_curves(models, X_test, y_test):
    """Plot ROC curves"""
    fig, ax = plt.subplots(figsize=(10, 8))
    
    colors = ['#3498db', '#e74c3c', '#2ecc71']
    
    for idx, (model_name, model) in enumerate(models.items()):
        y_proba = model.predict_proba(X_test)[:, 1]
        fpr, tpr, _ = roc_curve(y_test, y_proba)
        auc = roc_auc_score(y_test, y_proba)
        
        ax.plot(fpr, tpr, color=colors[idx], lw=2, label=f'{model_name} (AUC = {auc:.3f})', marker='o', markersize=4)
    
    ax.plot([0, 1], [0, 1], 'k--', lw=2, label='Random Classifier')
    ax.set_xlabel('False Positive Rate', fontsize=11, fontweight='bold')
    ax.set_ylabel('True Positive Rate', fontsize=11, fontweight='bold')
    ax.set_title('ROC Curves - Course Completion Prediction', fontsize=12, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/course_roc_curves.png', dpi=300, bbox_inches='tight')
    print("Saved: course_roc_curves.png")
    plt.close()

def plot_feature_importance(models):
    """Plot feature importance"""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Random Forest
    rf = models['Random Forest']
    feature_importance_rf = pd.DataFrame({
        'Feature': range(len(rf.feature_importances_)),
        'Importance': rf.feature_importances_
    }).sort_values('Importance', ascending=False).head(10)
    
    axes[0].barh(feature_importance_rf['Feature'].astype(str), feature_importance_rf['Importance'], 
                color='#3498db', alpha=0.8, edgecolor='black', linewidth=1.5)
    axes[0].set_xlabel('Importance', fontsize=11, fontweight='bold')
    axes[0].set_title('Random Forest - Top 10 Features', fontsize=12, fontweight='bold')
    axes[0].invert_yaxis()
    axes[0].grid(axis='x', alpha=0.3)
    
    # Gradient Boosting
    gb = models['Gradient Boosting']
    feature_importance_gb = pd.DataFrame({
        'Feature': range(len(gb.feature_importances_)),
        'Importance': gb.feature_importances_
    }).sort_values('Importance', ascending=False).head(10)
    
    axes[1].barh(feature_importance_gb['Feature'].astype(str), feature_importance_gb['Importance'],
                color='#e74c3c', alpha=0.8, edgecolor='black', linewidth=1.5)
    axes[1].set_xlabel('Importance', fontsize=11, fontweight='bold')
    axes[1].set_title('Gradient Boosting - Top 10 Features', fontsize=12, fontweight='bold')
    axes[1].invert_yaxis()
    axes[1].grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/course_feature_importance.png', dpi=300, bbox_inches='tight')
    print("Saved: course_feature_importance.png")
    plt.close()

def plot_engagement_analysis(df):
    """Plot engagement metrics analysis"""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Login frequency vs completion
    login_completion = df.groupby('Login_Frequency_Per_Week')['Course_Completed'].agg(['sum', 'count'])
    login_completion['Completion_Rate'] = (login_completion['sum'] / login_completion['count'] * 100).round(2)
    
    axes[0, 0].scatter(login_completion.index, login_completion['Completion_Rate'], s=100, color='#3498db', alpha=0.7, edgecolor='black', linewidth=1.5)
    axes[0, 0].plot(login_completion.index, login_completion['Completion_Rate'], color='#3498db', linewidth=2, alpha=0.5)
    axes[0, 0].set_xlabel('Login Frequency (per week)', fontsize=10, fontweight='bold')
    axes[0, 0].set_ylabel('Completion Rate (%)', fontsize=10, fontweight='bold')
    axes[0, 0].set_title('Login Frequency vs Completion Rate', fontsize=11, fontweight='bold')
    axes[0, 0].grid(alpha=0.3)
    
    # Course progress vs completion
    progress_bins = pd.cut(df['Course_Progress_Percentage'], bins=[0, 25, 50, 75, 100], labels=['0-25%', '25-50%', '50-75%', '75-100%'])
    progress_completion = df.groupby(progress_bins)['Course_Completed'].agg(['sum', 'count'])
    progress_completion['Completion_Rate'] = (progress_completion['sum'] / progress_completion['count'] * 100).round(2)
    
    axes[0, 1].bar(progress_completion.index.astype(str), progress_completion['Completion_Rate'], color='#e74c3c', alpha=0.8, edgecolor='black', linewidth=1.5)
    axes[0, 1].set_xlabel('Course Progress', fontsize=10, fontweight='bold')
    axes[0, 1].set_ylabel('Completion Rate (%)', fontsize=10, fontweight='bold')
    axes[0, 1].set_title('Course Progress vs Completion Rate', fontsize=11, fontweight='bold')
    axes[0, 1].grid(axis='y', alpha=0.3)
    
    # Quiz performance vs completion
    quiz_bins = pd.cut(df['Quiz_Average_Score'], bins=[0, 50, 70, 85, 100], labels=['0-50', '50-70', '70-85', '85-100'])
    quiz_completion = df.groupby(quiz_bins)['Course_Completed'].agg(['sum', 'count'])
    quiz_completion['Completion_Rate'] = (quiz_completion['sum'] / quiz_completion['count'] * 100).round(2)
    
    axes[1, 0].bar(quiz_completion.index.astype(str), quiz_completion['Completion_Rate'], color='#2ecc71', alpha=0.8, edgecolor='black', linewidth=1.5)
    axes[1, 0].set_xlabel('Quiz Average Score', fontsize=10, fontweight='bold')
    axes[1, 0].set_ylabel('Completion Rate (%)', fontsize=10, fontweight='bold')
    axes[1, 0].set_title('Quiz Performance vs Completion Rate', fontsize=11, fontweight='bold')
    axes[1, 0].grid(axis='y', alpha=0.3)
    
    # Days since activity vs completion
    activity_bins = pd.cut(df['Days_Since_Last_Activity'], bins=[0, 7, 14, 21, 30], labels=['0-7 days', '7-14 days', '14-21 days', '21-30 days'])
    activity_completion = df.groupby(activity_bins)['Course_Completed'].agg(['sum', 'count'])
    activity_completion['Completion_Rate'] = (activity_completion['sum'] / activity_completion['count'] * 100).round(2)
    
    axes[1, 1].bar(activity_completion.index.astype(str), activity_completion['Completion_Rate'], color='#f39c12', alpha=0.8, edgecolor='black', linewidth=1.5)
    axes[1, 1].set_xlabel('Days Since Last Activity', fontsize=10, fontweight='bold')
    axes[1, 1].set_ylabel('Completion Rate (%)', fontsize=10, fontweight='bold')
    axes[1, 1].set_title('Activity Recency vs Completion Rate', fontsize=11, fontweight='bold')
    axes[1, 1].grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/course_engagement_analysis.png', dpi=300, bbox_inches='tight')
    print("Saved: course_engagement_analysis.png")
    plt.close()

def main():
    print("="*80)
    print("ONLINE COURSE COMPLETION PREDICTION SYSTEM")
    print("="*80)
    
    # Generate dataset
    print("\n[1] Generating synthetic student course dataset...")
    df = generate_course_dataset(n_samples=1000)
    df.to_csv('/home/ubuntu/course_data.csv', index=False)
    print(f"Dataset generated: {len(df)} students")
    print(f"Completion rate: {df['Course_Completed'].mean()*100:.2f}%")
    
    # Preprocess data
    print("\n[2] Preprocessing data...")
    df_processed, feature_cols = preprocess_data(df)
    X = df_processed[feature_cols].values
    y = df_processed['Course_Completed'].values
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print(f"Training set: {len(X_train)}, Test set: {len(X_test)}")
    
    # Train models
    print("\n[3] Training course completion prediction models...")
    models, results_df, y_pred_rf, y_proba_rf = train_models(X_train, X_test, y_train, y_test)
    results_df.to_csv('/home/ubuntu/course_model_results.csv', index=False)
    print("\nModel Results:")
    print(results_df.to_string(index=False))
    
    # Generate visualizations
    print("\n[4] Generating visualizations...")
    plot_completion_distribution(df)
    plot_model_comparison(results_df)
    plot_confusion_matrices(models, X_test, y_test)
    plot_roc_curves(models, X_test, y_test)
    plot_feature_importance(models)
    plot_engagement_analysis(df)
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE - All visualizations saved")
    print("="*80)

if __name__ == "__main__":
    main()
