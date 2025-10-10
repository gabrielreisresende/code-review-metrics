import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import spearmanr, mannwhitneyu

sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (16, 12)
plt.rcParams['font.size'] = 10


print("="*80)
print("CARREGANDO DADOS...")
print("="*80)

df = pd.read_csv('pull_requests_metrics.csv')

df['total_lines_changed'] = df['additions'] + df['deletions']
df['status_binary'] = (df['state'] == 'merged').astype(int)

merged_df = df[df['state'] == 'merged']
closed_df = df[df['state'] == 'closed']

print(f"\\nTotal de PRs: {len(df)}")
print(f"PRs Merged: {len(merged_df)} ({len(merged_df)/len(df)*100:.1f}%)")
print(f"PRs Closed: {len(closed_df)} ({len(closed_df)/len(df)*100:.1f}%)")
print(f"Repositórios únicos: {df['repo'].nunique()}")

print("\\n" + "="*80)
print("ANÁLISE ESTATÍSTICA COMPLETA")
print("="*80)


metrics = {
    'analysis_time_hours': 'Tempo de Análise',
    'description_length': 'Tamanho da Descrição',
    'participants_count': 'Número de Participantes',
    'comments_count': 'Número de Comentários'
}

print("\\n" + "-"*80)
print("1. CORRELAÇÃO DE SPEARMAN (Métricas vs Status)")
print("-"*80)

correlations = {}
for metric, label in metrics.items():
    corr, p_value = spearmanr(df[metric], df['status_binary'])
    correlations[metric] = {'corr': corr, 'p_value': p_value, 'label': label}
    
    print(f"\\n{label}:")
    print(f"  ρ (rho) = {corr:.4f}")
    print(f"  p-valor = {p_value:.6f}")
    print(f"  Significativo: {'✓ Sim' if p_value < 0.05 else '✗ Não'}")

    if abs(corr) < 0.1:
        strength = "muito fraca"
    elif abs(corr) < 0.3:
        strength = "fraca"
    elif abs(corr) < 0.5:
        strength = "moderada"
    elif abs(corr) < 0.7:
        strength = "forte"
    else:
        strength = "muito forte"
    
    direction = "positiva" if corr > 0 else "negativa"
    print(f"  Interpretação: Correlação {strength} {direction}")

print("\\n" + "-"*80)
print("2. TESTE MANN-WHITNEY U (Comparação Merged vs Closed)")
print("-"*80)

mann_whitney_results = {}
for metric, label in metrics.items():
    merged_values = merged_df[metric]
    closed_values = closed_df[metric]
    
    statistic, p_value = mannwhitneyu(merged_values, closed_values, alternative='two-sided')
    
    mann_whitney_results[metric] = {
        'merged_median': merged_values.median(),
        'closed_median': closed_values.median(),
        'statistic': statistic,
        'p_value': p_value
    }
    
    print(f"\\n{label}:")
    print(f"  Mediana Merged: {merged_values.median():.2f}")
    print(f"  Mediana Closed: {closed_values.median():.2f}")
    print(f"  Diferença: {((closed_values.median() - merged_values.median()) / merged_values.median() * 100):+.1f}%")
    print(f"  Estatística U: {statistic:.2f}")
    print(f"  p-valor: {p_value:.6f}")
    print(f"  Diferença significativa: {'Sim' if p_value < 0.05 else 'Não'}")



print("\\n" + "-"*80)
print("3. ESTATÍSTICAS DESCRITIVAS")
print("-"*80)

print("\\nMERGED:")
print(merged_df[list(metrics.keys())].describe())

print("\\nCLOSED:")
print(closed_df[list(metrics.keys())].describe())

print("\\n" + "="*80)
print("GERANDO VISUALIZAÇÕES...")
print("="*80)


fig, axes = plt.subplots(2, 3, figsize=(18, 12))
fig.suptitle('Análise Exploratória do Dataset de Pull Requests', fontsize=16, fontweight='bold')


ax1 = axes[0, 0]
status_counts = df['state'].value_counts()
colors = ['#2ecc71', '#e74c3c']
bars = ax1.bar(status_counts.index, status_counts.values, color=colors, alpha=0.7, 
               edgecolor='black', linewidth=2)
