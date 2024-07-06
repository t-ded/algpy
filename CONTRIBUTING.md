# Contributing to AlgPy

AlgPy is an open source project built by algorithm enthusiasts. Contribute and benefit by learning through practice:

- Starting with open source? What better project to choose than one with immense diversity and plethora of independent little parts such as distinct algorithms or data structures? **AlgPy is the place to start!**
- Switching to Python? You already know the algorithms; now see them in Python! **AlgPy is the place to start!**
- Preparing for coding interviews with LeetCode? Deepen your understanding by adding your solutions to AlgPy and get feedback. **AlgPy is the place to start!**
- Struggling with abstract fundamental concepts? Go wild comparing and visualising different algorithms in a notebook to see their pros and cons. **AlgPy is the place to start!**

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Features](#suggesting-features)
  - [Improving Documentation and example usage](#improving-documentation-and-example-usage)
- [Tiny Little Bits for Starting Right Away](#tiny-simple-bits-for-starting-right-away)
- [Contributing Steps](#contributing-steps)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Style Guide](#style-guide)
- [License](#license)

## Code of Conduct

Please read our [Code of Conduct](CODE_OF_CONDUCT.md) before participating.

## How Can I Contribute?

### Reporting Bugs

If you find a bug, please open an issue and provide detailed information. Include:
- A descriptive title and a detailed explanation of the bug.
- Steps to reproduce the issue.
- Expected and actual results.
- Any other relevant pieces of information.

### Suggesting Features

We welcome feature suggestions! To propose a new feature:
- Open an issue with a clear title and description.
- Explain why the feature would benefit users.
- Provide examples and use cases.
- Point to relevant sources (e.g., papers) if necessary.

### Improving Documentation and example usage

Help us improve our documentation by:
- Fixing typos or errors.
- Adding new examples or explanations.
- Updating outdated information.
- Adding walkthrough notebooks

## Tiny Simple Bits for Starting Right Away

If you want to start immediately but do not have any idea how, here are few ideas to spark your imagination:
- Implement a hashing algorithm - these typically have 0 dependencies and prerequisites.
- Pick a sorting algorithm, search algorithm or string manipulation algorithm - these also tend to not have many prerequisites. 
- Add a simple data structure that you like.
- Pick an algorithm you like and explore it in a notebook. Add a comparison to its concurrents.
- Select a LeetCode question that you think might be solvable with an algorithm from our database and solve it.
- Contribute to the documentation by adding examples, fixing typos or errors, or explaining complex algorithms.

## Contributing Steps

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.
6. Enjoy a discussion over any possible changes to your contribution.

## Development Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/t-ded/algpy.git
    cd algpy
    ```

2. (Optional but recommended) Set up a virtual environment:
    ```bash
    python -m venv venv  # or use conda
    source venv/bin/activate  # on Windows: venv\Scripts\activate
    ```

3. Install dependencies:
    ```bash
    pip install -r algpy_src/requirements.txt
    ```

4. Run tests to ensure everything is set up correctly:
    ```bash
    pytest
    ```

## Pull Request Process

1. Ensure your code follows the project’s [Style Guide](#style-guide).
2. Write clear, concise commit messages.
3. Update documentation if necessary.
4. Ensure all tests pass before submitting.
5. Submit your pull request and fill out the template provided.

## Style Guide

- Follow PEP 8 for Python code.
- Use meaningful variable and function names.
- Write comments and docstrings for clarity.
- Keep functions and classes small and focused.
- Make sure that your subclass is implementing all necessary abstract methods.
- Add tests if you are implementing a new functionality or found one that did not work before.

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).
