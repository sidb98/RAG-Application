# Offline-RAG

# Project Setup and Run Instructions

This project consists of two main components:

1. **Django Backend** (located in the main directory)
2. **React Frontend** (located in the `client` directory)

### Running the Django Backend

To start the Django backend, follow these steps:

1. **Navigate to the main directory** (where `manage.py` is located):

   ```bash
   cd /path/to/your/project
   ```
2. Install requirement.txt
   ```bash
   cd backend && pip install -r requirements.txt 
   ```
3. Come back to root of project
    ```bash
   cd ../
   ```
4. Apply migrations (if there are any)
   ```bash
   python manage.py migrate
   ```
5. Run the Django server
   ```bash
   python manage.py runserver
   ```
   
### Running the Django Backend
1. Navigate to the client directory:
    ```bash
   python manage.py runserver
   ```
2. Install the required npm packages :
    ```bash
   npm install
    ```
3. Run the React server:
   ```bash
   npm start

   ```