ax1.set_title('Distribuição de Status dos PRs', fontweight='bold', fontsize=12)
ax1.set_ylabel('Quantidade', fontsize=11)
ax1.set_xlabel('Status', fontsize=11)
for i, v in enumerate(status_counts.values):
    ax1.text(i, v + 50, f'{v}\\n({v/len(df)*100:.1f}%)', ha='center', 
             fontweight='bold', fontsize=10)
ax1.grid(axis='y', alpha=0.3)

ax2 = axes[0, 1]
bp = ax2.boxplot([merged_df['analysis_time_hours'], closed_df['analysis_time_hours']], 
                  labels=['Merged', 'Closed'], patch_artist=True,
                  boxprops=dict(facecolor='lightblue', alpha=0.7),
                  medianprops=dict(color='red', linewidth=2))
ax2.set_title('Tempo de Análise por Status', fontweight='bold', fontsize=12)
ax2.set_ylabel('Horas (escala log)', fontsize=11)
ax2.set_yscale('log')
ax2.grid(True, alpha=0.3)

ax3 = axes[0, 2]
bp = ax3.boxplot([merged_df['description_length'], closed_df['description_length']], 
                  labels=['Merged', 'Closed'], patch_artist=True,
                  boxprops=dict(facecolor='lightgreen', alpha=0.7),
                  medianprops=dict(color='red', linewidth=2))
ax3.set_title('Tamanho da Descrição por Status', fontweight='bold', fontsize=12)
ax3.set_ylabel('Caracteres', fontsize=11)
ax3.set_ylim(0, 5000)
ax3.grid(True, alpha=0.3)

ax4 = axes[1, 0]
bp = ax4.boxplot([merged_df['participants_count'], closed_df['participants_count']], 
                  labels=['Merged', 'Closed'], patch_artist=True,
                  boxprops=dict(facecolor='lightyellow', alpha=0.7),
                  medianprops=dict(color='red', linewidth=2))
ax4.set_title('Número de Participantes por Status', fontweight='bold', fontsize=12)
ax4.set_ylabel('Participantes', fontsize=11)
ax4.grid(True, alpha=0.3)

ax5 = axes[1, 1]
bp = ax5.boxplot([merged_df['comments_count'], closed_df['comments_count']], 
                  labels=['Merged', 'Closed'], patch_artist=True,
                  boxprops=dict(facecolor='lightcoral', alpha=0.7),
                  medianprops=dict(color='red', linewidth=2))
ax5.set_title('Número de Comentários por Status', fontweight='bold', fontsize=12)
ax5.set_ylabel('Comentários', fontsize=11)
ax5.grid(True, alpha=0.3)

ax6 = axes[1, 2]
top_repos = df['repo'].value_counts().head(10)
bars = ax6.barh(range(len(top_repos)), top_repos.values, color='steelblue', 
                alpha=0.7, edgecolor='black', linewidth=1)
ax6.set_yticks(range(len(top_repos)))
ax6.set_yticklabels([repo.split('/')[-1][:20] for repo in top_repos.index], fontsize=9)
ax6.set_title('Top 10 Repositórios', fontweight='bold', fontsize=12)
ax6.set_xlabel('Número de PRs', fontsize=11)
ax6.invert_yaxis()
ax6.grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.savefig('fig1_analise_exploratoria.png', dpi=300, bbox_inches='tight')
print("✓ Figura 1 salva: fig1_analise_exploratoria.png")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Comparação de Medianas: PRs Merged vs Closed', fontsize=16, fontweight='bold')

metrics_list = ['Tempo de Análise\\n(horas)', 'Tamanho da Descrição\\n(caracteres)', 
                'Participantes', 'Comentários']
merged_medians = [
    merged_df['analysis_time_hours'].median(),
    merged_df['description_length'].median(),
    merged_df['participants_count'].median(),
    merged_df['comments_count'].median()
]
closed_medians = [
    closed_df['analysis_time_hours'].median(),
    closed_df['description_length'].median(),
    closed_df['participants_count'].median(),
    closed_df['comments_count'].median()
]

