# GrowSmart

<h3 align = "center">Nossa Equipe</h3>
<p align = "center">
  <a href="https://github.com/AdrielFernando">Adriel Fernando</a>
  -
  <a href="https://github.com/Ioshua-N">Ioshua Noia</a>
  -
  <a href="https://github.com/PedroHCMelo">Pedro Henrique</a>
  -
  <a href="https://github.com/SidneyRodrigo">Sidney Rodrigo</a>
  -
  <a href="">Ana Carla</a>
  -
  <a href="">Ana Paula</a>
  -
  <a href="">Amanndha Sena</a>
</p>

## Nosso Projeto / Our Project

O GrowSmart é um projeto IoT que utiliza uma placa Arduino juntamente com sensores para monitorar a temperatura, umidade e luminosidade de um vaso de plantas. Os dados coletados são enviados para uma API que os exibe de forma prática e, com o auxílio de inteligência artificial, faz uma análise das condições da planta, indicando possíveis mudanças para resolver problemas. O repositório inclui o código da API, os arquivos HTML e CSS do site, o script para a placa Arduino e o arquivo de configuração da API hospedada no PythonAnywhere.

GrowSmart is an IoT project that uses an Arduino board along with sensors to monitor the temperature, humidity, and light levels of a plant pot. The collected data is sent to an API, which displays it in a user-friendly manner. Additionally, with the help of artificial intelligence, it analyzes the plant's conditions and suggests possible changes to address any issues. The repository includes the API code, the HTML and CSS files for the website, the script for the Arduino board, and the API configuration file hosted on PythonAnywhere.

## Itens Nescessários / 

- 1 Placa Arduino
- 1 Sensore de Umidade
- 1 Sensor de Luminosidade
- 1 Sensor de Temperatura
- API e Banco de Dados

## Fluxo de Funcionamento

1. Arduino
- Faz conexão com rede Wi-Fi
- Envia os dados recebidos pelos sensores para a API

2. API
- Recebe a requisição POST
- Insere os dados no banco de dados
- Consulta a condição da planta utilizando um prompt retornado de uma API do Gemini
- Fornece acesso aos dados armazenados

3. Front-End
- Recebe os dados do back utilizando a requisição GET da API.
- Exibe os valores

4. Banco de Dados MySQL
- Recebe e armazena os dados recebidos da API
- Envia dados para a API
