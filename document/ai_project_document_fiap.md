
<img src="../assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=30% height=30%>

# AI Project Document - Módulo 1 - FIAP

**_Os trechos em itálico servem apenas como guia para o preenchimento da seção. Por esse motivo, não devem fazer parte da documentação final_**

## Nome do Grupo

#### Nomes dos integrantes do grupo



## Sumário

[1. Introdução](#c1)

[2. Visão Geral do Projeto](#c2)

[3. Desenvolvimento do Projeto](#c3)

[4. Resultados e Avaliações](#c4)

[5. Conclusões e Trabalhos Futuros](#c5)

[6. Referências](#c6)

[Anexos](#c7)

<br>

# <a name="c1"></a>1. Introdução

## 1.1. Escopo do Projeto

### 1.1.1. Contexto da Inteligência Artificial

A Inteligência Artificial (IA) vem transformando várias indústrias com soluções que automatizam processos, aprimoram a eficiência e fornecem insights avançados por meio de algoritmos de aprendizado de máquina e análise de dados em tempo real. No setor agrícola, a IA permite monitorar variáveis ambientais críticas como umidade, luz e movimento, auxiliando produtores rurais no gerenciamento e otimização de recursos. A aplicação de IA no agronegócio possui abrangência internacional, pois auxilia tanto pequenos agricultores quanto grandes propriedades a reduzir custos e maximizar a produção por meio da agricultura de precisão.

### 1.1.2. Descrição da Solução Desenvolvida

Este projeto desenvolve uma aplicação de monitoramento agrícola inteligente que utiliza sensores (DHT22 para umidade e temperatura, HC-SR04 para nível de água, PIR para detecção de movimento e LDR para luminosidade). A solução visa auxiliar no controle de irrigação e segurança de áreas agrícolas. Através da coleta e análise de dados ambientais, o sistema toma decisões automáticas para ativar ou desativar a irrigação com base em condições de umidade, luminosidade e níveis de água, além de disparar alertas em caso de detecção de movimento suspeito. A solução proporciona valor ao cliente ao garantir o uso eficiente da água, aumentar a segurança e melhorar as condições de cultivo.

# <a name="c2"></a>2. Visão Geral do Projeto

## 2.1. Objetivos do Projeto

O objetivo do projeto é criar um sistema autônomo de monitoramento agrícola que otimize o uso da água e promova a segurança do ambiente monitorado. Especificamente, o sistema busca ajustar a intensidade da irrigação com base em leituras de sensores ambientais e identificar possíveis invasões por meio da detecção de movimento. Com isso, o projeto pretende reduzir o desperdício de água, garantir melhores condições de cultivo e promover uma maior segurança no local.

## 2.2. Público-Alvo

O público-alvo deste projeto são produtores rurais e gestores de propriedades agrícolas que desejam adotar práticas mais sustentáveis e automatizadas na gestão de recursos hídricos e segurança. A solução também se aplica a pequenas e médias empresas agrícolas e até mesmo para quem faz cultivo em estufas, que se beneficiariam de um monitoramento contínuo e uma irrigação controlada.

## 2.3. Metodologia

A metodologia para o desenvolvimento do projeto foi estruturada em várias etapas:

1.  **Levantamento de Requisitos**: Os sensores necessários e parâmetros de monitoramento ambiental (umidade, luz, movimento e nível de água) já foram previamente indicados na descrição da atividade.
    
2.  **Desenvolvimento do Código**: Implementação em Python para leitura de sensores e lógica de controle dos sistemas de irrigação e alarme de movimento.
    
3.  **Simulação no Wokwi**: Testes dos sensores e ajustes do código foram feitos em ambiente simulado no Wokwi, onde foi possível avaliar o funcionamento da lógica de controle de irrigação e alarme.
    
4.  **Testes e Avaliação**: Realização de ciclos de teste para validar a leitura de sensores e decisões do sistema, verificando se as ações tomadas pelo sistema correspondem às condições simuladas.
    
5.  **Ajustes Finais**: Refinamento do código e ajustes nas variáveis de controle e limites de atuação dos sensores para otimizar o funcionamento da solução.

Aqui está a documentação com as seções preenchidas com base no código fornecido:

---

# <a name="c3"></a>3. Desenvolvimento do Projeto

## 3.1. Tecnologias Utilizadas

O desenvolvimento do projeto utilizou as seguintes tecnologias, ferramentas e bibliotecas:

- **Python**: Linguagem de programação utilizada para desenvolver a lógica de monitoramento e controle do sistema.
- **Biblioteca `dht`**: Para integração com o sensor DHT22, utilizado para medir temperatura e umidade.
- **Biblioteca `machine`**: Utilizada para manipulação de pinos do microcontrolador, possibilitando a leitura de sensores.
- **Biblioteca `time`**: Para controle de intervalos de tempo e registro do tempo de resposta dos sensores.
- **Ambiente de Simulação Wokwi**: Plataforma utilizada para simular o comportamento dos sensores e testar o código em ambiente virtual.
- **Sensores**:
  - **DHT22**: Sensor de temperatura e umidade.
  - **HC-SR04**: Sensor ultrassônico para medir o nível de água.
  - **PIR**: Sensor de movimento infravermelho passivo.
  - **LDR**: Sensor de luminosidade para captar a intensidade da luz.

## 3.2. Modelagem e Algoritmos

O projeto utiliza algoritmos de tomada de decisão baseados em regras lógicas e condicionais, que controlam a ativação e intensidade do sistema de irrigação, além de disparar alertas de segurança. Os algoritmos de controle incluem:

- **Algoritmo de Irrigação**: Analisa três variáveis principais (umidade do solo, nível do reservatório e intensidade da luz) para decidir a intensidade da irrigação. A lógica de controle considera a umidade baixa ou moderada, intensidade da luz e nível do reservatório para ajustar automaticamente o nível da irrigação entre leve, moderada ou forte. Se a umidade for alta ou o reservatório estiver com nível baixo, a irrigação é desativada para evitar desperdício.
  
- **Algoritmo de Segurança**: Utiliza o sensor PIR para detectar movimentos e acumular dados de detecção ao longo de um intervalo de cinco minutos. Se mais de duas detecções forem registradas em cinco minutos, um alerta de invasão é ativado. Caso não haja detecção por cinco minutos consecutivos, o sistema automaticamente desativa o alarme, indicando área segura.

Esses algoritmos foram escolhidos por sua simplicidade e efetividade na modelagem de sistemas de decisão baseados em condições de monitoramento ambiental, proporcionando um controle eficiente e preciso para o sistema agrícola.

## 3.3. Treinamento e Teste

Como o projeto não utiliza modelos de IA treináveis, mas sim um sistema de regras determinísticas, não houve necessidade de treinamento. Em vez disso, foram realizados testes intensivos no ambiente de simulação Wokwi para ajustar limites de decisão e avaliar o desempenho. Os testes incluíram:

- **Avaliação de Limites de Umidade e Luminosidade**: Testes para ajustar os valores que ativam ou desativam os níveis de irrigação.
- **Teste de Detecção de Movimento**: Testes para validar a lógica de invasão com o sensor PIR, verificando o acionamento do alarme após múltiplas detecções em cinco minutos.
  
Os resultados foram ajustados para refletir as condições ideais de umidade e luminosidade para ativação dos sistemas de irrigação e segurança, garantindo a efetividade do monitoramento sem necessidade de ajustes adicionais.

# <a name="c4"></a>4. Resultados e Avaliações

## 4.1. Análise dos Resultados

Os resultados mostraram que o sistema responde adequadamente às condições ambientais, ajustando a intensidade da irrigação e disparando alertas de invasão conforme esperado. Em relação aos objetivos, o sistema demonstrou eficiência no controle da irrigação e segurança, atendendo a cenários simulados de baixa umidade, diferentes níveis de reservatório e intensidade de luz, além de detectar movimento com precisão. Algumas divergências ocorreram em leituras de luminosidade, possivelmente devido à variação na calibração do sensor LDR, mas foram ajustadas para otimizar a precisão.

## 4.2. Feedback dos Usuários

Durante a fase de testes no ambiente Wokwi, o sistema não chegou a ser testado com sensores reais nem em produção. No entanto, os testes realizados pelos membros da equipe indicaram que:

- O sistema de alarme foi eficaz e gerou alertas adequados para movimentos detectados.
- A lógica de irrigação foi considerada intuitiva e eficiente, e uma recomendação foi integrar sensores de umidade do solo diretamente para um controle ainda mais preciso.

Esses testes mostraram que os sistemas são promissores em atender as demandas de agricultores reais.

# <a name="c5"></a>5. Conclusões e Trabalhos Futuros

A solução desenvolvida cumpriu os objetivos principais de monitorar variáveis ambientais e ajustar automaticamente o sistema de irrigação e segurança para otimizar o uso de água e proteger o ambiente. Os principais pontos fortes foram a precisão dos alertas de segurança e a adaptação da irrigação a diferentes condições de luz e umidade.

Para futuras melhorias, recomenda-se:

- **Integração de Sensores de Umidade do Solo**: Para uma avaliação mais direta das condições de irrigação.
- **Notificação Remota**: Implementação de alertas via SMS ou aplicativo para notificar o usuário sobre detecções e estado da irrigação em tempo real.
- **Aprendizado de Máquina**: Evoluir o projeto com um modelo preditivo que sugira condições de irrigação baseadas em padrões históricos, otimizando o uso de recursos ao longo do tempo.

# <a name="c6"></a>6. Referências

- Documentação oficial do [Wokwi](https://docs.wokwi.com/pt-BR/)
- [Wokwi IoT Simulation Platform](https://wokwi.com)
- Manuais técnicos dos sensores: [DHT22](https://docs.wokwi.com/pt-BR/parts/wokwi-dht22/), [HC-SR04](https://docs.wokwi.com/pt-BR/parts/wokwi-hc-sr04/), [PIR](https://docs.wokwi.com/pt-BR/parts/wokwi-pir-motion-sensor/) e [LDR](https://docs.wokwi.com/pt-BR/parts/wokwi-photoresistor-sensor/).
- [Projeto usando sensor LDR](https://wokwi.com/projects/372429832828226561) usado como referência para os cálculos (agradecimentos aos autores do projeto!).

# <a name="c7"></a>Anexos

### 7.1. Ver o [Diagrama de conexão dos sensores](./other/sensor_diagram.md)

### 7.2. Ver a [Lógica de irrigação](./other/irrigation_logic.md)


### 7.3. Ver a [Lógica de segurança](./other/security_logic.md)
