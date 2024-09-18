Getting Started
===============

Installation
------------

#. **Clone the repository**

   .. code-block:: console

      $ git clone https://github.com/t-ded/algpy.git
      $ cd algpy
#. **(Optional but strongly recommended) Set up virtual environment**

   #. **Using `venv`:**

      .. code-block:: console

         $ python -m venv venv  # Alternatively, use python3
         $ source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   #. **Using `conda`:**

      .. code-block:: console

         $ conda create --name algpy python=3.x  # Replace `3.x` with your desired Python version, preferably 3.12
         $ conda activate algpy
#. **Install dependencies**

   .. code-block:: console

      $ (venv) pip install -r algpy_src/requirements.txt
#. **Run tests**

   .. code-block:: console

      $ (venv) pytest