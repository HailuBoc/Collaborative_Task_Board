# Contributing to Collaborative Task Board

Thank you for your interest in contributing! Here's how to get started.

## Development Setup

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

Backend runs on `http://localhost:8000`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on `http://localhost:5173`

## Project Structure

```
├── backend/
│   ├── main.py           # Starlette app & routes
│   ├── database.py       # PostgreSQL connection
│   ├── models.py         # Data models
│   ├── schemas.py        # Request/response schemas
│   └── requirements.txt   # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.tsx       # Main React component
│   │   ├── api.ts        # API client
│   │   └── App.css       # Styles
│   └── package.json      # Node dependencies
└── DEPLOY.md             # Deployment guide
```

## Making Changes

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make your changes
3. Test locally
4. Commit: `git commit -m "Add your feature"`
5. Push: `git push origin feature/your-feature`
6. Open a pull request

## Code Style

- **Backend**: Follow PEP 8
- **Frontend**: Use TypeScript strict mode
- Add comments for complex logic
- Keep functions focused and small

## Testing

Run tests before committing:

```bash
# Backend
cd backend
python -m pytest

# Frontend
cd frontend
npm run test
```

## Reporting Issues

Found a bug? Open an issue with:
- Clear description
- Steps to reproduce
- Expected vs actual behavior
- Screenshots if applicable

## Questions?

Feel free to open a discussion or issue!
