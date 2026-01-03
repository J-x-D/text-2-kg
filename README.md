# LXS Text to KG (MonoRepo)

A user-centered neuro-symbolic approach for transforming unstructured text into highly semantically structured Knowledge Graphs. This application combines neural and symbolic techniques, leveraging Large Language Models and Knowledge Graphs to enable users to create high-quality knowledge representations.

## About

This application was developed as part of research on user-driven hybrid neuro-symbolic approaches for Knowledge Graph creation. For more details, please refer to our publication:

**Stütz, J. D., Karras, O., Oelen, A., & Auer, S. (2026).** *A User-Centered Neuro-Symbolic Approach for Knowledge Graph Creation from Text.* In Knowledge Graphs and Semantic Web (pp. 9-24). Springer Nature Switzerland. [https://doi.org/10.1007/978-3-032-13109-6_2](https://doi.org/10.1007/978-3-032-13109-6_2)

## Architecture

The application is split into three main components:

- **[Frontend](./frontend/README.md)** - A Next.js application built with React, TypeScript, and Material UI
- **[Backend](./backend/README.md)** - A Python Flask application responsible for text-to-knowledge-graph conversion
- **Database** - PostgreSQL database for storing application data

## Prerequisites

- Docker and Docker Compose
- OpenAI API key with active billing/credits
- Minimum 4GB RAM recommended

## Getting Started

### 1. Environment Variables Setup

Before running the application, you need to configure the environment variables with your OpenAI API credentials.

Create a `.env` file in the **root directory** of the project:

```bash
cat > .env << 'EOF'
OPENAI_API_KEY=sk-proj-your-actual-openai-key-here
OPENAI_ORGANIZATION=org-your-organization-id-here
EOF
```

**Important Notes:**
- The OpenAI API key is **required** for the application to function
- Ensure your OpenAI account has active billing and sufficient credits
- You can obtain your API key from: https://platform.openai.com/api-keys
- You can find your organization ID at: https://platform.openai.com/account/organization

**Verifying Your API Key:**

You can test your API key before starting the application:

```bash
source .env
curl -s https://api.openai.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "gpt-4o-mini",
    "messages": [{"role": "user", "content": "Hello"}],
    "max_tokens": 10
  }'
```

If successful, you should receive a valid JSON response. If you see an `insufficient_quota` error, please add credits to your OpenAI account.

### 2. Run with Docker Compose

To run the entire application (Frontend, Backend, and Database):

```bash
# Build and start all services
docker compose up --build

# Or run in detached mode (background)
docker compose up -d --build
```

### 3. Access the Application

Once all services are running, you can access:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Database**: localhost:5433 (PostgreSQL)

### 4. Stopping the Application

To stop all services:

```bash
# If running in foreground, press Ctrl+C, then:
docker compose down

# Or directly:
docker compose down
```

## Usage

Sample texts for testing are available in the [`frontend/public/texts/`](./frontend/public/texts/) directory, including:
- Anthropic.txt
- AppleVisionPro.txt
- DigitalProcurementWorkspace.txt
- MistralAi.txt
- TeslaCyberTruck.txt

## Troubleshooting

### OpenAI API Errors

**Error: `insufficient_quota`**
- Your OpenAI account doesn't have sufficient credits
- Solution: Add credits at https://platform.openai.com/account/billing

**Error: `invalid_api_key`**
- Your API key is incorrect or expired
- Solution: Generate a new key at https://platform.openai.com/api-keys

### Container Issues

**View logs:**
```bash
docker compose logs backend -f
docker compose logs frontend -f
```

**Restart services:**
```bash
docker compose restart backend
docker compose restart frontend
```

**Rebuild from scratch:**
```bash
docker compose down -v
docker compose up --build
```

## Citation

If you use this work in your research, please cite:

```bibtex
@InProceedings{10.1007/978-3-032-13109-6_2,
  author="St{\"u}tz, Jan-David
  and Karras, Oliver
  and Oelen, Allard
  and Auer, S{\"o}ren",
  editor="Villaz{\'o}n-Terrazas, Boris
  and Ortiz-Rodriguez, Fernando
  and Tiwari, Sanju
  and Riechert, Thomas
  and Marx, Edgard",
  title="A User-Centered Neuro-Symbolic Approach for Knowledge Graph Creation from Text",
  booktitle="Knowledge Graphs and Semantic Web",
  year="2026",
  publisher="Springer Nature Switzerland",
  address="Cham",
  pages="9--24",
  abstract="Organizations often use unstructured text to represent and exchange crucial information, such as product model descriptions, system requirements, and documentation. Even though the information within such unstructured text is precious, extracting it in more structured forms and exchanges is cumbersome, time-consuming, error-prone, and mostly reserved for experts. Combining neural and symbolic techniques, leveraging the integration of Large Language Models and Knowledge Graphs, can boost knowledge extraction and post-processing. While many approaches exist for transforming text into structured knowledge, they mostly lack automation, user integration, visual communication, and, consequently, trust and explainability. To address this gap, we present a user-driven hybrid neuro-symbolic approach that puts users in the loop to steer the transformation of unstructured text into highly semantically structured Knowledge Graphs. We evaluated our approach quantitatively and qualitatively to show that inexperienced users can create high-quality Knowledge Graphs with the same quality as experts, but in a fraction of the time. Our approach demonstrates that human interactions significantly enhance quality. Additionally, we confirmed our approach's high usability, as measured by the System Usability Scale, and strengthened the trust-building and explainability-contributing aspects through expert interviews.",
  isbn="978-3-032-13109-6"
}
```
