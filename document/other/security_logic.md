## Lógica do sistema de segurança

O sistema de segurança é composto por um sensor PIR e um alarme sonoro. O sensor PIR detecta movimento e envia um sinal ao microcontrolador, que ativa o alarme em caso de detecção de movimento. O alarme é desativado automaticamente após 5 minutos sem detecções.

### Fluxograma do Sistema de Segurança

1. **Detecção de Movimento**: Verifica estado do sensor PIR.
2. **Acumulação de Detecções**: Acumula detecções em lista de histórico.
3. **Verificação de Limite**: Ativa alarme se detecções > 2 nos últimos 5 minutos.
4. **Desativação do Alarme**: Desativa após 5 minutos sem detecções.