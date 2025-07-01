# 📈 Paper Price Test - Data Engineer Case

Projeto de coleta automatizada de indicadores econômicos públicos para previsão do preço do papel. Desenvolvido em Python com deploy na Google Cloud Platform.

## 🧠 Objetivo

Extrair diariamente 3 indicadores do site [investing.com](https://br.investing.com):

- **Chinese Caixin Services Index**
- **Bloomberg Commodity Index**
- **USD/CNY**

Esses dados são salvos em formato tabular no Google Cloud Storage e prontos para ingestão no BigQuery.

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.10** + Selenium + BeautifulSoup + Pandas
- **Google Cloud Platform (GCP)**
  - Cloud Storage (GCS)
  - BigQuery
  - Cloud Run
  - Cloud Composer (Airflow)
- **Terraform** para infraestrutura como código
- **Docker** para conteinerização

---

## 📂 Estrutura do Projeto

```bash
paper-price-test/
├── dags/                       # DAG do Airflow (Cloud Composer)
│   └── invest_data_pipeline.py
├── scraper/                   # Scripts de scraping
│   └── main_scraper.py
├── terraform/                 # IaC para GCP
│   └── main.tf
├── Dockerfile                 # Empacota o scraper para Cloud Run
├── requirements.txt           # Bibliotecas Python
└── README.md                  # Documentação do projeto
```

---

## ⚙️ Setup Local

### 1. Clone o repositório
```bash
git clone https://github.com/SEU_USUARIO/paper-price-test.git
cd paper-price-test
```

### 2. Instale dependências (opcional com virtualenv)
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Exporte variáveis de ambiente (GCP)
```bash
export GOOGLE_APPLICATION_CREDENTIALS="path/to/key.json"
export GCS_BUCKET="investing-data-bucket"
```

### 4. Execute localmente
```bash
python scraper/main_scraper.py
```

Os arquivos `caixin_index.csv`, `bloomberg_commodity_index.csv` e `usd_cny.csv` serão enviados para o bucket.

---

## 🐳 Deploy via Docker

### Build da imagem
```bash
docker build -t paper-scraper .
```

### Execução local
```bash
docker run -e GCS_BUCKET=investing-data-bucket -v $HOME/.config/gcloud:/root/.config/gcloud paper-scraper
```

---

## ☁️ Deploy na Google Cloud

### 1. Enviar imagem para o Container Registry
```bash
gcloud builds submit --tag gcr.io/paper-price/scraper
```

### 2. Deploy com Terraform
```bash
cd terraform
terraform init
terraform apply
```

Recursos provisionados:
- Bucket GCS
- Dataset BigQuery
- Cloud Run Service
- Cloud Composer (Airflow DAG)

---

## 🛫 Agendamento Diário

O Airflow (Cloud Composer) executa a DAG `investing_data_pipeline` todos os dias às 6h (UTC), chamando o script principal para scraping e salvamento no GCS.

---

## 📌 Observações
- O scraping depende da estrutura do HTML do investing.com e pode quebrar com mudanças no site.
- A raspagem utiliza Chromium headless e pode demandar ajustes de timeout.

---

## 👨‍💻 Autor

Desenvolvido por **Lucas Nicholas** para desafio técnico de engenharia de dados.

📧 [linkedin.com/in/lucas-nicholas](https://linkedin.com/in/lucas-nicholas)

---

## ✅ Checklist de Entrega

- [x] Scraper funcional (Caixin, Bloomberg, USD/CNY)
- [x] Upload para GCS
- [x] Deploy via Docker e Cloud Run
- [x] DAG Airflow para Composer
- [x] Terraform com todos recursos
- [x] Código versionado no GitHub privado
