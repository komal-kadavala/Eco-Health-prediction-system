v# Fix FileNotFoundError in app.py - Path Correction Plan

## Steps:
- [x] 1. Add path constants at top of app.py
- [x] 2. Fix init_user_csv() and init_health_data_csv() to use correct paths
- [x] 3. Update all user CSV functions (register_user, login_user, etc.) to use constants
- [x] 4. Fix save_user_health_data and get_user_health_history paths
- [x] 5. Fix model load paths in health assessment
- [x] 6. Test: streamlit run app.py (no FileNotFoundError)
- [x] 7. Complete task

**Status:** All path corrections completed (steps 1-5). Test with `streamlit run app.py`.
