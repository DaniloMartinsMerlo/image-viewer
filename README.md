# Visualizador de imagens

## Funções

* Upload de imagem (.png, .jpg, .jpeg)
* Inverter Cor
* Ajuste de intensidade RGB (vermelho, verde, azul) com reset
* Ajuste de Contraste e Brilho
* Aumento de Nitidez
* Conversão para Escala de Cinza
* Aplicação de Blur (Gaussiano)
* Detecção de Bordas (Canny)
* Espelhamento horizontal
* Rotação personalizada
* Visualização da imagem original e processada lado a lado
* Download da imagem filtrada nos formatos PNG, JPEG ou PDF

## Como executar

1- Crie um ambiente virtual
```bash
python -m venv venv
source venv/bin/activate
```

2- Instale as bibliotecas
```bash
pip install -r requirements.txt
```

3- Execute o streamlit
```bash
streamlit run app.py
```