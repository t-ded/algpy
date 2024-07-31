# AlgPy
AlgPy is the go-to learning tool for common Data Structures and Algorithms in Python.

What sets AlgPy apart from other DSA libraries:
* **AlgPy is first and foremost a *learning tool***.
  * Extensive lecture-like documentation
  * interactive Try-it-yourself options.
* **AlgPy is *highly modular***.
  * Need a Graph class? Just import it, no need to re-implement it for each new algorithm.
* **AlgPy is ruled by *Explainability >> Performance***
  * Native Python structures wherever possible.
* **AlgPy provides *LeetCode solutions***
  * Apply newly learned data structures and algorithms straight away to solve common LeetCode problems.

## Getting Started

1. **Clone the repository**
   ```sh
   git clone https://github.com/t-ded/algpy.git
   cd algpy
   ```

2. **(Optional but strongly recommended) Set up virtual environment**
   - **Using `venv`:**
     ```sh
     python -m venv venv  # Alternatively, use python3
     source venv/bin/activate  # On Windows use `venv\Scripts\activate`
     ```
   - **Using `conda`:**
     ```sh
     conda create --name algpy python=3.x  # Replace `3.x` with your desired Python version, preferably 3.12
     conda activate algpy
     ```

3. **Install dependencies**
   ```sh
   pip install -r algpy_src/requirements.txt
   ```

4. **Run tests**
   ```sh
   pytest
   ```

## Repository Structure
The algpy repository is organized to facilitate learning and contribution. Below is a brief explanation of the main directories and their purposes:

* ```.github/```: Contains GitHub-specific files such as workflows, issue templates, and contribution guidelines.
* ```algpy_src/```: The primary source directory for the project. This is where the main modules and implementations of data structures and algorithms reside.
    * ```algorithms/```: One of primary implementation folders, storing submodules such as ```graph_algorithms/```, ```sorting/``` etc.
    * ```base/```: Stores base objects used in other modules.
    * ```data_structures/```: One of primary implementation folders, storing submodules such as ```graphs/```, ```hash_based/``` etc.
    * ```tests/```: Includes unit tests for the project to ensure code reliability and correctness. Directory structure should match that of ```algpy_src/```.
    * ```tools/```: Utility functionalities for end-user experiments with provided algorithms and data structures. Provides tooling such as runtime analysis, input generation etc.
* ```docs/```: Contains documentation files. This includes detailed explanations of various data structures and algorithms, how-to guides, and other educational resources.
* ```examples/```: Provides example scripts demonstrating how to use the various data structures and algorithms implemented in algpy and how to try provided tools.

## Contributing
AlgPy has been meant as an open-sourced initiative since beginning. There are so many ways to contribute and none of them is less appreciated than any other -
here are some quickstart ideas (and you can find more detailed information in our [contributing guidelines](CONTRIBUTING.md)):

* Miss a data structure? Feel free to add it!
* Miss an algorithm? Feel free to add it! Think you can use an already implemented data structure for it? Even better.
Feel like there is a data structure you are missing and need to implement it? The best case!
* Have you tried an algorithm and the tools but found out you would be curious about some other feature inside? Add a new tool!
* Have you used AlgPy to solve a LeetCode problem? Present your solution!
* Do you miss an explanation somewhere in the docs or found a mistake in there? Let us know!

Before going forward with contributing, please read our [code of conduct](CODE_OF_CONDUCT.md).

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Project Structure
