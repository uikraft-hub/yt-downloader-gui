# Contributing to Youtube-Media-Downloader

Thank you for your interest in contributing to Youtube-Media-Downloader! This document provides guidelines and information for contributors to help make the development process smooth and effective.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contributing Guidelines](#contributing-guidelines)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting](#issue-reporting)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Community](#community)

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct:

- Be respectful and inclusive to all contributors
- Use welcoming and constructive language
- Focus on what's best for the community and project
- Show empathy towards other community members
- Accept constructive criticism gracefully

## Getting Started

### Prerequisites

Before contributing, ensure you have:

- Python 3.8 or higher
- Git installed and configured
- Basic knowledge of PyQt6 and Python GUI development
- Understanding of yt-dlp and media downloading concepts

### Development Setup

1. **Fork the Repository**
   ```bash
   # Fork the repo on GitHub, then clone your fork
   git clone https://github.com/UKR-PROJECTS/Youtube-Media-Downloader.git
   cd Youtube-Media-Downloader
   ```

2. **Set Up Development Environment**
   ```bash
   # Create and activate virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Verify Installation**
   ```bash
   # Run the application to ensure everything works
   python src/main.py
   ```

4. **Set Up Upstream Remote**
   ```bash
   git remote add upstream https://github.com/UKR-PROJECTS/Youtube-Media-Downloader.git
   ```

## Contributing Guidelines

### Types of Contributions

We welcome various types of contributions:

- **Bug Fixes**: Fix existing issues or problems
- **Feature Enhancements**: Add new functionality or improve existing features
- **UI/UX Improvements**: Enhance the user interface and experience
- **Performance Optimizations**: Improve application speed and responsiveness
- **Documentation**: Improve README, add code comments, or create tutorials
- **Testing**: Add unit tests, integration tests, or fix test-related issues

### Before You Start

1. **Check Existing Issues**: Browse [existing issues](https://github.com/UKR-PROJECTS/Youtube-Media-Downloader/issues) to see if your idea or bug report already exists
2. **Create an Issue**: For major changes, create an issue first to discuss your proposed changes
3. **Get Feedback**: Wait for maintainer feedback on significant features before implementing

## Pull Request Process

### 1. Create a Feature Branch

```bash
# Sync with upstream
git fetch upstream
git checkout main
git merge upstream/main

# Create feature branch
git checkout -b feature/awesome-feature
# or for bug fixes:
git checkout -b fix/issue-description
```

### 2. Make Your Changes

- Write clean, readable code following our [coding standards](#coding-standards)
- Add comments for complex logic
- Update documentation if needed
- Test your changes thoroughly

### 3. Commit Your Changes

```bash
# Stage your changes
git add .

# Commit with clear, descriptive message
git commit -m "Add awesome feature: brief description

- Detailed explanation of what was added/changed
- Why the change was necessary
- Any breaking changes or migration notes"
```

### 4. Push and Create Pull Request

```bash
# Push to your fork
git push origin feature/awesome-feature
```

Then create a Pull Request on GitHub with:

- **Clear Title**: Summarize the change in 50 characters or less
- **Detailed Description**: Explain what, why, and how
- **Screenshots**: Include before/after screenshots for UI changes
- **Testing Information**: Describe how you tested the changes
- **Related Issues**: Reference any related issues (e.g., "Fixes #123")

### Pull Request Requirements

- [ ] Code follows project coding standards
- [ ] Changes have been tested locally
- [ ] Documentation updated (if applicable)
- [ ] No merge conflicts with main branch
- [ ] Commit messages are clear and descriptive
- [ ] Screenshots included for UI changes

## Issue Reporting

### Bug Reports

When reporting bugs, please include:

- **Environment Information**:
  - Operating System and version
  - Python version
  - PyQt6 version
  - Application version
  
- **Steps to Reproduce**:
  1. Clear, numbered steps
  2. Expected behavior
  3. Actual behavior
  
- **Additional Context**:
  - Error messages or logs
  - Screenshots or screen recordings
  - URLs that cause issues (if applicable)

### Feature Requests

For feature requests, provide:

- **Use Case**: Why is this feature needed?
- **Proposed Solution**: How should it work?
- **Alternatives**: Any alternative solutions considered?
- **Implementation Ideas**: Technical approach (if you have ideas)

## Coding Standards

### Python Code Style

- Follow [PEP 8](https://pep8.org/) style guidelines
- Use 4 spaces for indentation (no tabs)
- Maximum line length: 88 characters (Black formatter standard)
- Use meaningful variable and function names

### PyQt6 Specific Guidelines

- Use descriptive names for UI components (`download_button` instead of `btn1`)
- Organize UI code logically with proper separation of concerns
- Use Qt's signal-slot mechanism appropriately
- Handle threading properly for UI responsiveness

### Code Organization

```python
# File structure example for new modules
"""
Brief module description.

Longer description if needed.
"""

import sys
import os
from pathlib import Path

from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import QThread, pyqtSignal


class YourClass:
    """Class docstring."""
    
    def __init__(self):
        """Initialize the class."""
        pass
    
    def public_method(self):
        """Public method docstring."""
        pass
    
    def _private_method(self):
        """Private method docstring."""
        pass
```

### Error Handling

- Use appropriate exception handling
- Provide meaningful error messages to users
- Log errors appropriately for debugging
- Don't expose sensitive information in error messages

## Testing

### Manual Testing

Before submitting changes:

1. **Basic Functionality**: Test core download features
2. **UI Interactions**: Verify all buttons, menus, and dialogs work
3. **Cross-Platform**: Test on different operating systems (if possible)
4. **Edge Cases**: Test with various YouTube URLs and formats

### Automated Testing

While the project doesn't currently have automated tests, consider:

- Adding unit tests for utility functions
- Creating integration tests for download workflows
- Testing UI components with Qt Test framework

## Documentation

### Code Documentation

- Add docstrings to all classes and public methods
- Use inline comments for complex logic
- Keep comments up-to-date with code changes

### User Documentation

- Update README.md for new features
- Add screenshots for UI changes
- Document any new configuration options
- Update installation instructions if dependencies change

## Community

### Getting Help

- **GitHub Issues**: Ask questions or report problems
- **Discussions**: Use GitHub Discussions for general questions
- **Pull Request Comments**: Get code review feedback

### Communication Guidelines

- Be patient and respectful
- Provide context when asking questions
- Search existing issues before creating new ones
- Use clear, descriptive titles for issues and PRs

## Release Process

The project maintainers handle releases, but contributors should:

- Ensure changes are backward compatible when possible
- Document any breaking changes clearly
- Update version numbers in relevant files (if applicable)

## Attribution

Contributors will be acknowledged in:

- GitHub's contributor statistics
- Release notes for significant contributions
- Special recognition for major features or fixes

---

Thank you for contributing to Youtube-Media-Downloader! Your efforts help make this tool better for everyone. If you have questions about these guidelines, feel free to open an issue for discussion.
