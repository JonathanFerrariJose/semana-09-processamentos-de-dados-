# PREPROCESSAMENTO

## Tabela de Decisões

| Problema | Quantos | Decisão | Justificativa |
|-----------|----------|----------|---------------|
| Valores ausentes | Presentes em múltiplas colunas | Preenchimento com mediana e moda | Mantém a maior parte dos registros sem distorcer excessivamente a distribuição |
| Valores inválidos em idade_anos | Registros com valor -1 | Converter para ausente e imputar pela mediana do tipo | -1 não representa uma idade válida |
| Bairros com escrita inconsistente | Diversos registros | Padronização com strip() e title() | Evita categorias duplicadas |
| Registros duplicados | Encontrados na base | Remoção com drop_duplicates() | Evita contagem duplicada dos mesmos imóveis |
| Erros de negócio | Área > 600, preço < 50000 ou quartos > 10 | Remoção | Valores considerados inconsistentes para o domínio do problema |
| Preços atípicos | Identificados por IQR | Criação da coluna preco_atipico | Permite identificar extremos sem removê-los automaticamente |
| Variáveis numéricas | area_m2, quartos e idade_anos | StandardScaler | Coloca as colunas na mesma escala |
| Variáveis ordinais | condicao | OrdinalEncoder | Preserva a ordem natural das categorias |
| Variáveis nominais | tipo e bairro | OneHotEncoder | Evita criar relações artificiais entre categorias |
| Variáveis binárias | aceita_pet e mobiliado | Conversão Sim/Não para 1/0 | Facilita o processamento pelo modelo |
| Divisão treino/teste | 80% / 20% | train_test_split(random_state=42) | Permite reproduzir os resultados |
| Prevenção de vazamento | Transformações ajustadas apenas no treino | fit no treino e transform no teste | Garante avaliação correta do modelo |

## Possíveis Melhorias

Testar outras estratégias de detecção e tratamento de outliers, além de avaliar o impacto de diferentes escaladores e métodos de codificação no desempenho final do modelo.