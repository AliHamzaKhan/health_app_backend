


CREATE_USER_SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
            id VARCHAR(36) PRIMARY KEY,
            phone_no VARCHAR(15),
            email VARCHAR(255),
            ai_tokens INTEGER,
            user_type_id INTEGER,
            token VARCHAR(255),
            fcm_token VARCHAR(255)  
        )
"""

CHECK_USER_SCHEMA = """
 SELECT * FROM users WHERE phone_no = COALESCE($1, phone_no) OR email = COALESCE($2, email)
"""

INSERT_USER_SCHEMA = """
INSERT INTO users (id, phone_no, email, ai_tokens, user_type_id, token, fcm_token)
                    VALUES ($1, $2, $3, $4, $5, $6, $7)
"""

UPDATE_USER_TOKEN_SCHEMA = """
    UPDATE users SET token = $1 WHERE id = $2
"""

CREATE_PROFILE_SCHEMA = """
CREATE TABLE IF NOT EXISTS profiles (
    id VARCHAR(250) PRIMARY KEY,         -- id can be optional but it's a primary key
    first_name VARCHAR(50),              -- Optional fields can still have a default size in SQL
    last_name VARCHAR(50),
    email VARCHAR(100) UNIQUE NOT NULL,  -- Email is required and unique
    phone_no VARCHAR(15) UNIQUE NOT NULL,  -- Phone number is required and unique
    dob VARCHAR(50),                     -- Optional date of birth
    country VARCHAR(50),
    city VARCHAR(50),
    gender CHAR(10),
    profile_image TEXT,
    is_verified BOOLEAN NOT NULL,        -- This must be provided
    package_id INT NOT NULL,             -- Required field
    total_usage FLOAT DEFAULT 0.0,       -- Default value of 0.0 for total_usage
    user_type_id INT NOT NULL            -- Required field
);
"""

INSERT_PROFILE_SCHEMA = """
INSERT INTO profiles (id, first_name, last_name, email, phone_no, dob, country, city, gender, profile_image, is_verified, package_id, total_usage, user_type_id)
    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14)
    ON CONFLICT (id) DO UPDATE SET
        first_name = EXCLUDED.first_name,
        last_name = EXCLUDED.last_name,
        email = EXCLUDED.email,
        phone_no = EXCLUDED.phone_no,
        dob = EXCLUDED.dob,
        country = EXCLUDED.country,
        city = EXCLUDED.city,
        gender = EXCLUDED.gender,
        profile_image = EXCLUDED.profile_image,
        is_verified = EXCLUDED.is_verified,
        package_id = EXCLUDED.package_id,
        total_usage = EXCLUDED.total_usage,
        user_type_id = EXCLUDED.user_type_id;
"""

FIND_PROFILE_ID_SCHEMA = """
SELECT * FROM profiles WHERE id = $1;
"""

UPDATE_PROFILE_PACKAGE_ID_SCHEMA = """
    UPDATE profiles SET package_id = $1 WHERE id = $2
"""

CREATE_DATA_PROCESS_SCHEMA = """
CREATE TABLE IF NOT EXISTS data_process (
                id VARCHAR(255) PRIMARY KEY,
                user_id VARCHAR(255),
                prompt TEXT,
                image_url TEXT,
                token_used INTEGER,
                ai_generated_text JSONB,
                request_type VARCHAR(50),
                created_at TIMESTAMP DEFAULT NOW()
            );
"""

INSERT_DATA_PROCESS_SCHEMA = """
INSERT INTO data_process (id, user_id, prompt, image_url, token_used, ai_generated_text, request_type, created_at)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
            ON CONFLICT (id) DO UPDATE SET
                user_id = EXCLUDED.user_id,
                prompt = EXCLUDED.prompt,
                image_url = EXCLUDED.image_url,
                token_used = EXCLUDED.token_used,
                ai_generated_text = EXCLUDED.ai_generated_text,
                request_type = EXCLUDED.request_type;
