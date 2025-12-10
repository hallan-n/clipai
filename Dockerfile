FROM python:3.11-slim

# Instala dependências do sistema necessárias
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    libffi-dev \
    libssl-dev \
    python3-dev \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Define diretório de trabalho
WORKDIR /app

# Copia código e requirements
COPY ./app /app
COPY requirements.txt /app/requirements.txt

# Atualiza pip
RUN pip install --upgrade pip

# Instala Torch CPU-only com index especial
RUN pip install torch==2.9.1+cpu torchvision==0.24.1+cpu torchaudio==2.9.1+cpu --index-url https://download.pytorch.org/whl/cpu

# Instala o restante das dependências (Whisper e Loguru)
RUN pip install --no-cache-dir -r requirements.txt

# Executa o main.py por padrão
CMD ["python", "main.py"]
