# Bororo Sentence Generator

[![DOI](https://zenodo.org/badge/1382167262.svg)](https://doi.org/10.5281/zenodo.22941512)

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

A versão pública inclui:

- `src/bororo_generator/` — implementação do gerador e da avaliação;
- `scripts/` — utilitários de geração, diagnóstico, auditoria e avaliação;
- `tests/` — testes automatizados;
- `data/corbo/README.md` — documentação da relação com o CorBo;
- `docs/DATA_POLICY.md` — política de dados.

Dados documentais, análises linguísticas privadas, adjudicações humanas e dados gold experimentais não são distribuídos neste repositório.

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

A metodologia distingue explicitamente avaliação interna e avaliação held-out.

A validação interna verifica se o sistema realiza corretamente estruturas já representadas na gramática congelada. Ela demonstra **functional correctness** da pipeline e não deve ser interpretada como estimativa de desempenho em material não visto.

Um conjunto interno de 84 itens — 28 positivos, 28 negativos e 28 casos de fronteira — é usado para testar limites de decisão, cobertura e comportamento fail-closed. Como os casos derivam de fenômenos representados na gramática congelada, esse conjunto não constitui evidência independente de generalização.

A avaliação externa usa uma divisão por fonte documental. A gramática é construída apenas a partir da partição de desenvolvimento e congelada antes da avaliação das fontes held-out. Cobertura lexical e compatibilidade são medidas separadamente: predicados sem licença na gramática congelada ficam fora de cobertura e não são contados como erros.

Os materiais privados usados na revisão linguística e na adjudicação não fazem parte da distribuição pública do software.

## Uso

Instale o projeto em ambiente Python e execute os testes:

```bash
python3 -m pytest
```

Os utilitários em `scripts/` implementam as etapas públicas de geração, diagnóstico, auditoria e avaliação.

## Dados

**CorBo — Corpus da Língua Bororo**  
DOI: 10.5281/zenodo.12110451

Os dados documentais permanecem no repositório próprio do CorBo. Este projeto os utiliza como fonte externa e não substitui a documentação original.

## Citação do software

A versão citable atual é **v1.0.1**:

**Gerardi, Fabrício Ferraz. (2026). _Bororo Sentence Generator: Evidence-Bounded Generation for Boe-Bororo_ (v1.0.1). Zenodo. DOI: 10.5281/zenodo.22941512.**

## Estado

Projeto de pesquisa em desenvolvimento. As gramáticas experimentais são versionadas e congeladas por experimento para impedir que observações obtidas durante a avaliação alterem retrospectivamente as licenças usadas no mesmo teste.
