# NOVA Store — Flask E-Commerce Demo

NOVA Store is a simple, responsive e-commerce web application built with Python and Flask for the Agile Software Development FA2 assignment. The project demonstrates web application development, automated testing, code quality checks, build artifacts, and CI/CD deployment using GitHub Actions and Render.

## Live Demo

- **Live Application:** https://nova-store-flask.onrender.com
- **GitHub Repository:** https://github.com/Atharvaa09/nova-store-flask

The application is hosted on Render. As this project uses a free web service, the first request after a period of inactivity may take some time to load.

## Technology Stack

- **Backend:** Python, Flask
- **Frontend:** HTML, Jinja2 templates, CSS
- **Database:** SQLite
- **Testing:** pytest
- **Code Quality:** Flake8
- **Version Control:** Git and GitHub
- **CI/CD:** GitHub Actions
- **Deployment:** Render
- **Production Server:** Gunicorn

## Features

- Responsive storefront with product cards
- Product search and category filtering
- Session-based shopping cart
- Cart quantity updates and item removal
- Checkout form with server-side validation
- Order confirmation page
- Order and order-item records stored in SQLite
- Health-check endpoint at `/health`
- Automated testing with pytest
- Automated code quality checks with Flake8
- ZIP build artifact generation and upload
- Deployment request to Render after successful CI checks

## Project Structure

```text
nova-store-flask/
├── .github/
│   └── workflows/
│       └── ci.yml
├── app/
│   ├── __init__.py
│   ├── templates/
│   └── static/
├── data/
│   └── products.json
├── tests/
│   └── test_app.py
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
└── run.py
```

The application initializes its SQLite database in the `data/` directory. The database file is created when the application starts if it does not already exist.

## Run Locally on Windows

### Prerequisites

- Python 3.10 or newer
- Git (optional for cloning and version control)
- Visual Studio Code or another code editor

### 1. Clone the repository

```powershell
git clone https://github.com/Atharvaa09/nova-store-flask.git
cd nova-store-flask
```

Alternatively, open your existing project folder in VS Code.

### 2. Create a virtual environment

```powershell
py -m venv .venv
```

### 3. Activate the virtual environment

```powershell
.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use the virtual environment's Python executable directly in the following commands.

### 4. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

If you could not activate the environment, run:

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 5. Start the application

```powershell
python run.py
```

If the environment is not activated:

```powershell
.venv\Scripts\python.exe run.py
```

### 6. Open the website

Visit:

http://127.0.0.1:5000

## Automated Testing

Run the test suite from the project root:

```powershell
python -m pytest -v
```

The tests verify application behavior, including key routes and shopping or checkout functionality.

## Code Quality Checks

Run Flake8:

```powershell
python -m flake8 app tests run.py
```

This checks the application and test code for common Python style and quality issues.

## CI/CD Pipeline

The GitHub Actions workflow is defined in:

`.github/workflows/ci.yml`

The workflow runs automatically on pushes and pull requests targeting the `main` branch.

### Pipeline stages

1. **Checkout:** Retrieves the repository source code.
2. **Environment setup:** Configures Python 3.12.
3. **Dependency installation:** Installs packages from `requirements.txt`.
4. **Code quality check:** Runs Flake8.
5. **Automated testing:** Runs pytest.
6. **Build artifact:** Packages the application into a ZIP file.
7. **Artifact upload:** Uploads the ZIP file to GitHub Actions.
8. **Deployment request:** On a successful push to `main`, sends a deployment request to Render using the `RENDER_DEPLOY_HOOK` GitHub Actions secret.

The deployment step is intended to run only after the preceding checks and artifact steps succeed. The GitHub repository must have the deployment hook configured as an Actions secret.

### Viewing workflow results

1. Open the GitHub repository.
2. Select the **Actions** tab.
3. Open a workflow run.
4. Inspect the code quality, testing, artifact, and deployment steps.

A successful workflow indicates that its configured steps completed successfully. Render deployment status can also be checked in the Render dashboard.

## Application Routes

| Method | Route | Description |
|---|---|---|
| GET | `/` | Storefront, product search, and category filtering |
| POST | `/cart/add/<product_id>` | Add a product to the cart |
| GET | `/cart` | View the shopping cart |
| POST | `/cart/update/<product_id>` | Update a cart item's quantity |
| POST | `/cart/remove/<product_id>` | Remove an item from the cart |
| GET, POST | `/checkout` | Display and process checkout |
| GET | `/orders/<order_id>` | Display order confirmation |
| GET | `/health` | Health check |

## Database and Data Persistence

The application currently uses SQLite to store orders and order items.

During local development, the database is stored at:

`data/nova_store.db`

The live Render deployment currently uses SQLite on the service's local filesystem. Render's free web services have ephemeral filesystems, so database changes may be lost after a restart or redeployment.

Moving order storage to a hosted PostgreSQL database is a planned improvement for persistent order history.

## Security and Limitations

- No customer accounts or authentication.
- No real payment processing.
- No inventory or stock management.
- Shopping cart data is stored in Flask's signed session cookie.
- A strong, private `SECRET_KEY` must be configured for deployment.
- Order persistence on the free Render filesystem is not guaranteed.
- Product images may require internet access.
- The application is designed as a college demonstration project and is not production-ready.

## Future Improvements

- Migrate order storage to hosted PostgreSQL.
- Add customer registration and login.
- Integrate a payment gateway in a properly secured environment.
- Add inventory and stock management.
- Improve order history and administrative functionality.
- Expand automated tests and security checks.

## Learning Outcomes

This project demonstrates:

- Building a Flask web application
- Handling forms, sessions, and database operations
- Writing automated tests using pytest
- Enforcing code quality with Flake8
- Managing source code with Git and GitHub
- Automating CI/CD workflows using GitHub Actions
- Packaging build artifacts
- Deploying a web application to Render

## Author

**Atharva Gaikwad**

Developed as part of the Agile Software Development FA2 assignment.
