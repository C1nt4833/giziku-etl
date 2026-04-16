# Contributing Guidelines

Terima kasih untuk berkontribusi pada project GiziKu ETL Pipeline! Berikut adalah panduan untuk memastikan kolaborasi tim berjalan lancar.

## 📋 Code of Conduct

- Hormati setiap contributor
- Berikan feedback yang constructive
- Hindari bahasa yang menyinggung
- Kolaborasi dengan team spirit

## 🔄 Development Workflow

### 1. Setup Development Environment

```bash
# Clone repository
git clone https://github.com/username/giziku-etl.git
cd giziku-etl

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Create Feature Branch

```bash
# Update master branch
git checkout main
git pull origin main

# Create feature branch
git checkout -b feature/your-feature-name
# atau untuk bug fixes:
git checkout -b bugfix/your-bugfix-name
```

Branch naming convention:
- `feature/` untuk fitur baru
- `bugfix/` untuk bug fixes
- `docs/` untuk documentation updates
- `refactor/` untuk code refactoring

### 3. Make Changes

#### Code Style
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use 4 spaces for indentation
- Max line length: 100 characters
- Use meaningful variable names

#### Documentation
```python
def extract_nutrition_values(html_content):
    """Extract nutrition values dari HTML content.
    
    Args:
        html_content (str): HTML content berisi nutrient data
        
    Returns:
        dict: Dictionary berisi parsed nutrition values
        
    Raises:
        ValueError: Jika input tidak valid
        
    Example:
        >>> result = extract_nutrition_values(html)
        >>> result['energi']
        2650.0
    """
    pass
```

#### Comments
```python
# Gunakan comments untuk menjelaskan MENGAPA, bukan APA
# ❌ JANGAN:
x = y + 1  # tambah 1 ke y

# ✅ BENAR:
# Tambah margin tambahan untuk kategori khusus (hamil/menyusui)
nutritional_value = base_value + additional_value
```

### 4. Write/Update Tests

**Untuk setiap fitur baru, HARUS ada unit tests:**

```python
class TestNewFeature(unittest.TestCase):
    """Test cases untuk new feature."""
    
    def setUp(self):
        """Setup test data."""
        self.sample_data = {...}
    
    def test_feature_success(self):
        """Test happy path scenario."""
        result = new_feature(self.sample_data)
        self.assertEqual(result, expected_value)
    
    def test_feature_error_handling(self):
        """Test error handling scenario."""
        with self.assertRaises(ValueError):
            new_feature(invalid_data)
```

**Jalankan tests locally:**
```bash
# Run semua tests
python -m unittest discover tests

# Run specific test file
python -m unittest tests.test_extract

# Run dengan coverage
coverage run -m unittest discover tests
coverage report -m
```

**Target coverage:** ≥85%

### 5. Commit Changes

```bash
# Check status
git status

# Add files
git add .

# Commit dengan meaningful message
git commit -m "Add feature: [description of what changed]"
```

Commit message guidelines:
```
# Format
[Type]: [Subject]

[Body - optional]

[Footer - optional]

# Types:
# - feat: fitur baru
# - fix: bug fix
# - docs: dokumentasi changes
# - style: formatting, missing semicolons, etc
# - refactor: code restructuring
# - test: adding/updating tests
# - chore: build config, dependencies, etc

# Examples:
feat: Add Google Sheets integration for team collaboration
fix: Handle None values in extract_nutrition_values
docs: Update README dengan setup instructions
```

### 6. Push & Create Pull Request

```bash
# Push branch ke remote
git push origin feature/your-feature-name
```

**PR Description Template:**
```markdown
## Description
Brief description of changes.

## Type of Change
- [ ] New feature
- [ ] Bug fix
- [ ] Documentation update
- [ ] Breaking change

## Testing Done
- [ ] Unit tests added/updated
- [ ] Manual testing completed
- [ ] Coverage ≥85%

## Checklist
- [ ] Code follows PEP 8 style guide
- [ ] Documentation updated
- [ ] Tests passing locally
- [ ] No breaking changes

## Screenshots/Output
[if applicable]
```

### 7. Code Review & Merge

- Reviewer akan melakukan code review
- Diskusikan feedback dan lakukan updates jika diperlukan
- Setelah approved, merge ke main branch
- Delete feature branch

## 📊 Error Handling Standards

```python
# Selalu handle errors dengan meaningful messages
try:
    result = fetch_data(url)
except requests.exceptions.Timeout:
    # Jangan: print("Error")
    # Benar:
    logger.error(f"Timeout fetching data from {url}")
    raise ConnectionError(f"Failed to fetch {url}: timeout after 30s")
except requests.exceptions.RequestException as e:
    logger.error(f"Request failed: {e}")
    raise
```

## 🗂️ Module Organization

```
module/
├── __init__.py          # Expose public API
├── core.py              # Main logic
├── handlers.py          # Error handling
└── utils.py             # Helper functions

# __init__.py example:
from .core import main_function
from .handlers import CustomException

__all__ = ['main_function', 'CustomException']
```

## 📝 Documentation Standards

- Update README.md jika ada breaking changes
- Tambahkan docstrings untuk semua functions/classes
- Include example usage di docstring
- Update CHANGELOG.md untuk release notes

## 🐛 Bug Reports

Jika menemukan bug:

1. Cek issue list belum ada yang similar
2. Buat issue dengan template:

```markdown
## Description
[Clear description of bug]

## Steps to Reproduce
1. [First step]
2. [Second step]

## Expected Behavior
[What should happen]

## Actual Behavior
[What actually happens]

## Environment
- Python version: 
- OS: 
- Dependencies installed: 

## Error Message/Logs
[Relevant logs/errors]

## Possible Solution
[If you have ideas]
```

## 🎯 Performance Considerations

- Minimize API calls (use caching jika applicable)
- Handle rate limits dengan retry logic
- Log execution time untuk performance-critical operations
- Profile code untuk identify bottlenecks: `python -m cProfile main.py`

## 📚 Useful Resources

- [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
- [Python Logging](https://docs.python.org/3/library/logging.html)
- [Unit Testing Best Practices](https://realpython.com/python-testing/)

## ❓ Questions?

- Tanyakan di team chat untuk quick questions
- Buat GitHub Discussion untuk broader topics
- Ping maintainers untuk urgent issues

---

**Happy Contributing!** 🚀
