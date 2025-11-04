# Contributing to Streamix

Thank you for your interest in contributing to Streamix!

## Development Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd streamix
```

2. **Backend Setup**
```bash
cd backend
pip install -r requirements.txt
# Configure db.py with your MySQL credentials
python app.py
```

3. **Frontend Setup**
```bash
cd frontend/my-app
npm install
npm start
```

4. **Database Setup**
```bash
mysql -u root -p
CREATE DATABASE streamingdb;
USE streamingdb;
source path/to/schema.sql;
source backend/database_objects.sql;
```

## Project Structure

```
streamix/
├── README.md                      # Main documentation
├── DATABASE_FEATURES.md           # Database objects documentation
├── TESTING_RESULTS.md            # Test results and examples
├── .gitignore                    # Git ignore rules
├── backend/
│   ├── README.md                 # Backend documentation
│   ├── API_DOCUMENTATION.md      # Complete API reference
│   ├── database_objects.sql      # All procedures, functions, triggers
│   ├── app.py                    # Flask application
│   ├── db.py                     # Database connection
│   ├── requirements.txt          # Python dependencies
│   ├── routes/                   # API route modules
│   └── utils/                    # Utilities (auth middleware)
└── frontend/
    └── my-app/
        ├── README.md             # Frontend documentation
        ├── package.json          # Node dependencies
        ├── public/               # Static files
        └── src/
            ├── pages/            # Page components
            ├── components/       # Reusable components
            └── services/         # API client
```

## Coding Standards

### Backend (Python)
- Follow PEP 8 style guide
- Use meaningful variable names
- Add docstrings to functions
- Handle errors with try-except blocks
- Use connection pooling for database

### Frontend (React)
- Use functional components with hooks
- Follow React best practices
- Use meaningful component names
- Keep components small and focused
- Use proper PropTypes or TypeScript

### Database
- Table names: singular, lowercase
- Column names: PascalCase (e.g., `Movie_Id`, `Title`)
- Stored procedures: prefix with `sp_`
- Functions: prefix with `fn_`
- Triggers: prefix with `trg_`

## Making Changes

1. **Create a new branch**
```bash
git checkout -b feature/your-feature-name
```

2. **Make your changes**
- Write clean, readable code
- Add comments where necessary
- Update documentation if needed

3. **Test your changes**
```bash
# Backend tests
cd backend
python -m pytest

# Frontend
cd frontend/my-app
npm test
```

4. **Commit your changes**
```bash
git add .
git commit -m "Description of your changes"
```

5. **Push to GitHub**
```bash
git push origin feature/your-feature-name
```

6. **Create Pull Request**
- Go to GitHub repository
- Click "New Pull Request"
- Describe your changes
- Wait for review

## Database Changes

When adding database objects:

1. Add SQL to `backend/database_objects.sql`
2. Document in `DATABASE_FEATURES.md`
3. Add usage examples in relevant route files
4. Test thoroughly with sample data
5. Update `TESTING_RESULTS.md` with test results

## API Changes

When adding/modifying API endpoints:

1. Update route files in `backend/routes/`
2. Document in `backend/API_DOCUMENTATION.md`
3. Update frontend API calls in `src/services/api.js`
4. Test with Postman or similar tool
5. Update frontend components as needed

## UI Changes

When modifying UI:

1. Maintain dark purple theme consistency
2. Ensure responsiveness
3. Test on multiple screen sizes
4. Update component documentation
5. Check accessibility

## Bug Reports

When reporting bugs:

1. Check if bug already reported
2. Provide clear description
3. Include steps to reproduce
4. Add screenshots if applicable
5. Mention your environment (OS, browser, etc.)

## Feature Requests

When requesting features:

1. Check if feature already requested
2. Provide clear use case
3. Explain expected behavior
4. Consider implementation complexity
5. Be open to discussion

## Questions?

Feel free to open an issue for any questions or clarifications.

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

---

Thank you for contributing to Streamix! 🎬
