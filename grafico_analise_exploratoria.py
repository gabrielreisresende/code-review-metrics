import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

fig, axes = plt.subplots(2, 3, figsize=(18, 12))
fig.suptitle('Análise Exploratória do Dataset de Pull Requests', fontsize=16, fontweight='bold')

df = pd.read_csv('pull_requests_metrics.csv')


ax1 = axes[0, 0]
status_counts = df['state'].value_counts()
colors = ['#2ecc71', '#e74c3c']
bars = ax1.bar(status_counts.index, status_counts.values, color=colors, alpha=0.7, edgecolor='black', linewidth=2)
ax1.set_title('Distribuição de Status dos PRs', fontweight='bold', fontsize=12)
ax1.set_ylabel('Quantidade', fontsize=11)
ax1.set_xlabel('Status', fontsize=11)
for i, v in enumerate(status_counts.values):
    ax1.text(i, v + 50, f'{v}\n({v/len(df)*100:.1f}%)', ha='center', fontweight='bold', fontsize=10)
ax1.grid(axis='y', alpha=0.3)


ax2 = axes[0, 1]
merged_times = df[df['state'] == 'merged']['analysis_time_hours']
closed_times = df[df['state'] == 'closed']['analysis_time_hours']
bp = ax2.boxplot([merged_times, closed_times], labels=['Merged', 'Closed'], patch_artist=True,
            boxprops=dict(facecolor='lightblue', alpha=0.7),
            medianprops=dict(color='red', linewidth=2),
            whiskerprops=dict(linewidth=1.5),
            capprops=dict(linewidth=1.5))
ax2.set_title('Tempo de Análise por Status', fontweight='bold', fontsize=12)
ax2.set_ylabel('Horas (escala log)', fontsize=11)
ax2.set_yscale('log')
ax2.grid(True, alpha=0.3)

ax3 = axes[0, 2]
merged_desc = df[df['state'] == 'merged']['description_length']
closed_desc = df[df['state'] == 'closed']['description_length']
bp = ax3.boxplot([merged_desc, closed_desc], labels=['Merged', 'Closed'], patch_artist=True,
            boxprops=dict(facecolor='lightgreen', alpha=0.7),
            medianprops=dict(color='red', linewidth=2),
            whiskerprops=dict(linewidth=1.5),
            capprops=dict(linewidth=1.5))
ax3.set_title('Tamanho da Descrição por Status', fontweight='bold', fontsize=12)
ax3.set_ylabel('Caracteres', fontsize=11)
ax3.set_ylim(0, 5000)
ax3.grid(True, alpha=0.3)


ax4 = axes[1, 0]
merged_part = df[df['state'] == 'merged']['participants_count']
closed_part = df[df['state'] == 'closed']['participants_count']
bp = ax4.boxplot([merged_part, closed_part], labels=['Merged', 'Closed'], patch_artist=True,
            boxprops=dict(facecolor='lightyellow', alpha=0.7),
            medianprops=dict(color='red', linewidth=2),
            whiskerprops=dict(linewidth=1.5),
            capprops=dict(linewidth=1.5))
ax4.set_title('Número de Participantes por Status', fontweight='bold', fontsize=12)
ax4.set_ylabel('Participantes', fontsize=11)
ax4.grid(True, alpha=0.3)

ax5 = axes[1, 1]
merged_comm = df[df['state'] == 'merged']['comments_count']
closed_comm = df[df['state'] == 'closed']['comments_count']
bp = ax5.boxplot([merged_comm, closed_comm], labels=['Merged', 'Closed'], patch_artist=True,
            boxprops=dict(facecolor='lightcoral', alpha=0.7),
            medianprops=dict(color='red', linewidth=2),
            whiskerprops=dict(linewidth=1.5),
            capprops=dict(linewidth=1.5))
ax5.set_title('Número de Comentários por Status', fontweight='bold', fontsize=12)
ax5.set_ylabel('Comentários', fontsize=11)
ax5.grid(True, alpha=0.3)

ax6 = axes[1, 2]
top_repos = df['repo'].value_counts().head(10)
bars = ax6.barh(range(len(top_repos)), top_repos.values, color='steelblue', alpha=0.7, edgecolor='black', linewidth=1)
ax6.set_yticks(range(len(top_repos)))
ax6.set_yticklabels([repo.split('/')[-1][:20] for repo in top_repos.index], fontsize=9)
ax6.set_title('Top 10 Repositórios', fontweight='bold', fontsize=12)
ax6.set_xlabel('Número de PRs', fontsize=11)
ax6.invert_yaxis()
ax6.grid(axis='x', alpha=0.3)
for i, v in enumerate(top_repos.values):
    ax6.text(v + 1, i, str(v), va='center', fontsize=9)

plt.tight_layout()
plt.savefig('fig1_analise_exploratoria.png', dpi=300, bbox_inches='tight')
plt.show()

print(" Figura 1 gerada: fig1_analise_exploratoria.png")