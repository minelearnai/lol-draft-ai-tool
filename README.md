# LoL Draft AI Tool

## Architecture Overview

### Technology Stack
- **Backend**: Python FastAPI on Google Cloud Run
- **Frontend**: React/TypeScript on Firebase Hosting 
- **ML/AI**: Vertex AI + Custom Models
- **Database**: Cloud Firestore + Cloud SQL
- **API**: Riot Games Match-v5 Integration
- **CI/CD**: GitHub Actions

### Project Structure
```
lol-draft-ai-tool/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── core/           # Configuration
│   │   ├── ml/             # ML models & training
│   │   ├── models/         # Data models
│   │   └── services/       # Business logic
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/                # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── hooks/          # Custom hooks
│   │   ├── services/       # API calls
│   │   └── types/          # TypeScript types
│   └── package.json
├── infrastructure/          # GCP setup
│   ├── terraform/          # Infrastructure as Code
│   └── scripts/           # Deployment scripts
├── .github/workflows/      # CI/CD pipelines
└── docs/                   # Documentation
```

### Features
- Real-time draft tracking
- AI-powered pick/ban suggestions
- Team composition analysis
- Win probability predictions
- Champion synergy recommendations
- Historical data insights

### Riot Games ToS Compliance
- Read-only API usage
- No automated actions
- Educational purpose focus
- Rate limiting compliance
- Personal use restrictions

## Quick Start

### Prerequisites
- Google Cloud Platform account
- Riot Games API key
- Node.js 18+
- Python 3.11+
- Docker

### Development Setup
```bash
git clone https://github.com/minelearnai/lol-draft-ai-tool.git
cd lol-draft-ai-tool

# Backend setup
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend setup
cd ../frontend
npm install
npm start
```

### GCP Deployment
```bash
# Setup GCP project
gcloud projects create lol-draft-ai-tool
gcloud config set project lol-draft-ai-tool

# Deploy infrastructure
cd infrastructure/terraform
terraform init
terraform apply

# Deploy application
gcloud run deploy lol-draft-api --source backend/
```

## Cost Estimation
- **Free Tier Usage**: ~$0-5/month for low traffic
- **Production Ready**: ~$20-50/month for 1k users
- **Scale**: ~$100-300/month for 10k+ users

## Performance Targets
- API Response: <200ms
- ML Predictions: <500ms
- Real-time Updates: <100ms latency
- Uptime: 99.9%

## License
MIT License - Educational use only