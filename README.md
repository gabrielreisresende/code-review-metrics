# Lab03S02 - Caracterizando a Atividade de Code Review no GitHub
## Primeira Versão do Relatório Final

**Disciplina:** Laboratório de Experimentação de Software  
**Data:** 10 de Outubro de 2025  
**Dataset:** 3.816 Pull Requests de 168 repositórios populares do GitHub

---

## 1. Introdução

Este relatório apresenta a análise da atividade de code review em repositórios populares do GitHub, com foco em identificar variáveis que influenciam no merge de Pull Requests (PRs). O estudo analisa 3.816 PRs coletados de 168 repositórios, dos quais 83,4% foram aceitos (merged) e 16,6% foram rejeitados (closed).

### 1.1 Contexto do Dataset

O dataset foi construído seguindo os critérios metodológicos estabelecidos:
- **Repositórios analisados:** 168 repositórios populares do GitHub
- **Total de PRs:** 3.816 pull requests
- **Distribuição de status:**
  - Merged: 3.182 PRs (83,4%)
  - Closed: 634 PRs (16,6%)
- **Período de análise:** PRs com tempo de revisão superior a 1 hora
- **Critério de revisão:** Apenas PRs com pelo menos uma revisão humana

### 1.2 Limitações Identificadas

 **Observação importante:** Durante a análise exploratória, identificamos que as métricas de tamanho (additions, deletions e changed_files) apresentam valor zero para todos os PRs do dataset. Isso indica que essas métricas não foram coletadas adequadamente ou não estavam disponíveis na fonte de dados. Portanto, as análises relacionadas ao tamanho dos PRs (RQ01 e RQ05) **não poderão ser realizadas** com o dataset atual.

As métricas disponíveis para análise são:
- Tempo de análise (analysis_time_hours)
- Tamanho da descrição (description_length)
- Número de participantes (participants_count)
- Número de comentários (comments_count)
- Número de arquivos alterados (changed_files) - **não disponível**
- Linhas adicionadas (additions) - **não disponível**
- Linhas removidas (deletions) - **não disponível**

---

## 2. Hipóteses Iniciais

Com base na literatura sobre code review e nas práticas de desenvolvimento de software, formulamos as seguintes hipóteses para cada questão de pesquisa:

### Dimensão A: Feedback Final das Revisões (Status do PR)

#### **RQ01: Qual a relação entre o tamanho dos PRs e o feedback final das revisões?**

**Hipótese H1:** *PRs menores têm maior probabilidade de serem aceitos (merged) do que PRs maiores.*

**Justificativa:** PRs menores são mais fáceis de revisar, compreender e testar. Revisores tendem a aprovar mudanças incrementais e focadas, enquanto PRs grandes podem gerar sobrecarga cognitiva, aumentar o risco de defeitos e dificultar a identificação de problemas. Espera-se que PRs merged apresentem menor número de arquivos alterados e menor quantidade de linhas adicionadas/removidas em comparação com PRs closed.

**Status:**  **Não testável com o dataset atual** (métricas de tamanho não disponíveis)

---

#### **RQ02: Qual a relação entre o tempo de análise dos PRs e o feedback final das revisões?**

**Hipótese H2:** *PRs que são rejeitados (closed) levam mais tempo para serem analisados do que PRs aceitos (merged).*

**Justificativa:** PRs que eventualmente são rejeitados podem passar por múltiplas rodadas de discussão, tentativas de correção e debates sobre a adequação da mudança proposta. Esse processo iterativo e muitas vezes inconclusivo tende a prolongar o tempo de análise. Por outro lado, PRs bem elaborados e alinhados com os objetivos do projeto tendem a ser aprovados mais rapidamente. Espera-se que a mediana do tempo de análise seja significativamente maior para PRs closed.

**Expectativa quantitativa:** PRs closed devem apresentar tempo de análise pelo menos 2-3x maior que PRs merged.

---

#### **RQ03: Qual a relação entre a descrição dos PRs e o feedback final das revisões?**

**Hipótese H3:** *PRs com descrições mais detalhadas têm maior probabilidade de serem aceitos (merged).*

**Justificativa:** Uma descrição bem elaborada facilita o trabalho do revisor ao fornecer contexto, justificativa e explicação das mudanças propostas. Descrições claras e completas demonstram profissionalismo e cuidado do contribuidor, reduzindo a necessidade de esclarecimentos adicionais e aumentando a confiança do revisor na qualidade da contribuição. Espera-se que PRs merged apresentem descrições mais longas (maior número de caracteres) em comparação com PRs closed.

**Expectativa quantitativa:** PRs merged devem ter descrições 20-30% mais longas que PRs closed.

---

#### **RQ04: Qual a relação entre as interações nos PRs e o feedback final das revisões?**

**Hipótese H4:** *PRs rejeitados (closed) apresentam maior número de interações (participantes e comentários) do que PRs aceitos (merged).*

**Justificativa:** PRs problemáticos ou controversos tendem a gerar mais discussões, envolver mais pessoas e acumular mais comentários antes de serem rejeitados. Isso pode indicar desalinhamento com os objetivos do projeto, problemas técnicos complexos ou falta de consenso entre os mantenedores. Por outro lado, PRs bem elaborados podem ser aprovados com poucas interações. No entanto, é importante considerar que PRs muito complexos e bem-sucedidos também podem gerar muitas interações construtivas.

**Expectativa quantitativa:** PRs closed devem apresentar 30-50% mais comentários e participantes que PRs merged.

---

### Dimensão B: Número de Revisões

Para as questões RQ05-RQ08, que investigam a relação entre as métricas e o **número de revisões**, não temos essa informação disponível no dataset atual. O dataset contém apenas o status final (merged/closed) e não o número de revisões realizadas em cada PR.

