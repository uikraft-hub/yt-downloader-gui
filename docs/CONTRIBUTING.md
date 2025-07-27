# Contributing to Pinterest Media Scraper

Thank you for your interest in contributing to Pinterest Media Scraper! We welcome contributions from everyone and appreciate your help in making this Streamlit-based media downloader better for the community.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Issue Guidelines](#issue-guidelines)
- [Community](#community)

## Code of Conduct

This project and everyone participating in it is governed by our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to [ujjwalkrai@gmail.com](mailto:ujjwalkrai@gmail.com).

## Getting Started

### Prerequisites

Before you begin, ensure you have the following:
- A GitHub account
- Git installed on your local machine
- Python 3.8 or higher
- Basic knowledge of web scraping and Streamlit applications
- Understanding of Pinterest's structure and media handling

### First Time Setup

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/your-username/pinterest-media-scraper.git
   cd pinterest-media-scraper
   ```
3. Add the upstream repository:
   ```bash
   git remote add upstream https://github.com/uikraft-hub/pinterest-media-scraper.git
   ```
4. Review the project structure:
```
pinterest-media-scraper/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   ├── PULL_REQUEST_TEMPLATE.md
│   ├── RELEASE_TEMPLATE.md
│   └── workflows/
│       └── ci.yml
├── .gitignore
├── assets/
│   ├── pinterest-media-scraper-banner.jpg
│   └── screenshots/
│       └── screenshot.png
├── docs/
│   ├── CHANGELOG.md
│   ├── CODE_OF_CONDUCT.md
│   ├── CONTRIBUTING.md
│   ├── README.md
│   ├── SECURITY.md
│   ├── STATUS.md
│   └── USAGE.md
├── LICENSE
├── pyproject.toml
├── requirements.txt
├── src/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── downloader.py
│   │   ├── ui.py
│   │   └── utils.py
│   └── main.py
└── tests/
    └── test_downloader.py
```

5. Install the project in development mode:
   ```bash
   pip install -e .
   ```

## How to Contribute

### Types of Contributions

We welcome several types of contributions:

- **Core Functionality**: Enhance media scraping capabilities and download features
- **UI/UX Improvements**: Improve the Streamlit interface and user experience
- **Performance Optimization**: Optimize scraping speed, memory usage, and concurrency
- **Error Handling**: Improve error handling and user feedback mechanisms
- **Testing**: Add comprehensive tests for scraping and download functionality
- **Documentation**: Improve guides, API documentation, and usage examples
- **Bug Reports**: Help us identify and fix scraping or download issues
- **Feature Requests**: Suggest new Pinterest media sources or download options
- **Platform Support**: Add support for new Pinterest URL formats or media types

### Before You Start

1. Check existing [issues](https://github.com/uikraft-hub/pinterest-media-scraper/issues) and [pull requests](https://github.com/uikraft-hub/pinterest-media-scraper/pulls) to avoid duplicates
2. For major changes or new features, please open an issue first to discuss your proposed changes
3. Make sure your contribution aligns with the project's goal of providing reliable Pinterest media downloading
4. Test your changes with various Pinterest URLs (pins, boards, profiles)

## Development Setup

### Local Development Environment

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```

3. Install development dependencies:
   ```bash
   pip install pytest pytest-cov black flake8 mypy
   ```

4. Create a new branch for your feature or improvement:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/scraping-issue-description
   # or
   git checkout -b ui/interface-improvement
   ```

### Running the Application

1. Start the Streamlit application:
   ```bash
   streamlit run src/main.py
   ```

2. Test with various Pinterest URLs:
   - Individual pins
   - Board URLs
   - Profile URLs
   - Different media types (images, videos)

### Development Tools

- **Code Formatting**: Use `black` for consistent code formatting
- **Linting**: Use `flake8` for code quality checks
- **Type Checking**: Use `mypy` for static type analysis
- **Testing**: Use `pytest` for running tests

## Coding Standards

### General Guidelines

- Write clean, readable, and well-documented Python code
- Follow PEP 8 style guidelines with Black formatting
- Use type hints for function parameters and return values
- Handle errors gracefully with proper exception handling
- Log important events and errors for debugging
- Respect Pinterest's robots.txt and rate limiting

### Python Standards

#### Code Style
- Use Black for automatic code formatting
- Maximum line length: 88 characters (Black default)
- Use meaningful variable and function names
- Add docstrings for all public functions and classes
- Follow PEP 8 naming conventions

#### Architecture Guidelines
- Separate concerns: UI logic in `ui.py`, scraping logic in `downloader.py`
- Use utility functions in `utils.py` for common operations
- Keep the main application entry point clean in `main.py`
- Implement proper error handling and user feedback

### Scraping Ethics and Guidelines

- **Respect Rate Limits**: Implement appropriate delays between requests
- **User-Agent Headers**: Use appropriate user-agent strings
- **Error Handling**: Handle HTTP errors, network timeouts, and parsing errors
- **Content Validation**: Verify downloaded content integrity
- **Legal Compliance**: Ensure scraping practices comply with terms of service

### Streamlit UI Guidelines

- **Responsive Design**: Ensure UI works on different screen sizes
- **Progress Feedback**: Show progress for long-running operations
- **Error Messages**: Display clear, actionable error messages
- **Input Validation**: Validate Pinterest URLs before processing
- **State Management**: Use Streamlit session state appropriately

## Testing Guidelines

### Test Structure

Tests are located in the `tests/` directory and should follow these patterns:

```python
# tests/test_downloader.py
import pytest
from src.app.downloader import PinterestDownloader

def test_url_validation():
    """Test Pinterest URL validation."""
    downloader = PinterestDownloader()
    assert downloader.is_valid_pinterest_url("https://pinterest.com/pin/123456")
    assert not downloader.is_valid_pinterest_url("https://invalid-url.com")

def test_media_extraction():
    """Test media extraction from Pinterest pages."""
    # Implementation details
    pass
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_downloader.py

# Run tests with verbose output
pytest -v
```

### Test Guidelines

- Write tests for all new functionality
- Test both success and failure scenarios
- Mock external API calls and network requests
- Test with various Pinterest URL formats
- Include edge cases and error conditions
- Maintain test coverage above 80%

## Commit Guidelines

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification for commit messages.

### Commit Message Format

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Types

- `feat`: A new feature (scraping capability, UI improvement)
- `fix`: A bug fix (scraping error, UI issue, download problem)
- `perf`: Performance improvements (faster scraping, memory optimization)
- `refactor`: Code refactoring without changing functionality
- `test`: Adding or updating tests
- `docs`: Documentation only changes
- `style`: Code style changes (formatting, etc.)
- `chore`: Maintenance tasks and dependency updates

### Scopes (Optional)

- `scraper`: Changes to scraping functionality
- `ui`: Streamlit interface changes
- `downloader`: Download mechanism changes
- `utils`: Utility functions
- `tests`: Test-related changes
- `docs`: Documentation changes

### Examples

```
feat(scraper): add support for Pinterest video downloads

fix(ui): resolve progress bar not updating during batch downloads

perf(downloader): optimize concurrent download processing

docs: update usage examples with new Pinterest URL formats

test(scraper): add comprehensive URL validation tests
```

## Pull Request Process

### Before Submitting

1. Ensure your branch is up to date with the main branch:
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. Run the full test suite:
   ```bash
   pytest
   ```

3. Check code formatting and linting:
   ```bash
   black src/ tests/
   flake8 src/ tests/
   mypy src/
   ```

4. Test the application manually with various Pinterest URLs

5. Update documentation if necessary

### Submitting Your Pull Request

1. Push your branch to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

2. Create a pull request from your fork to the main repository

3. Fill out the pull request template completely

4. Include testing information and sample Pinterest URLs used for testing

### Pull Request Checklist

- [ ] Code follows the project's coding standards
- [ ] Tests pass locally and cover new functionality
- [ ] Documentation has been updated (if applicable)
- [ ] Commit messages follow conventional commit format
- [ ] Changes have been tested with various Pinterest URL types
- [ ] No breaking changes (or breaking changes are documented)
- [ ] Performance impact has been considered
- [ ] Error handling has been implemented appropriately

## Issue Guidelines

### Before Creating an Issue

1. Search existing issues to avoid duplicates
2. Test with the latest version of the application
3. Gather relevant information (URLs, error messages, screenshots)
4. Try to reproduce the issue consistently

### Bug Reports

When reporting a scraping or download bug, please include:

- **Bug Description**: Clear and concise description of the issue
- **Pinterest URL**: The specific Pinterest URL that's causing issues
- **Steps to Reproduce**: Detailed steps to reproduce the issue
- **Expected Behavior**: What should happen
- **Actual Behavior**: What actually happens
- **Error Messages**: Any error messages or logs
- **Environment**: Operating system, Python version, browser (if relevant)
- **Screenshots**: UI screenshots showing the issue

### Feature Requests

When requesting a new feature, please include:

- **Feature Description**: Clear description of the proposed feature
- **Use Case**: Why is this feature needed? What problem does it solve?
- **Pinterest Context**: Which Pinterest features or URL types this relates to
- **Proposed Implementation**: Your ideas for how this could be implemented
- **Examples**: Examples from other scraping tools if applicable
- **Priority**: How important is this feature to you?

### Performance Issues

When reporting performance problems:

- **Performance Issue**: Description of the slowness or resource usage
- **Test URLs**: Pinterest URLs used for testing
- **System Specs**: Hardware specifications and available resources
- **Measurements**: Specific timing or memory usage measurements
- **Comparison**: Performance with different URL types or quantities
- **Proposed Solutions**: Any optimization ideas you might have

## Community

### Getting Help

If you need help or have questions:

- Open an issue with the "question" label
- Email us at [ujjwalkrai@gmail.com](mailto:ujjwalkrai@gmail.com)
- Check existing documentation in the `docs/` folder
- Review the [USAGE.md](USAGE.md) for detailed usage instructions

### Development Discussion

For development-related discussions:

- Use GitHub Discussions for general questions
- Comment on relevant issues for specific topics
- Join conversations in pull requests
- Follow our [Code of Conduct](CODE_OF_CONDUCT.md) in all interactions

### Recognition

We appreciate all contributions and maintain a contributors list to recognize everyone who has helped improve this project. Contributors will be acknowledged in our documentation and release notes.

## License

By contributing to this project, you agree that your contributions will be licensed under the MIT License, the same license as the project. See [LICENSE](../LICENSE) for details.

---

## Quick Reference

### Common Development Commands

```bash
# Setup
git clone https://github.com/your-username/pinterest-media-scraper.git
cd pinterest-media-scraper
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -e .

# Development
git checkout -b feature/new-scraping-feature
# Make your changes
black src/ tests/
flake8 src/ tests/
pytest
git add .
git commit -m "feat(scraper): add new Pinterest board scraping capability"
git push origin feature/new-scraping-feature

# Testing
pytest
pytest --cov=src
streamlit run src/main.py
```

### 📞 Support

- **📧 Email**: [ujjwalkrai@gmail.com](mailto:ujjwalkrai@gmail.com)
- **🐛 Issues**: [Repository Issues](https://github.com/uikraft-hub/pinterest-media-scraper/issues)
- **🔓 Security**: [Repository Security](https://github.com/uikraft-hub/pinterest-media-scraper/security)
- **⛏ Pull Requests**: [Repository Pull Requests](https://github.com/uikraft-hub/pinterest-media-scraper/pulls)
- **📖 Documentation**: [Repository Documentation](https://github.com/uikraft-hub/pinterest-media-scraper/tree/main/docs)
- **📃 Changelog**: [Repository Changelog](https://github.com/uikraft-hub/pinterest-media-scraper/blob/main/docs/CHANGELOG.md)

### Need Help?

If you're new to contributing or need assistance:

- Start by reviewing the existing code structure
- Test the application with different Pinterest URLs
- Begin with small improvements or bug fixes
- Don't hesitate to ask questions in issues or via email
- Check the [USAGE.md](USAGE.md) for application usage details

Thank you for contributing to Pinterest Media Scraper! Together, we're making Pinterest media downloading more accessible and reliable for everyone. 🎉