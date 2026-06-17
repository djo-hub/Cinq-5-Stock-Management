# Cinq-5 - Desktop Business Management App

A comprehensive desktop application built with Python and PyQt6 to help businesses manage their products, inventory, clients, suppliers, and financials.

##  Key Features

- **Product & Stock Management**: Track inventory levels, categorize products, and receive low stock alerts.
- **Client & Supplier Management**: Maintain detailed profiles and contact information.
- **Invoice Creation**: Generate, manage, and print professional PDF invoices.
- **Debt & Payment Tracking**: Monitor outstanding debts and record partial or full payments.
- **Interactive Dashboard**: Visualize key metrics and statistics with charts.
- **Secure Access**: First-run setup wizard and password-protected login system.
- **Multi-language Support**: Built-in internationalization for multiple languages.
- **Customizable Settings**: Configure business details, currency, and tax (TVA) rates.

##  Technology Stack

- **Language**: Python 3
- **GUI Framework**: PyQt6 (with QtAwesome for icons)
- **Database**: SQLite (via SQLAlchemy ORM)
- **PDF Generation**: ReportLab
- **Data Visualization**: Matplotlib
- **Packaging**: PyInstaller

##  Project Structure

- `app/models/`: SQLAlchemy database models.
- `app/services/`: Core business logic and database operations.
- `app/ui/`: PyQt6 user interface components and windows.
- `assets/`: Application icons and static assets.
- `saves/`: Directory where generated PDF invoices are saved.
- `logs/`: Application execution logs.
- `main.py`: Entry point of the application.

##  Setup & Installation

1. **Install the dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application**:
   ```bash
   python main.py
   ```
   *On the first run, the app will initialize the local database and launch a setup wizard to configure your business profile and admin credentials.*

##  Packaging as an Executable (Windows)

To package the application into a standalone `.exe` file:

```bash
pyinstaller --onefile --windowed --name Manager main.py
```
*(Or use the provided `manager.spec` file for more advanced bundling).*
