# NOVA Store — Flask E-Commerce Demo

A simple, polished e-commerce web application for the Agile Software Development FA2 CI/CD assignment.

## Stack
- Python + Flask
- HTML templates + CSS (no JavaScript required)
- SQLite for order storage
- pytest for automated tests
- flake8 for code quality
- GitHub Actions for CI and build-artifact delivery

## Features
- Responsive storefront and product cards
- Product search and category filters
- Session-based shopping cart
- Quantity updates and item removal
- Checkout form with server-side validation
- Order confirmation page
- Orders saved in SQLite
- Health endpoint at `/health`

## Run on Windows
1. Install Python 3.10 or newer.
2. Open this folder in VS Code.
3. Create and activate a virtual environment:

   ```powershell
   py -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

4. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

5. Start the app:

   ```powershell
   python run.py
   ```

6. Open http://127.0.0.1:5000.

If PowerShell blocks activation, use `.venv\Scripts\python.exe -m pip install -r requirements.txt` and `.venv\Scripts\python.exe run.py`.

## Verify
```powershell
pytest -q
flake8 app tests run.py --max-line-length=100
```

## CI/CD
The workflow at `.github/workflows/ci.yml` runs on pushes and pull requests to `main` or `master`. It installs dependencies, runs flake8, runs pytest, prepares an application folder, and uploads it as a GitHub Actions artifact.

The current workflow uploads a build artifact; it does not publish a public website. If your instructor requires a live deployment, add a hosting target such as Render after the core pipeline works.

## Push to GitHub
Create an empty GitHub repository, then run these commands from this folder, replacing the URL:

```powershell
git init
git add .
git commit -m "Build NOVA Store with Flask"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```

Then open the repository's Actions tab.

## Routes
- `GET /` — storefront, search, and category filtering
- `POST /cart/add/<product_id>` — add item
- `GET /cart` — view cart
- `POST /cart/update/<product_id>` — update quantity
- `POST /cart/remove/<product_id>` — remove item
- `GET, POST /checkout` — checkout
- `GET /orders/<order_id>` — order confirmation
- `GET /health` — health check

## Limitations
- No accounts, real payments, or stock management.
- Cart is stored in Flask's signed session cookie.
- Product images require internet access.
- This is a college demo, not production-ready. Set a strong `SECRET_KEY` before public deployment.
