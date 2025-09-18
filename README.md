# Robô de envio via WhatsApp Web

Um robô que automatiza o envio de mensagens (texto e mídia) no WhatsApp Web para uma lista de clientes, usando um arquivo de dados e configurado por `config.ini`.

## Aviso de uso e licença
- Projeto de uso interno. Não possui licença pública.
- Não é permitida a utilização, distribuição ou cópia fora do ambiente interno sem autorização expressa do(s) responsável(is).
- Todos os direitos reservados.

## Como funciona (resumo)
- Você fornece um arquivo de dados com as colunas `UC`, `NOME`, `NUMTEL`, `NUMTEL2`.
- O robô abre o WhatsApp Web (no seu perfil do Chrome), busca cada contato pelo número e envia:
  - a mensagem definida em `config.ini` (permitindo placeholders) e
  - um arquivo (imagem/vídeo) se configurado.
- O status de cada envio é salvo de volta no arquivo de dados.

## Requisitos
- Windows
- Google Chrome instalado e logado no WhatsApp Web no perfil indicado (cache do Chrome)
- Python 3.11+ (recomendado 3.12/3.13)
- Pacotes Python (Selenium, pandas, python-dotenv, etc.)

## Instalação (PowerShell)
Crie e ative um ambiente virtual, depois instale as dependências:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Se você não possui um `requirements.txt`, instale os pacotes base:

```powershell
pip install selenium pandas python-dotenv
```

## Configuração
A configuração é feita por dois arquivos: `.env` (variáveis de ambiente) e `config.ini` (parâmetros de execução e conteúdo da mensagem).

### 1) .env
Defina no `.env` as variáveis para o caminho do arquivo de dados e do cache do Chrome usado pelo Selenium:

- `DATA_FILE`: caminho completo para a planilha/arquivo de contatos (xlsx, xls, csv ou txt)
- `CACHE_DRIVER_PATH`: caminho para a pasta de perfil do Chrome a ser usada pelo robô (deve estar logada no WhatsApp Web)

Exemplo:

```env
DATA_FILE=C:\\caminho\\para\\dados.xlsx
CACHE_DRIVER_PATH=C:\\caminho\\para\\perfil_chrome
```

Dicas:
- Para usar sua sessão do Chrome já logada no WhatsApp Web, aponte `CACHE_DRIVER_PATH` para uma pasta de perfil do Chrome (por exemplo, um diretório dedicado criado para este projeto). O robô inicia o Chrome com `--user-data-dir=<CACHE_DRIVER_PATH>`.
- Se `CACHE_DRIVER_PATH` apontar para um perfil sem WhatsApp logado, o WhatsApp Web pedirá autenticação no primeiro uso.

### 2) config.ini
Defina o conteúdo da mensagem, mídia e opções do robô.

Campos suportados:

```ini
[USER]
name = SeuNomeOpcional

[MESSAGE]
# Caminho completo para a mídia (imagem/vídeo). Deixe em branco se não quiser enviar arquivo.
image_path = C:\\caminho\\para\\arquivo.mp4

# Texto da mensagem. Placeholders disponíveis:
#   {cliente} -> substituído pelo valor da coluna NOME
#   {unidade_consumidora} -> substituído pelo valor da coluna UC
# Para quebras de linha, use ponto e vírgula ';' entre as linhas.
text = Olá {cliente};Sua UC é {unidade_consumidora};Mensagem de teste.

[SETTINGS]
# Pasta onde serão salvos os logs (será criada se não existir)
log_path = C:\\caminho\\para\\logs

# Executar o navegador sem interface (True/False). False para ver o navegador abrindo.
headless = False
```

Observações sobre `MESSAGE.text`:
- O robô aceita `;` como separador de linhas. Cada `;` vira uma quebra de linha no WhatsApp.
- Os placeholders `{cliente}` e `{unidade_consumidora}` são preenchidos a partir do arquivo de dados.

## Arquivo de dados
O arquivo indicado em `DATA_FILE` deve conter, obrigatoriamente, as colunas:
- `UC` (número)
- `NOME` (texto)
- `NUMTEL` (número)
- `NUMTEL2` (número)

Regras e tratamento aplicados:
- Linhas totalmente vazias são removidas.
- `NUMTEL` e `NUMTEL2` com vazio viram `0` e são convertidos para inteiro.
- Números na lista de exclusão `[0, 83900000000, 83999999999]` são ignorados.
- A mensagem é enviada primeiro para `NUMTEL`; se não der, tenta `NUMTEL2`.
- O status é salvo de volta no arquivo original (coluna `Status`) com valores `Entregue` ou `Não encontrado`.

Formatos suportados: `xlsx`, `xls`, `csv` (separador `;`) e `txt` (tabulado).

## Execução
Após configurar `.env` e `config.ini`, execute o robô:

```powershell
python .\main.py
```

Comportamento durante a execução:
- O Chrome é iniciado usando o perfil em `CACHE_DRIVER_PATH`.
- O WhatsApp Web é aberto. Se necessário, autentique-se.
- Para cada cliente da lista, o robô busca o número, envia a mensagem e a mídia (`MESSAGE.image_path`, se informada como arquivo válido). No código atual, o modo de envio de arquivo está definido para `video` por padrão.
- Intervalos aleatórios curtos são aplicados entre ações para parecer humano.

Interromper com segurança:
- Pressione `Ctrl + C` no terminal. O robô tenta salvar o progresso e finalizar.

## Logs e saída
- Os logs são gravados na pasta definida em `SETTINGS.log_path`:
  - `app.log`: informações gerais da execução
  - `error.log`: erros ocorridos
- Mensagens também aparecem no console.

## Solução de problemas
- "Diretório inválido" ao ler dados: verifique `DATA_FILE` no `.env` e se o arquivo existe e não está aberto por outro programa.
- Planilha sem colunas esperadas: confirme que `UC`, `NOME`, `NUMTEL`, `NUMTEL2` existem com exatamente esses nomes.
- WhatsApp não encontra o número: o robô registra como `Não encontrado` e prossegue; revise o DDD/país.
- Precisar apenas texto (sem mídia): deixe `MESSAGE.image_path` vazio, ou ajuste o código para não chamar `send_file` quando vazio.
- Headless sem interface: defina `headless = True` em `[SETTINGS]`. Se houver problemas de login no WhatsApp, use `False` temporariamente.

## Notas técnicas
- Versão do app: `0.0.5` (definida em código)
- O Chrome é iniciado com a opção `--user-data-dir=<CACHE_DRIVER_PATH>`
- Placeholders de mensagem são formatados via `str.format` no momento do envio.
- O separador de linhas `;` é convertido para quebras de linha reais.

---
Dúvidas ou melhorias? Abra um issue interno ou ajuste o `config.ini` conforme sua necessidade.