**Observação:** As questões RQ05-RQ08 **não poderão ser respondidas** com o dataset atual, pois não há uma coluna específica indicando o número de revisões. Seria necessário coletar essa informação adicional da API do GitHub.

---

## 3. Metodologia

### 3.1 Coleta de Dados

O dataset foi construído a partir da API do GitHub, seguindo os critérios estabelecidos:

1. **Seleção de repositórios:**
   - 200 repositórios mais populares do GitHub
   - Mínimo de 100 PRs (merged + closed)

2. **Filtragem de PRs:**
   - Status: MERGED ou CLOSED
   - Pelo menos uma revisão registrada
   - Tempo de análise superior a 1 hora (para excluir revisões automáticas)

3. **Métricas coletadas:**
   - Tempo de análise (horas)
   - Tamanho da descrição (caracteres)
   - Número de participantes
   - Número de comentários
   - Status final (merged/closed)

### 3.2 Análise Estatística

Para responder às questões de pesquisa, utilizaremos:

1. **Estatísticas descritivas:** Medianas, quartis e distribuições
2. **Testes de correlação:** 
   - **Teste de Spearman** será utilizado como método principal
   - **Justificativa:** O teste de Spearman é não-paramétrico e adequado para:
     - Dados que não seguem distribuição normal
     - Relações monotônicas (não necessariamente lineares)
     - Presença de outliers (comum em métricas de software)
     - Variáveis ordinais ou contínuas

3. **Análise comparativa:** Comparação de medianas entre PRs merged e closed

### 3.3 Ferramentas

- **Linguagem:** Python 3.x
- **Bibliotecas:** pandas, numpy, matplotlib, seaborn, scipy

---

## 4. Análise Exploratória dos Dados

### 4.1 Estatísticas Gerais

**Medianas gerais (todos os PRs):**
- Tempo de análise: **46,70 horas** (~2 dias)
- Tamanho da descrição: **537 caracteres**
- Número de participantes: **2**
- Número de comentários: **3**

### 4.2 Comparação por Status

| Métrica | Merged (mediana) | Closed (mediana) | Diferença |
|---------|------------------|------------------|-----------|
| **Tempo de análise** | 33,59 horas | 216,49 horas | **+544,4%**  |
| **Tamanho da descrição** | 574 caracteres | 408 caracteres | **-29,0%** |
| **Número de participantes** | 2 | 2 | **0,0%** |
| **Número de comentários** | 3 | 3 | **0,0%** |

### 4.3 Observações Preliminares

1. **Tempo de análise:** PRs rejeitados levam **6,4x mais tempo** para serem analisados (216h vs 33h), confirmando fortemente a hipótese H2.

2. **Descrição:** Contrariando a hipótese H3, PRs rejeitados têm descrições **29% mais curtas** que PRs aceitos, sugerindo que descrições inadequadas podem contribuir para a rejeição.

3. **Interações:** As medianas de participantes e comentários são idênticas (2 e 3, respectivamente), não confirmando a hipótese H4 na análise de medianas. Será necessário análise mais aprofundada com testes estatísticos.

4. **Distribuição:** A alta taxa de aceitação (83,4%) indica que a maioria dos PRs submetidos aos repositórios populares são eventualmente aceitos, possivelmente devido a processos de triagem e qualidade dos contribuidores.

---

## 5. Próximos Passos (Lab03S03)

Para a próxima entrega, serão realizadas:

1. **Testes estatísticos de correlação** (Spearman) para todas as métricas disponíveis
2. **Análise de significância estatística** (p-valores)
3. **Visualizações avançadas:** scatter plots, heatmaps de correlação, distribuições
4. **Discussão aprofundada** comparando hipóteses iniciais com resultados obtidos
5. **Análise de outliers** e casos extremos
6. **Recomendações práticas** para desenvolvedores e revisores

---

## 6. Referências

- GitHub API Documentation: https://docs.github.com/en/rest
- Rigby, P. C., & Bird, C. (2013). Convergent contemporary software peer review practices. *Proceedings of the 2013 9th Joint Meeting on Foundations of Software Engineering*.
- Bacchelli, A., & Bird, C. (2013). Expectations, outcomes, and challenges of modern code review. *Proceedings of the 2013 International Conference on Software Engineering*.

---

## Apêndice A: Informações do Dataset

- **Arquivo:** `pull_requests_metrics.csv`
- **Total de registros:** 3.816 PRs
- **Repositórios únicos:** 168
- **Período de coleta:** Outubro de 2025
- **Colunas disponíveis:**
  - `pr_number`: Número do PR
  - `state`: Status (merged/closed)
  - `additions`: Linhas adicionadas  (não disponível)
  - `deletions`: Linhas removidas  (não disponível)
  - `changed_files`: Arquivos alterados  (não disponível)
  - `analysis_time_hours`: Tempo de análise em horas
  - `description_length`: Tamanho da descrição em caracteres
  - `participants_count`: Número de participantes
  - `comments_count`: Número de comentários
  - `repo`: Nome do repositório

### Top 10 Repositórios com Mais PRs

1. apache/dolphinscheduler - 73 PRs
2. grpc/grpc-java - 70 PRs
3. apache/skywalking - 69 PRs
4. jenkinsci/jenkins - 68 PRs
5. apolloconfig/apollo - 65 PRs
6. TeamNewPipe/NewPipe - 64 PRs
7. apache/incubator-seata - 63 PRs
8. questdb/questdb - 62 PRs
9. apache/zookeeper - 62 PRs
10. gyoogle/tech-interview-for-developer - 62 PRs

---
