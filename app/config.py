from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
APP_DIR = BASE_DIR / "app"
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
REPORTS_DIR = BASE_DIR / "reports"

SALES_MODEL_PATH = MODELS_DIR / "best_sales_model.joblib"
ROI_MODEL_PATH = MODELS_DIR / "best_roi_model.joblib"
SALES_MODEL_NAME_PATH = MODELS_DIR / "best_model_name.txt"
ROI_MODEL_NAME_PATH = MODELS_DIR / "best_roi_model_name.txt"

PROCESSED_DATA_PATH = DATA_DIR / "processed" / "marketing_and_sales_cleaned.csv"

SALES_TEST_RESULTS_PATH = REPORTS_DIR / "model_comparison_test_results.csv"
SALES_CV_RESULTS_PATH = REPORTS_DIR / "model_comparison_cv_results.csv"
ROI_TEST_RESULTS_PATH = REPORTS_DIR / "roi_model_comparison_test_results.csv"
ROI_CV_RESULTS_PATH = REPORTS_DIR / "roi_model_comparison_cv_results.csv"
SALES_IMPORTANCE_PATH = REPORTS_DIR / "permutation_importance.csv"
ROI_IMPORTANCE_PATH = REPORTS_DIR / "roi_permutation_importance.csv"

DEFAULT_API_URL = "http://127.0.0.1:8000"
INFLUENCERS = ["Mega", "Macro", "Micro", "Nano"]

MODEL_ORDER = [
    "Dummy Regressor",
    "Linear Regression",
    "Ridge Regression",
    "Random Forest",
    "Gradient Boosting",
    "MLP Regressor",
]
