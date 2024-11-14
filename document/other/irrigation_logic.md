## Lógica de Irrigação

### 1. Influência dos Componentes no Controle de Irrigação

O sistema de controle de irrigação considera três componentes principais — **Umidade do Solo**, **Nível de Água no Reservatório** e **Luminosidade** — para determinar a necessidade e intensidade da irrigação. Cada componente tem uma lógica específica de influência sobre o processo, conforme detalhado a seguir:

#### 1.1. Umidade do Solo

A **umidade do solo** é o principal indicador de necessidade de irrigação:
- **Baixa Umidade**: Quando o solo apresenta baixa umidade, a irrigação é necessária e ativada em diferentes intensidades, dependendo dos outros fatores (reservatório e luminosidade).
- **Umidade Moderada**: Quando a umidade é moderada, o solo ainda pode se beneficiar de irrigação, mas de forma mais controlada, variando entre fluxos leve e moderado, de acordo com a luminosidade.
- **Alta Umidade**: Quando a umidade do solo está alta, a irrigação é completamente desativada, independentemente das condições de luminosidade ou nível de água, para evitar saturação e desperdício.

#### 1.2. Nível de Água no Reservatório

O **nível de água no reservatório** influencia diretamente a sustentabilidade do sistema, ajustando o fluxo de irrigação para economizar água quando necessário:
- **Reservatório Cheio**: Permite fluxos de irrigação mais intensos, incluindo forte e moderado, dependendo das condições de umidade e luminosidade.
- **Reservatório Médio**: Promove a conservação, restringindo o fluxo a leve ou moderado, mesmo quando a umidade é baixa, para preservar água.
- **Reservatório Baixo**: Quando o nível de água está baixo, a irrigação é automaticamente desativada, independentemente de outros fatores, para priorizar a conservação do recurso hídrico.

#### 1.3. Luminosidade

A **luminosidade** afeta a intensidade da irrigação ao considerar as taxas de evaporação e a necessidade de água pelas plantas:
- **Alta Luminosidade**: Condições de alta luz, associadas a maior evaporação e maior necessidade de água pelas plantas, permitem fluxos mais intensos (forte ou moderado), conforme o nível de umidade e a disponibilidade de água no reservatório.
- **Luminosidade Moderada**: A luz moderada requer irrigação menos intensa, favorecendo o uso de fluxo moderado ou leve, considerando também a umidade e o nível de água.
- **Baixa Luminosidade**: Em condições de baixa luminosidade, o risco de evaporação é menor, e o sistema utiliza fluxo leve ou desativa a irrigação (caso a umidade seja alta ou o reservatório esteja em nível baixo).

Esses componentes trabalham em conjunto para otimizar o uso da água, garantindo que a irrigação seja fornecida na quantidade adequada com base nas condições de umidade do solo, nível de água disponível e intensidade de luz solar. Essa abordagem equilibrada permite uma irrigação eficiente e adaptada às condições reais de necessidade e disponibilidade de recursos.

#### 2. Regras de Irrigação

- **Baixa umidade e reservatório cheio**:
    - Inicia a irrigação com fluxo **forte** se a luminosidade for alta.
    - Inicia a irrigação com fluxo **moderado** se a luminosidade for moderada.
    - Inicia a irrigação com fluxo **leve** se a luminosidade for baixa.
- **Baixa umidade e reservatório médio**:
    - Inicia a irrigação com fluxo **moderado** quando a luminosidade é alta.
    - Inicia a irrigação com fluxo **leve** quando a luminosidade é moderada ou baixa.
- **Umidade moderada e reservatório médio ou cheio**:
    - Inicia a irrigação com fluxo **leve** se a luminosidade for baixa.
    - Inicia a irrigação com fluxo **moderado** se a luminosidade for moderada ou alta.
- **Alta umidade ou nível de água baixo**:
    - A irrigação é desativada independentemente das outras condições.

Essa lógica cumpre a nova tabela e permite um controle mais eficiente de irrigação ajustado ao nível médio do reservatório.

#### 3. Tabela de Decisão de Irrigação

| Umidade (U) | Nível de Água (N)        | Luminosidade (L)    | Ação                                |
|-------------|--------------------------|----------------------|-------------------------------------|
| Baixa       | Cheio                    | Alta                | Iniciar irrigação com fluxo forte   |
| Baixa       | Cheio                    | Moderada            | Iniciar irrigação com fluxo moderado|
| Baixa       | Cheio                    | Baixa               | Iniciar irrigação com fluxo leve    |
| Baixa       | Médio                    | Alta                | Iniciar irrigação com fluxo moderado|
| Baixa       | Médio                    | Moderada ou Baixa   | Iniciar irrigação com fluxo leve    |
| Moderada    | Cheio ou Médio           | Alta ou Moderada    | Iniciar irrigação com fluxo moderado|
| Moderada    | Cheio ou Médio           | Baixa               | Iniciar irrigação com fluxo leve    |
| Alta        | Qualquer nível           | Qualquer nível      | Parar irrigação                     |
| Qualquer    | Baixo                    | Qualquer nível      | Parar irrigação (preservar água)    |