"""

FIND_DATA_PROCESS_SCHEMA = """
SELECT id, user_id, prompt, image_url, ai_generated_text, request_type, token_used, created_at
            FROM data_process 
            WHERE user_id = $1
"""

CREATE_DOCTOR_SCHEMA = """
CREATE TABLE IF NOT EXISTS doctors (
                id VARCHAR(250) PRIMARY KEY,
                name VARCHAR(100),
                email VARCHAR(100),
                degree VARCHAR(100),
                age VARCHAR(100),
                phone_no VARCHAR(100),
                gender VARCHAR(100),
                address VARCHAR(100),
                hospitals VARCHAR(100),
                specialization VARCHAR(100),
                experience VARCHAR(100),
                image VARCHAR(100),
                availability VARCHAR(100),
            )
"""

INSERT_DOCTOR_SCHEME = """
INSERT INTO doctors (id, name, email, degree, age, phone_no, gender, address, hospitals, specialization, 
                                experience, image, availability)
           VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13)
"""

FIND_DOCTOR_SPECIALITY_SCHEMA = """
 SELECT * FROM doctors 
                   WHERE EXISTS (
                       SELECT 1 FROM unnest(string_to_array(specialization, ',')) AS specialization_item
                       WHERE TRIM(specialization_item) ILIKE TRIM($1)
                   )
"""

FIND_ALL_DOCTOR_SCHEMA = """
SELECT * FROM doctors
"""

FIND_DOCTOR_BY_ID_SCHEMA = """
SELECT * FROM doctors WHERE id = $1
"""

FIND_DOCTOR_IN_HOSPITAL_SCHEMA = """
SELECT * FROM doctors
            WHERE $1 = ANY(string_to_array(hospitals, ','))
"""

CREATE_HOSPITAL_SCHEME = """
 CREATE TABLE IF NOT EXISTS hospitals (
           id VARCHAR(250) PRIMARY KEY,
           name VARCHAR(100),
           address TEXT,
           phone_number VARCHAR(15),
           email VARCHAR(100) UNIQUE,
           website VARCHAR(100),
           type VARCHAR(50),
           departments TEXT[],  -- Array of strings
           latlng VARCHAR(50),
           img TEXT,
           staff_count INT
       );
"""

INSERT_HOSPITAL_SCHEMA = """
INSERT INTO hospitals (id, name, address, phone_number, email, website, type, departments, latlng, img, staff_count)
       VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
       ON CONFLICT (email) DO UPDATE SET
           id = EXCLUDED.id,
           name = EXCLUDED.name,
           address = EXCLUDED.address,
           phone_number = EXCLUDED.phone_number,
           website = EXCLUDED.website,
           type = EXCLUDED.type,
           departments = EXCLUDED.departments,
           latlng = EXCLUDED.latlng,
           img = EXCLUDED.img,
           staff_count = EXCLUDED.staff_count;
"""

FIND_HOSPITAL_IN_CITY_SCHEMA = """
SELECT * FROM hospitals WHERE city = $1
"""

FIND_HOSPITAL_VALUES_SCHEMA = """
SELECT id, name, latlng FROM hospitals
"""

CREATE_DEPARTMENTS_SCHEMA = """
CREATE TABLE IF NOT EXISTS departments (
    department_id SERIAL PRIMARY KEY,
    department_name VARCHAR(36) NOT NULL
);
"""

FIND_DEPARTMENTS_SCHEMA = """
select * from departments
"""

INSERT_DEPARTMENTS_SCHEMA = """
INSERT INTO departments (department_name) VALUES ($1)
"""


CREATE_MEDICAL_SPECIALITIES_SCHEMA = """
    CREATE TABLE IF NOT EXISTS medical_specialities (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
    ); 
"""

INSERT_MEDICAL_SPECIALITIES_SCHEMA = """
    INSERT INTO medical_specialities (name) VALUES ($1)
"""

FIND_MEDICAL_SPECIALITIES_SCHEMA = """
SELECT * FROM medical_specialities
"""

FIND_MEDICAL_SPECIALITIES_NAME_SCHEMA = """
SELECT name FROM medical_specialities
"""