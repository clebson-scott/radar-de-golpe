# Radar de Golpe — case de validação (Product Discovery)

> Veredito em minutos para mensagens suspeitas de WhatsApp/PIX: **cole a mensagem, receba GOLPE / SUSPEITO / SEGURO — com o motivo.**

## O problema
Golpes por WhatsApp e PIX (falso parente, boleto falso, falso atendente) exploram um momento emocional e solitário: a pessoa precisa decidir em segundos e não tem com quem verificar. Campanhas de conscientização chegam antes do evento — na hora da decisão, ninguém ajuda.

## A validação (não se constrói antes de validar)
- **Método:** MVP Concierge — o serviço entregue manualmente (análise assistida por IA com revisão humana) atrás de uma fachada de produto real.
- **Artefatos reais:** [landing page](https://clebson-scott.github.io/radar-de-golpe/) com formulário de validação em produção; [trabalho acadêmico completo](https://clebson-scott.github.io/radar-de-golpe/trabalho.html).
- **3 hipóteses testáveis** com metas numéricas e **critérios de decisão pré-registrados** (perseverar / ajustar / pivotar / abandonar) definidos **antes** da coleta, para eliminar viés de confirmação.
- **5 respostas reais** coletadas em 24h; cada mensagem suspeita submetida recebeu veredito por e-mail — o produto funcionando antes de existir.

## Resultados (n=5)
| Métrica | Meta | Resultado |
|---|---|---|
| % que recebe golpes (6m) | ≥60% | **100%** |
| Intenção de uso (0–10) | ≥7 | **7,2** |
| Confiança no veredito (0–10) | ≥6 | **6,0** |
| Pagaria R$5/mês (sim+talvez) | ≥30% | **60%** |
| NPS familiar (0–10) | ≥7 | **8,6** |
| Mensagens reais analisadas | ≥3 | **4** |

**Achado central:** a confiança no veredito não depende da frequência de golpes recebidos — depende de já ter sido vítima (vítima real: 10/10; nunca caiu: 1/10). O go-to-market começa pelo público já vitimado; confiança é a métrica crítica da próxima iteração.

## Decisão: ✅ PERSEVERAR
Acionada pelos critérios pré-registrados (uso 7,2 ≥ 7 · NPS 8,6 ≥ 7 · 4 mensagens ≥ 3). Próximo passo: protótipo automatizado no WhatsApp com foco em sinal de autoridade.

## Estrutura deste repositório
- `index.html` — landing page de validação (deploy: GitHub Pages)
- `trabalho.html` — trabalho acadêmico completo (metodologia, canvases, resultados, decisão, anexos)
- `analise.py` — pipeline de tabulação das respostas e acionamento dos critérios de decisão

## Transparência de uso de IA
IA foi utilizada como ferramenta assistida (scaffolding, tabulação e análise de mensagens com revisão humana). As decisões de produto e toda a coleta com usuários reais são do autor. A IA não validou o mercado — as pessoas reais validaram.

*Clebson Scott · UniFECAF · Metodologias Ágeis, Geais e Validação de Produtos · Out/2026*
