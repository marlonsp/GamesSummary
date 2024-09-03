# GamesSummary - Projeto de Recomendação de Jogos
Feito por: Marlon Silva Pereira

## Introdução
Este projeto é uma API de recomendação de jogos, desenvolvida utilizando a técnica de TF-IDF para análise de similaridade entre descrições de jogos. O objetivo é fornecer aos usuários recomendações de jogos que estejam alinhadas com seus interesses, baseando-se nas descrições dos jogos disponíveis no banco de dados. Além disso, a API retorna o link para a página do jogo no Metacritic, uma plataforma popular que oferece críticas e avaliações de jogos.

## O que é Metacritic?
[Metacritic](https://www.metacritic.com/) é um site que agrega críticas e avaliações de várias fontes para filmes, jogos, séries de TV, música e outras formas de mídia. Ele calcula uma média das pontuações dadas por diferentes críticos e apresenta uma pontuação geral para cada item, facilitando a decisão dos consumidores sobre o que assistir, jogar ou ouvir. Neste projeto, utilizamos o Metacritic como fonte para construir o banco de dados de jogos, extraindo descrições e links para as páginas de cada jogo.

## Funcionalidades do Projeto
- Recomendação Personalizada: Com base nos interesses do usuário fornecidos através de uma consulta, a API retorna uma lista de jogos recomendados, acompanhados de suas descrições, relevância em relação à consulta e links para suas páginas no Metacritic.
- Scraping de Dados: Caso o usuário não deseje usar o CSV fornecido no repositório, um script de scraping permite a extração de dados diretamente do site do Metacritic.

## Instalação e Uso

1- Clone o Repositório

Primeiro, clone o repositório para o seu ambiente local:

```bash
git clone https://github.com/marlonsp/GamesSummary
cd GamesSummary
```

2- Prepare o Ambiente

Execute o script setup_and_run.sh para configurar o ambiente virtual, instalar as dependências e iniciar o servidor FastAPI:

```bash
chmod +x setup_and_run.sh
./setup_and_run.sh
```
Este script irá:

Criar um ambiente virtual (venv) se ainda não existir.
Ativar o ambiente virtual.
Instalar todas as dependências listadas no requirements.txt.
Verificar se o arquivo CSV com os dados dos jogos está presente. Caso esteja, o servidor FastAPI será iniciado.
Desativar o ambiente virtual após a execução.

3- Iniciar a API

Se o arquivo CSV (data/games_data.csv) estiver no local correto, a API será automaticamente iniciada e estará disponível no endereço http://localhost:9191.

Utilização da API

Com a API em execução, você pode obter recomendações de jogos acessando o endpoint /query/ com o parâmetro text representando os interesses do usuário. Por exemplo:

```bash
http://localhost:8000/query/?text=shooter
```
Isto retornará uma lista de jogos recomendados com base na descrição de "shooter".

4- Raspagem de Dados (Opcional)

Se você deseja extrair seus próprios dados de jogos do Metacritic, execute o script scraping.py:

```bash
python scraping.py <número_de_páginas>
```
Substitua <número_de_páginas> pelo número de páginas que deseja extrair (máximo de 557).
O script gerará um arquivo CSV com os dados extraídos, que pode ser utilizado no projeto.

## Formato de Resposta
A resposta da API é no formato de json, como no exemplo:
```json
{
  "results": [
    {
      "game_name": "PixelJunk Shooter 2",
      "description": "PixelJunk Shooter returns with more levels and new features....",
      "url": "https://www.metacritic.com/game/pixeljunk-shooter-2/",
      "relevance": "0.3706"
    },
    // outros jogos
  ],
  "message": "OK"
}
```
A estrutura de retorno da API possui os seguintes campos:

- results: É uma lista de objetos, onde cada objeto representa um jogo recomendado com base nos interesses do usuário. Cada objeto contém as seguintes informações:

- game_name: O nome do jogo recomendado.
- description: Uma breve descrição do jogo, fornecida pela página do Metacritic, que ajuda o usuário a entender o conteúdo e a temática do jogo.
- url: O link para a página do jogo no Metacritic, onde o usuário pode encontrar mais informações, críticas, e avaliações sobre o jogo.
- relevance: Um valor numérico que indica a relevância do jogo em relação aos interesses do usuário, baseado na similaridade entre a descrição do jogo e a consulta feita.
- message: Uma string que indica o status da resposta da API. No exemplo dado, o valor é "OK", o que significa que a API processou a solicitação com sucesso.

## Casos de Testes:

1. Resposta com 10 resultados: http://localhost:9191/query/?text=rpg<br>
Essa pesquisa retorna 10 resultados por causa do estilo "RPG" ser um tema comum no mundo dos jogos
2. Resposta com menos de 10 resultados: http://localhost:9191/query/?text=educational<br>
Essa pesquisa retorna menos de 10 resultados por causa do tema "educational" não ter tanto destaque entre os jogos mais conhecidos.
3. Resposta não óbvia: http://localhost:9191/query/?text=brazil<br>
Esta pesquisa retorna jogos relacionados ao termo "Brazil", sendo quase todos jogos de futebol que fazem referência direta ao país. No entanto, também retorna o jogo "Sherlock Holmes: The Silver Earring", que, embora não seja um jogo de futebol, menciona o Brasil em seu enredo, pois o jogo leva os jogadores a várias localizações, incluindo o Brasil, como parte da aventura do detetive Sherlock Holmes.
