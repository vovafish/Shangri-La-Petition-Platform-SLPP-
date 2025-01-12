# Shangri-La Petition Platform (SLPP)

## Prerequisites
- Python 3.x
- MySQL 8.0 or higher
- pip (Python package manager)

## Setup Instructions

1. **Get Project**:
   Open up the project and start from the root directory

2. **Create a Virtual Environment**:
   Create a virtual environment to manage dependencies in the root:
   ```bash
   python -m venv .venv
   ```

3. **Activate the Virtual Environment**:
   - **For Windows**:
     ```bash
     .venv\Scripts\activate
     ```
   - **For Unix/MacOS**:
     ```bash
     source .venv/bin/activate
     ```

4. **Install Python Dependencies**:
   Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

5. **Install Frontend Dependencies**:
   ```bash
   npm install
   ```
   or
   ```bash
   yarn install
   ```

6. **Set Up the Database**:
   - Import the SQL dump file `slpp_dump.sql` into your MySQL database using MySQL Workbench or the command line:
   ```bash
   mysql -u newuser -p slpp < slpp_dump.sql
   ```

7. **Update Database Credentials**:
   Open the `slpp/slpp/settings.py` file and update the database credentials (lines 85-93):
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'slpp',  
           'USER': 'newuser', 
           'PASSWORD': 'newpassword', 
           'HOST': '127.0.0.1', 
           'PORT': '3306', 
       }
   }
   ```

8. **Run Migrations** (if necessary, refer to the next step, Step 9):
   If you have any migrations to apply, run:
   DO IT FROM THE slpp/ NOT root
   ```bash
   python manage.py migrate
   ```

9. **Run the Development Server** 
    ! (If when you run the sever it prompts you a message about having
    unresolved migration please do Step 8.) ! :
    DO IT FROM THE slpp/ NOT root
   Start the Django development server:
   ```bash
   python manage.py runserver
   ```

10. **Access the Application**:
    Open your web browser and go to: [http://127.0.0.1:8000]


## Testing Credentials
For testing purposes, use the following credentials:

### Petitioner Credentials
- **Email:** forgrading@gmail.com
- **Password:** forgrading

### Admin Credentials
- **Username (Email):** admin@petition.parliament.sr
- **Password:** 2025%shangrila


**Note:** You must use the specific login endpoint for logging in as admin: `/slpp/petitions/admin/login/` or access it via the button in the header.

## Troubleshooting
If you encounter any issues during setup, feel free to contact me for assistance.