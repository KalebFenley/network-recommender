# Network Hardware Recommendation Engine

A "Wirecutter for network gear" — an opinionated, questionnaire-driven recommendation engine for network engineers.

## Overview

This project helps network engineers select the right vendor hardware based on their specific requirements. Users answer a structured questionnaire, and the engine scores all known products, returning ranked recommendations with reasoning.

## Technology Stack
- **Backend:** Python/FastAPI
- **Frontend:** React + Tailwind CSS (Vite)
- **Database:** Flat YAML files

## Running Locally

### Backend
1. Create a virtual environment and install dependencies:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Run the FastAPI server:
   ```bash
   export PYTHONPATH=.
   uvicorn recommender.main:app --reload
   ```

### Frontend
1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```
2. Start the dev server:
   ```bash
   npm run dev
   ```

## Contributing New Products

We welcome community contributions to expand our hardware database! You don't need to know Python or React to contribute—just YAML.

1. Copy the template file: `cp products/_template.yaml products/vendor-model.yaml`
2. Fill out the fields in your new YAML file based on the product's datasheet.
3. Validate your product file using our validation script:
   ```bash
   source .venv/bin/activate
   export PYTHONPATH=.
   python -m recommender.validate
   ```
   *Note: Ensure all tests and validations pass before submitting a Pull Request.*
4. Submit a PR with your new file.
