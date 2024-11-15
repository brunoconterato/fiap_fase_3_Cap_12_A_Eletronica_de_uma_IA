# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# A Eletrônica de uma IA

## Sobre o grupo

## 👨‍🎓 Integrantes: 
- <a href="https://www.linkedin.com/in/brunoconterato">Bruno Conterato</a> 
- <a href="https://www.linkedin.com/in/willianpmarques">Willian Pinheiro Marques</a> 
- <a href="https://www.linkedin.com/in/robertobesser">Roberto Besser</a>
- <a href="https://www.linkedin.com/in/ludimila-vi">Ludimila Vitorino</a>

## 👩‍🏫 Professores:
### Tutor(a) 
- <a href="https://www.linkedin.com/in/lucas-gomes-moreira-15a8452a/">Lucas Gomes Moreira</a>
### Coordenador(a)
- <a href="https://www.linkedin.com/in/profandregodoi/">André Godoi</a>


## 📜 Descrição

O projeto consiste em um sistema de monitoramento e controle de irrigação para plantações, utilizando sensores para medir variáveis ambientais e controlar automaticamente o sistema de irrigação. A solução foi desenvolvida em duas etapas: inicialmente em MicroPython para prototipagem e testes em ambiente virtual, e posteriormente traduzida para C++ para otimizar desempenho e controle de hardware. A versão final, implementada em um microcontrolador simulado no Wokwi, utiliza sensores de umidade, temperatura, luz e movimento para ajustar a irrigação e disparar alertas de segurança. O sistema é capaz de monitorar continuamente a umidade do solo, a temperatura ambiente, o nível de água em reservatórios, a intensidade da luz solar e a presença de movimentos suspeitos em áreas delimitadas.

O projeto se propõe a otimizar o uso da água, reduzir o desperdício e garantir um ambiente seguro, além de melhorar as condições de cultivo. A plataforma oferece controle remoto e automatizado, permitindo que agricultores acompanhem as condições de suas plantações e gerenciem os recursos de forma eficiente.

Para mais informações, acesse:
- [Documentação do projeto](./document/ai_project_document_fiap.md)
- [Lógica de irrigação](./document/other/irrigation_logic.md)
- [Diagrama de conexão dos sensores](./document/other/sensor_diagram.md)
- [Código-fonte no Wokwi C++](https://wokwi.com/projects/414104064226887681)
- [[LEGADO] Código-fonte no Wokwi MicroPython](https://wokwi.com/projects/412840257175989249)


## 📁 Estrutura de pastas

O projeto está organizado em diversas pastas e arquivos, com o intuito de facilitar a organização e a manutenção do código. As pastas presentes no projeto são:

- **assets**: Contém imagens utilizadas no README.md.

- **document**: Documentação geral do projeto. A pasta possui dois arquivos, sendo um o principal:

    - **ai_project_document_fiap.md**: Documento central que descreve o projeto de forma completa, abrangendo desde a introdução até as conclusões, incluindo objetivos, metodologia, análise de resultados e trabalhos futuros.
    - **other**: Subpasta que contém arquivos complementares e menos importantes, que detalham aspectos específicos do projeto:
        - **irrigation_logic.md**: Documento que descreve a lógica de funcionamento do sistema de irrigação, detalhando os algoritmos e as decisões tomadas com base nas leituras dos sensores de umidade, luz e nível de água.
        - **prints_serial_monitor.md**: Documento que apresenta prints da tela do monitor serial do Wokwi, demonstrando como as informações dos sensores são exibidas e como o sistema responde às condições simuladas.
        - **security_logic.md**: Documento que detalha a lógica de funcionamento do sistema de segurança, explicando como o sensor de movimento PIR é utilizado para detectar invasões e como o sistema de alarme é acionado e desativado.
        - **sensor_diagram.md**: Documento que apresenta um diagrama da conexão dos sensores utilizados no projeto, mostrando como cada sensor é conectado ao microcontrolador e como os sinais são transmitidos e processados.

- **src**: Código-fonte do projeto, dividido em duas subpastas:

    - **CPP**: Versão final em C++ do código, utilizada para otimizar desempenho e controle de hardware.
        - **diagram.json**: Arquivo de configuração do Wokwi.
        - **libraries.txt**: Lista das bibliotecas utilizadas no projeto.
        - **sketch.ino**: Código-fonte principal do projeto em C++.
        - **wokwi-project.txt**: Arquivo de configuração do Wokwi.
    - **MicroPython**: Versão inicial em MicroPython, utilizada para prototipagem e testes em ambiente virtual.
        - **diagram.json**: Arquivo de configuração do Wokwi.
        - **main.py**: Código-fonte principal do projeto em Python.
        - **wokwi-project.txt**: Arquivo de configuração do Wokwi.

- **README.md**: Arquivo de documentação do projeto.



## 🔧 Como executar o código

Para testar o código, acesse o projeto no Wokwi clicando [aqui](https://wokwi.com/projects/414104064226887681).

No Wokwi, você poderá observar o funcionamento dos sensores, a lógica de controle de irrigação e o sistema de segurança. O monitor serial exibirá as informações dos sensores e as ações do sistema.

## 📋 Licença

<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/"><a property="dct:title" rel="cc:attributionURL" href="https://github.com/agodoi/template">MODELO GIT FIAP</a> por <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a> está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>