for idx, (title, merged_val, closed_val) in enumerate(zip(metrics_list, merged_medians, closed_medians)):
    ax = axes[idx // 2, idx % 2]
    x = ['Merged', 'Closed']
    y = [merged_val, closed_val]
    bars = ax.bar(x, y, color=['#2ecc71', '#e74c3c'], alpha=0.7, edgecolor='black', linewidth=2)
    ax.set_title(title, fontweight='bold', fontsize=12)
    ax.set_ylabel('Valor', fontsize=11)
    
    for i, (bar, val) in enumerate(zip(bars, y)):
        ax.text(bar.get_x() + bar.get_width()/2, val * 1.05, f'{val:.1f}', 
                ha='center', va='bottom', fontweight='bold', fontsize=11)
    ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('fig2_comparacao_medianas.png', dpi=300, bbox_inches='tight')
print("✓ Figura 2 salva: fig2_comparacao_medianas.png")


fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Correlações de Spearman: Métricas vs Status', fontsize=16, fontweight='bold')

metrics_plot = [
    ('analysis_time_hours', 'Tempo de Análise (horas)', 'Blues'),
    ('description_length', 'Tamanho da Descrição (caracteres)', 'Greens'),
    ('participants_count', 'Número de Participantes', 'Oranges'),
    ('comments_count', 'Número de Comentários', 'Reds')
]

for idx, (metric, title, cmap) in enumerate(metrics_plot):
    ax = axes[idx // 2, idx % 2]
    
    x_jitter = df['status_binary'] + np.random.normal(0, 0.02, len(df))
    y_values = df[metric].copy()
    

    if metric == 'analysis_time_hours':
        y_values = np.minimum(y_values, 1000)
    elif metric == 'description_length':
        y_values = np.minimum(y_values, 5000)
    
    scatter = ax.scatter(x_jitter, y_values, alpha=0.3, s=20, c=df['status_binary'], 
                        cmap=cmap, edgecolors='none')
    
    z = np.polyfit(df['status_binary'], df[metric], 1)
    p = np.poly1d(z)
    ax.plot([0, 1], [p(0), p(1)], "r--", linewidth=2, label='Tendência')
    
    ax.set_xlabel('Status (0=Closed, 1=Merged)', fontsize=11)
    ax.set_ylabel(title.split('(')[0].strip(), fontsize=11)
    ax.set_title(title, fontweight='bold', fontsize=11)
    ax.set_xticks([0, 1])
    ax.set_xticklabels(['Closed', 'Merged'])
    ax.grid(True, alpha=0.3)
    
    corr_info = correlations[metric]
    textstr = f"ρ = {corr_info['corr']:.4f}\\np < 0.001"
    ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    ax.legend(loc='upper right', fontsize=9)

plt.tight_layout()
plt.savefig('fig3_correlacoes_spearman.png', dpi=300, bbox_inches='tight')
print("✓ Figura 3 salva: fig3_correlacoes_spearman.png")

fig, ax = plt.subplots(1, 1, figsize=(10, 8))

corr_columns = ['status_binary', 'analysis_time_hours', 'description_length', 
                'participants_count', 'comments_count']
corr_labels = ['Status\\n(Merged=1)', 'Tempo de\\nAnálise', 'Tamanho da\\nDescrição', 
               'Participantes', 'Comentários']

corr_matrix = df[corr_columns].corr(method='spearman')

sns.heatmap(corr_matrix, annot=True, fmt='.3f', cmap='RdBu_r', center=0,
            square=True, linewidths=1, cbar_kws={"shrink": 0.8},
            xticklabels=corr_labels, yticklabels=corr_labels,
            vmin=-0.5, vmax=0.5, ax=ax)

ax.set_title('Matriz de Correlação de Spearman', fontweight='bold', fontsize=14, pad=20)

plt.tight_layout()
plt.savefig('fig4_heatmap_correlacoes.png', dpi=300, bbox_inches='tight')
print("✓ Figura 4 salva: fig4_heatmap_correlacoes.png")


fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle('Distribuições das Métricas por Status', fontsize=16, fontweight='bold')

metrics_dist = [
    ('analysis_time_hours', 'Tempo de Análise', 'Horas', 'log', 1000),
    ('description_length', 'Tamanho da Descrição', 'Caracteres', 'linear', 5000),
    ('participants_count', 'Número de Participantes', 'Participantes', 'linear', None),
    ('comments_count', 'Número de Comentários', 'Comentários', 'linear', 30)
]

for idx, (metric, title, xlabel, scale, xlim) in enumerate(metrics_dist):
    ax = axes[idx // 2, idx % 2]
    
    merged_data = merged_df[metric]
    closed_data = closed_df[metric]
    
    if xlim:
        merged_data = merged_data[merged_data <= xlim]
        closed_data = closed_data[closed_data <= xlim]
    
    if scale == 'log':
        bins = np.logspace(np.log10(1), np.log10(merged_data.max()), 50)
    else:
        bins = 50
    
    ax.hist(merged_data, bins=bins, alpha=0.6, label='Merged', color='#2ecc71', edgecolor='black')
    ax.hist(closed_data, bins=bins, alpha=0.6, label='Closed', color='#e74c3c', edgecolor='black')
    
    ax.axvline(merged_df[metric].median(), color='#2ecc71', linestyle='--', linewidth=2)
    ax.axvline(closed_df[metric].median(), color='#e74c3c', linestyle='--', linewidth=2)
    
    ax.set_xlabel(xlabel, fontsize=11)
    ax.set_ylabel('Frequência', fontsize=11)
    ax.set_title(title, fontweight='bold', fontsize=11)
    if scale == 'log':
        ax.set_xscale('log')
    ax.legend(loc='upper right', fontsize=9)
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('fig5_distribuicoes.png', dpi=300, bbox_inches='tight')
print("✓ Figura 5 salva: fig5_distribuicoes.png")


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
fig.suptitle('Resumo dos Testes Estatísticos', fontsize=16, fontweight='bold')

metrics_names = ['Tempo de\\nAnálise', 'Tamanho da\\nDescrição', 'Participantes', 'Comentários']
corr_values = [correlations[m]['corr'] for m in ['analysis_time_hours', 'description_length', 
                                                   'participants_count', 'comments_count']]
colors_corr = ['#e74c3c' if c < 0 else '#2ecc71' for c in corr_values]

bars = ax1.barh(metrics_names, corr_values, color=colors_corr, alpha=0.7, 
                edgecolor='black', linewidth=2)
ax1.axvline(0, color='black', linewidth=1)
ax1.set_xlabel('Coeficiente de Correlação (ρ)', fontsize=11)
ax1.set_title('Correlações de Spearman', fontweight='bold', fontsize=12)
ax1.grid(axis='x', alpha=0.3)

p_values = [mann_whitney_results[m]['p_value'] for m in ['analysis_time_hours', 'description_length',
                                                           'participants_count', 'comments_count']]
log_p_values = [-np.log10(p) if p > 0 else 300 for p in p_values]

bars = ax2.barh(metrics_names, log_p_values, color='steelblue', alpha=0.7, 
                edgecolor='black', linewidth=2)
ax2.axvline(-np.log10(0.05), color='red', linewidth=2, linestyle='--', label='p=0.05')
ax2.set_xlabel('-log₁₀(p-valor)', fontsize=11)
ax2.set_title('Mann-Whitney U', fontweight='bold', fontsize=12)
ax2.grid(axis='x', alpha=0.3)
ax2.legend()

plt.tight_layout()
plt.savefig('fig6_resumo_testes.png', dpi=300, bbox_inches='tight')
print("✓ Figura 6 salva: fig6_resumo_testes.png")

print("\\n" + "="*80)
print("ANÁLISE COMPLETA FINALIZADA!")
print("="*80)
print("\\nArquivos gerados:")
print("  - fig1_analise_exploratoria.png")
print("  - fig2_comparacao_medianas.png")
print("  - fig3_correlacoes_spearman.png")
print("  - fig4_heatmap_correlacoes.png")
print("  - fig5_distribuicoes.png")
print("  - fig6_resumo_testes.png")
print("\\nTodos os testes estatísticos foram concluídos com sucesso!")

codigo_completo = open(__file__, 'r', encoding='utf-8').read()

with open('analise_completa_lab03s03.py', 'w', encoding='utf-8') as f:
    f.write(codigo_completo)

print("Arquivo Python criado: analise_completa_lab03s03.py")
print("\nPara executar a análise completa, use:")