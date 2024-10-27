# FaceRecognition

O intuito deste projeto é demonstrar como o reconhecimento facial funciona na prática. A aplicação possui um fluxo simples e intuitivo:

1. **Cadastro de Rosto**: O usuário pode cadastrar um rosto, fornecendo o nome e a cidade correspondente. Essa etapa é fundamental para construir uma base de dados que permitirá o reconhecimento posterior.

2. **Reconhecimento Facial**: Após o cadastro, o usuário pode realizar o reconhecimento facial. A aplicação utilizará algoritmos avançados para identificar o rosto e associá-lo ao nome e cidade cadastrados.

3. **Emissão de Carbono**: Após a identificação, o usuário poderá visualizar dados sobre a emissão de carbono de acordo com a cidade selecionada. Isso adiciona uma camada de conscientização ambiental à aplicação, conectando a tecnologia de reconhecimento facial com informações relevantes sobre sustentabilidade.

## Índice
- [Tecnologias Usadas](#tecnologias-usadas)
- [Fluxo da Aplicação](#fluxo-da-aplicação)
- [Desafios Enfrentados](#desafios-enfrentados)

## Tecnologias Usadas

- **Banco de Dados**: PostgreSQL (escolhido por ser rápido, gratuito e por permitir a comparação de vetores com a extensão vector)
- **Backend**:
  - SQLAlchemy
  - FastAPI
  - imgbeddings
  - OpenCV
  - PIL
- **Frontend**:
  - Streamlit
  - streamlit_webrtc
  - asyncio
  - httpx
  - pandas
  - plotly
  - re
  - requests

## Fluxo da Aplicação

Na tela inicial da aplicação, o usuário pode escolher entre reconhecer um rosto ou cadastrar novos rostos. O fluxo de cadastro funciona da seguinte forma:

1. **Cadastro de Novo Rosto**: Na parte inferior da página, o usuário deve preencher um formulário com o nome, cidade e a foto que deseja carregar. Assim que todos os campos estiverem preenchidos, um botão aparece para enviar os dados para a API de reconhecimento.


2. **API de Reconhecimento**: A API possui duas rotas: uma para cadastrar e outra para reconhecer. A rota de cadastro registra as informações de Nome e Cidade em uma tabela no banco de dados chamada `users`. A foto é armazenada na tabela `pictures`. Antes de cadastrar, usamos OpenCV com um algoritmo de cascata para identificar rostos, desenhar retângulos nas imagens e recortá-las. A imagem é então transformada em vetor utilizando a biblioteca Pillow e normalizada com NumPy. Essa normalização ajuda a ajustar a matriz da imagem, reduzindo o threshold (valor limite que determina se um rosto é reconhecido ou não), facilitando a calibração do reconhecimento.

3. **Confirmação**: Após cadastrar a imagem, a API retorna informações para confirmar que tudo ocorreu bem.

![cadastro](./readmefiles/cadastro.jpg)

4. **Reconhecimento Facial**: Na parte de reconhecimento, o usuário clica em "Start" para abrir a câmera. Quando o rosto está posicionado na câmera, a aplicação identifica que há um rosto e, usando algoritmos de classificação, envia a imagem para a API para reconhecimento. A imagem é convertida da mesma forma que durante o cadastro, transformando-a em matriz para comparação. A consulta ao banco de dados é feita usando a extensão vector, e a aplicação calcula a distância euclidiana entre as matrizes. Se o threshold for menor que 0.7, as informações do usuário são retornadas. Quando as informações são recebidas, um gráfico é carregado, filtrando apenas a cidade cadastrada.

![reconhecimento](./readmefiles/reconhecimento.jpg)

![grafico](./readmefiles/grafico.jpg)

### Desafios Enfrentados

Durante o desenvolvimento, enfrentei alguns desafios significativos:

- **Problemas com a Câmera**: A biblioteca Streamlit não lida bem com funções assíncronas, o que causava travamentos nas imagens da câmera durante as consultas. Para resolver isso, precisei implementar soluções para garantir que a imagem da câmera não ficasse congelada.

- **Reconhecimento na API**: Inicialmente, a API apresentava problemas, reconhecendo erroneamente rostos não cadastrados ou falhando em identificar qualquer rosto. Após a normalização da matriz, o cálculo tornou-se mais preciso, resolvendo essas inconsistências.

Essa experiência me fez perceber que, apesar do reconhecimento facial ser amplamente utilizado em várias aplicações, incluindo as bancárias, ele pode falhar. No entanto, os bancos têm métodos para contornar essas falhas, o que é uma consideração importante ao trabalhar com essa tecnologia.
