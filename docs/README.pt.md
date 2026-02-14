<div align="center">
  <a href="../README.md">🇺🇸 English</a> |
  <a href="README.pt.md">🇧🇷 Português</a> |
  <a href="README.ja.md">🇯🇵 日本語</a>
</div>

---

# 🎹 Teclado Sinestésico

![App Screenshot](assets/screenshot.png)

Um teclado virtual para pessoas pequenas com sinestesia grafema-cor.

Tem um jogo com cartas de baralho chamado 7-5-3: basicamente, quando aparecem essas cartas você tem que pegá-las. Outro dia brincando disso com minha filha, estranhei ela tentando pegar o 2 por algumas vezes. Fiz uma explicação rasa sobre a diferença de ambos e fui lavar a louça. Então ela volta com o caderno de desenho com os números 7 (amarelo) , 5 (verde), 3 (azul) e 2 (vermelho) pintados e me explica que confunde o 5 de ouro e de copas com o 2 porque o 2 é vermelho. Eu fiz cara de interrogação, já a minha parceira fez cara de exclamação e com entusiasmo explica que é sinestesia: lembrei dos meus tempos de faculdade quando ainda restava criatividade para ilustrar paisagens em resposta ao sabor das coisas.

Aproveitando que eu tinha que criar alguma aplicação utilizando o conhecimento de programação recém-adquirido, resolvi criar um aplicativo para mapear as cores das letras segundo o seu olhar. Como parece ser um fenômeno comum, resolvi disponibilizar o código e os dados a quem possa interessar. Espero que ajude as pessoas a se sintonizarem pelo menos 3 quarks de distância.


## ✨ Funcionalidades

Basicamente é um teclado com os caracteres alfanuméricos e o silabário japonês com dois modos. No modo "cores", é possível definir uma cor para cada caracter.
No modo "escrever" é possível redigir um breve texto utilizando o teclado personalizado. Para todo o processo não ficar tão enfadonho, inseri um botão para tocar um som de fundo e outro botão para mudar a configuração de cor da interface. A carta, para não ficar insossa, dá para trocar o papel de fundo e finalizar a decoração com adesivos. Com a carta finalizada, pressione "ver" para ver o resultado final, e sendo do agrado é só fazer o download.

* **🎨 Escolha de cores:** a ideia inicial era fazer um círculo com todas as cores em degradê para que a escolha fosse mais livre, mas acabei optando por uma versão mais simples com seleção direta das cores. Usei como referência para as cores a paleta de [cores tradicionais do Japão](https://www.colordic.org/w): sobre cada cor aparece o respectivo nome.

* **🔉 Som dos caracteres:** optei por usar um aplicativo ([VOICEVOX](https://voicevox.hiroshiba.jp/)) para gerar os sons dos caracteres. Se você precisa de controle refinado sobre cada consoante e vogal da língua japonesa, é um software muito bom. Vou continuar minha busca por uma boa biblioteca porque meu negócio é automatização de processos, mas para quem produz material é uma ótima ferramenta.

* **🏳️‍🌈 Temas de papel:** foi difícil controlar o resultado da imagem jogando o prompt direto no Nano Banana. Dar as instruções primeiro para o Gemini e depois pedir para ele criar a ilustração resulta em imagens mais próximas do desejado. Pensando em procurar alguma biblioteca livre de imagens ou um gerador de fractais para automatizar a criação de imagens. Transformar em ASCII (por exemplo: [ascii_magik](https://github.com/LeandroBarone/python-ascii_magic/)). As imagens geradas pelo Gemini são extremamente pesadas, por isso utilizei o processo de "quantização" da biblioteca PIL|pillow para reduzir as imagens sem perder a qualidade.

* **🍭 Adesivos:** se consguisse automatizar a geração de imagens estava pensando em criar os adesivos, mas como não deu tempo de explorar o tema optei por usar emojis. Exemplo de [lista de emoji](https://gohugo.io/quick-reference/emojis/) para utilizar com markdown.

* **🎶 Música de fundo:** utilizei a biblioteca [music21](https://music21.org/music21docs/) para a produção de música em formato MIDI. Para arranjos e conversão para MP3 utilizei [musescore](https://musescore.org/ja) pela praticidade. Tive que usar a biblioteca pygame para tocar as músicas no aplicativo porque a função nativa do PyQt5 estava dando conflito de codificação.

* **🌤️ Modo de tela:** é uma funcionalidade criada para explorar arquivos qss da biblioteca PyQt5, que é praticamente igual a css3. As variações foram geradas automaticamente por engenharia de prompt.

* **🇯🇵 🇧🇷 🇺🇸 Tradução:** ao inicializar o aplicativo, é possível escolher entre três idiomas: inglês, japonês e português. Como o volume de informação é reduzido, optei por criar um dicionário contendo as traduções.

* **🍡 Perfil de cores:** criei três perfis de cores como exemplo. Para cada novo perfil é gerado um novo arquivo JSON que registra automaticamente cada definição de cor. Memória visual para o futuro.


## 🛠️ Tech Stack

* **Language|version:** Python 3.13.5
* **UI Framework:** PyQt5 (QSS for styling)
* **Audio Engine:** `pygame`
* **Music Logic:** `music21`
* **Asset Processing:** `Pillow` (PIL)
* **AI assistant:** Gemini 3.0

## 📂 Estrutura do projeto

```text
SynesthesiaKeyboard/
├── main.py                 # Estrutura e inicialização
├── requirements.txt        # Bibliotecas
├── src/                    
│   ├── config.py           # Variáveis
│   └── widgets.py          # Funções
└── assets/                 
    ├── bgm/                # MP3|WAV
    ├── modes/              # QSS
    ├── profiles/           # JSON
    ├── sounds/             # WAV
    └── themes/             # PNG
```

## 🚀 Como começar

### Prerequisites

Certifique-se de ter instalado [Python 3](https://www.python.org/downloads/) e `git` na sua máquina.


### Instalação pelo Terminal (MacOS)

1. Clone o repositório:
   ```bash
   git clone https://github.com/mitinisan/SynesthesiaKeyboard.git
   cd SynesthesiaKeyboard
   ```

2. Instale as bibliotecas necessárias:
   ```bash
   pip install -r requirements.txt
   ```

3. Inicialize o aplicativo:
   ```bash
   python main.py
   ```


## Falhas

No geral a apliação cumpre o seu propósito, mas não é perfeito e tem uma série de falhas que precisam ser reparadas.
Se você quiser muito que eu arrume, me paga um tchai e a gente conversa.
Debulhando e debugando você aprende um monte de coisa, então meu amigo | minha amiga: boa sorte!


## 📝 Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE) - consulte o arquivo LICENSE para obter detalhes.