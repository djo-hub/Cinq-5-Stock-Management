import sys
import os
from PyQt6.QtWidgets import QApplication
from app.database import init_db
from app.ui.main_window import MainWindow
from app.ui.login import LoginDialog
from app.ui.first_run_setup import FirstRunWizard
from app.config import _get_app_dir, SETTINGS_PATH
from PyQt6.QtGui import QIcon
from app.utils import resource_path
from app.logger import get_logger


# Initialize logging
logger = get_logger()

app = QApplication(sys.argv)
app.setWindowIcon(QIcon(resource_path("assets/icon.ico")))

try:
    # Initialize database
    init_db()
    logger.info("Database initialized")
    
    # Check if this is first run (no settings.json)
    first_run = not os.path.exists(SETTINGS_PATH)
    
    if first_run:
        logger.info("First-run detected, showing setup wizard")
        wizard = FirstRunWizard()
        if wizard.exec() != FirstRunWizard.DialogCode.Accepted:
            logger.info("Setup wizard cancelled by user")
            sys.exit(0)
    
    # Main application loop
    while True:
        login = LoginDialog()
        if login.exec() != LoginDialog.DialogCode.Accepted:
            logger.info("User cancelled login")
            sys.exit(0)
        
        window = MainWindow()
        logged_out = False
        
        def on_logout():
            global logged_out
            logged_out = True
        
        window.logout_requested.connect(on_logout)
        window.show()
        app.exec()
        
        if not logged_out:
            logger.info("User closed main window normally")
            break  # window was closed normally (X button) — exit app
    
    logger.info("Application shut down normally")
    sys.exit(0)

except Exception as e:
    logger.exception("Fatal error during application startup")
    from PyQt6.QtWidgets import QMessageBox
    QMessageBox.critical(
        None,
        "Fatal Error",
        f"An unexpected error occurred:\n\n{str(e)}\n\n"
        "Check the logs directory for more details."
    )
    sys.exit(1)
