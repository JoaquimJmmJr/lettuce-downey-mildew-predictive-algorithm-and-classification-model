# Algoritmo preditivo de combate ao Míldio (Bremia lactucae) do alface
Sistema de antecipação de ocorrência de doenças com base em variáveis ambientais e validação visual dos primeiros sintomas, permitindo intervenção precoce e redução do uso de insumos. O modelo inicial é baseado em conhecimento agronômico e evolui continuamente com dados reais coletados pelo robô.

**Objetivo**: Ajudar no combate preventivo ao Míldio (_Bremia lactucae_), uma das doenças mais destrutivas e uma das maiores ameaças na cultura da alface, favorecida por:
- alta umidade relativa (> 90%)
- temperaturas amenas (10–20 °C)
- período prolongado de exposição (≥ 6 horas)

O sistema identifica condições ambientais favoráveis à doença antes do surgimento visível dos sintomas.

**Observações**: Para esse problema específico, um modelo de ML não é obrigatório. Com base no que a literatura agronômica descreve para o Míldio (_Bremia lactucae_), um sistema determinístico baseado em regras + janela temporal já entrega um resultado sólido, confiável, explicável, interpretável e defendível.

> Optamos por um modelo determinístico baseado em regras agronômicas e análise temporal contínua, priorizando interpretabilidade e confiabilidade. O sistema pode evoluir futuramente para aprendizado de máquina (exemplo: regressão ou árvores de decisão) com dados reais.

## 🏗️ Arquitetura do sistema
```
ESP32 → envia dados → Supabase (tabela temporal)
                         ↓
                 Script Python (a cada 30 min)
                         ↓
                 Calcula risco
                         ↓
                 Salva resultado / dashboard
```

## 🔁 Fluxo de funcionamento
1. Sensores coletam dados ambientais
2. Dados são enviados ao banco (Supabase)
3. Script Python:
   - lê últimas 24h
   - identifica condições críticas
   - calcula blocos contínuos
4. Sistema classifica o risco
5. Resultado pode ser:
   - exibido em dashboard
   - usado para acionar ações no robô

## 🧠 Lógica do modelo
O sistema calcula o risco com base em **condições ambientais contínuas ao longo do tempo**.
### Regra principal (Míldio):
```
Se:
umidade relativa > 90%
E temperatura entre 10–20 °C
Por um período contínuo ≥ 6 horas

→ RISCO ALTO
```
> **Fontes:**
>
> (N.d.). Bayer.com. Retrieved May 5, 2026, from https://www.vegetables.bayer.com/ca/en-ca/resources/agronomic-spotlights/lettuce-downy-mildew.html
>
> INSTITUTO BIOLÓGICO - Guia de Sanidade Vegetal - Versão: 1.0 : (n.d.). Bio.Br. Retrieved May 5, 2026, from https://www.sica.bio.br/guiabiologico/busca_culturas_resultado_ok.php?Id=13&Vlt=3

### Classificação de risco
| Condição                           | Risco    |
| ---------------------------------- | -------- |
| ≥ 6h contínuas em condição crítica | 🔴 Alto  |
| 3h – 6h                            | 🟡 Médio |
| < 3h                               | 🟢 Baixo |

### Janela temporal
- A análise é baseada nas últimas 24 horas (`df[col_ts].max() - pd.Timedelta(hours=24)`)
- Cálculo executado a cada 30 minutos (`intervalo_min = 30`)
### Estrutura dos dados
Formato da tabela (CSV ou banco):
```
timestamp,temp,umidade,solo
2026-04-25 00:00:00,18,92,65
2026-04-25 00:30:00,17,94,66
```
#### Campos:
- `timestamp`: data e hora da leitura
- `temp`: temperatura (°C)
- `umidade`: umidade relativa (%)
- `solo`: umidade do solo (%

## 🖥️ Tecnologias utilizadas
| Camada | Tecnologia |
|---|---|
| Backend / processamento | Python (Pandas + Numpy) |

### Implementações futuras:
| Hardware (IoT) | ESP32 + Sensores de temperatura e umidade |
|---|---|
| Banco de dados | Supabase (PostgreSQL) |
| Visualização   | Streamlit |
## ⚙️ Como executar o projeto
### 1. Clonar o repositório
```
git clone <repo>
cd <repo>
```
### 2. Instalar dependências
```
pip install pandas numpy
```
### 3. Utilize um dataset de teste
Utilize ou crie um arquivo `dados_sensores.csv` com o seguinte formato:
```
timestamp,temp,umidade,solo
2026-04-25 00:00:00,18,92,65
2026-04-25 00:30:00,17,94,66
...
```
#### Recomendado:
- Intervalo de 30 minutos
- 2 a 5 dias de dados
- Incluir períodos com alta umidade (>90%)

### 4. Executar o script
```
python algoritmo-previsao-mildio-pandas.py
```
### 5. Saída esperada
```
Horas contínuas em condição crítica: 6.5h
Nível de risco de Míldio: ALTO 🔴
```
## 🔬 Contribuição científica
Este projeto demonstra que:

- conhecimento agronômico pode ser traduzido em algoritmos
- sistemas simples podem gerar alto impacto
- prevenção baseada em dados podem reduz uso de defensivos

## 💡 Melhorias futuras
- Regressão logística para calcular a probabilidade de cada nível de risco e não ficar preso a regras rígidas
- Random Forest: funciona bem com poucos dados de treinamento e aprende padrões não óbvios 
- Modelos preditivos com séries temporais (LSTM) para aprender ao longo do tempo (projeto avançado)
- Inclusão de outras doenças:
    - mofo branco
    - mancha bacteriana
- Mapa de calor da plantação
- Histórico de risco
- Alertas em tempo real