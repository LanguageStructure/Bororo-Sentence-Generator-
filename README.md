# Bororo Sentence Generator

Gerador experimental de sentenças em **Boe-Bororo**, desenvolvido a partir do **CorBo — Corpus da Língua Bororo**.

O projeto implementa uma arquitetura de **evidence-bounded generation**: evidência de corpus, análise linguística humana, licença gramatical, geração e atestação posterior são mantidas como camadas distintas. Uma forma encontrada no corpus não se torna automaticamente uma regra produtiva, e ausência no corpus não é interpretada como agramaticalidade.

## Princípio

O fluxo central é:

```text
CorBo
  → corpus evidence
  → human linguistic review
  → reviewed grammar
  → controlled generator
  → generated candidate
  → validation / corpus attestation
```

Somente análises explicitamente revisadas podem criar licenças de geração. Casos incertos permanecem incertos em vez de serem completados por analogia.

## Componentes

- `src/bororo_generator/` — implementação do gerador e da avaliação;
- `config/` — configurações e inventários linguísticos versionados;
- `scripts/` — construção de dados, auditoria e experimentos reproduzíveis;
- `tests/` — testes automatizados;
- `data/corbo/` — dados experimentais derivados/selecionados do CorBo;
- `reports/` — resultados e manifests dos experimentos;
- `docs/` — documentação técnica.

## Gramática revisada

As licenças distinguem evidência lexical, morfológica e construcional. Entre outras coisas, o sistema mantém separados:

- paradigmas ou classes de radical explicitamente revisados;
- células de pessoa individualmente revisadas;
- quadros de valência;
- construções específicas;
- restrições morfotáticas;
- atestação de corpus.

A atestação posterior de uma forma gerada é evidência observacional, não uma atualização automática da gramática.

## Avaliação

O repositório contém avaliações internas e uma avaliação com divisão por fonte documental.

A validação interna verifica se o sistema realiza corretamente estruturas já representadas na gramática congelada. Ela demonstra **functional correctness** da pipeline e não deve ser interpretada como estimativa de desempenho em material não visto.

Para avaliar generalização, uma versão posterior da gramática é construída apenas a partir de uma partição de desenvolvimento do corpus e congelada antes da abertura das fontes reservadas para teste. Cobertura lexical e compatibilidade no conjunto held-out são medidas separadamente: predicados sem licença na gramática congelada são considerados fora de cobertura, não erros.

Os scripts, manifests e relatórios necessários para reproduzir essas etapas permanecem no repositório.

## Uso

Instale o projeto em ambiente Python e execute os testes:

```bash
python3 -m pytest
```

Os scripts em `scripts/` documentam as etapas específicas de construção dos conjuntos experimentais, geração, auditoria e avaliação.

## Dados

**CorBo — Corpus da Língua Bororo**  
DOI: 10.5281/zenodo.12110451

Os dados documentais permanecem no repositório próprio do CorBo. Este projeto os utiliza como fonte externa e não substitui a documentação original.

## Estado

Projeto de pesquisa em desenvolvimento. As gramáticas experimentais são versionadas e congeladas por experimento para impedir que observações obtidas durante a avaliação alterem retrospectivamente as licenças usadas no mesmo teste.
