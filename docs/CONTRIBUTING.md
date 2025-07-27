# Contributing to yt-downloader-gui

Thank you for your interest in contributing to yt-downloader-gui! We welcome contributions from everyone and appreciate your help in making this PyQt6-based media downloader better for the community.

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
- Basic knowledge of PyQt6 applications
- Understanding of YouTube's structure and media handling

### First Time Setup

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/your-username/yt-downloader-gui.git
   cd yt-downloader-gui
   ```
3. Add the upstream repository:
   ```bash
   git remote add upstream https://github.com/uikraft-hub/yt-downloader-gui.git
   ```
4. Install the project in development mode:
   ```bash
   pip install -r requirements.txt
   ```

## How to Contribute

### Types of Contributions

We welcome several types of contributions:

- **Core Functionality**: Enhance media downloading capabilities and features.
- **UI/UX Improvements**: Improve the PyQt6 interface and user experience.
- **Performance Optimization**: Optimize download speed and memory usage.
- **Error Handling**: Improve error handling and user feedback mechanisms.
- **Testing**: Add comprehensive tests for downloading and UI functionality.
- **Documentation**: Improve guides, API documentation, and usage examples.
- **Bug Reports**: Help us identify and fix downloading or UI issues.
- **Feature Requests**: Suggest new YouTube media sources or download options.

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
   ```

3. Create a new branch for your feature or improvement:
   ```bash
   git checkout -b feature/your-feature-name
   ```

### Running the Application

1. Start the application:
   ```bash
   python src/main.py
   ```

2. Test with various YouTube URLs:
   - Individual videos
   - Playlist URLs
   - Channel URLs
   - Different media types (video, audio)

## Coding Standards

### General Guidelines

- Write clean, readable, and well-documented Python code.
- Follow PEP 8 style guidelines.
- Use type hints for function parameters and return values.
- Handle errors gracefully with proper exception handling.
- Log important events and errors for debugging.
- Respect YouTube's terms of service.

## Testing Guidelines

### Test Structure

Tests are located in the `tests/` directory.

### Running Tests

```bash
# Run all tests
pytest
```

## Commit Guidelines

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification for commit messages.

### Examples

```
feat(downloader): add support for YouTube video downloads
fix(ui): resolve progress bar not updating during batch downloads
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

### Submitting Your Pull Request

1. Push your branch to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

2. Create a pull request from your fork to the main repository.

## Issue Guidelines

### Bug Reports

When reporting a bug, please include:

- **Bug Description**: Clear and concise description of the issue.
- **YouTube URL**: The specific YouTube URL that's causing issues.
- **Steps to Reproduce**: Detailed steps to reproduce the issue.
- **Expected Behavior**: What should happen.
- **Actual Behavior**: What actually happens.
- **Error Messages**: Any error messages or logs.

### Feature Requests

When requesting a new feature, please include:

- **Feature Description**: Clear description of the proposed feature.
- **Use Case**: Why is this feature needed? What problem does it solve?

## Community

### Getting Help

If you need help or have questions:

- Open an issue with the "question" label.
- Email us at [ujjwalkrai@gmail.com](mailto:ujjwalkrai@gmail.com).

## License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.
