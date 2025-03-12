DROP DATABASE IF EXISTS app_adm;
CREATE DATABASE app_adm;
USE app_adm;

-- Tabla: onboardings
CREATE TABLE onboardings (
    id INT PRIMARY KEY,
    name VARCHAR(255),
    status VARCHAR(50),
    title VARCHAR(255),
    description TEXT,
    color_config VARCHAR(255),
    allow_text_color_change BOOLEAN,
    allow_popups BOOLEAN,
);

-- Tabla: questions
CREATE TABLE questions (
    id INT PRIMARY KEY,
    title VARCHAR(255),
    description TEXT,
    type VARCHAR(50)
);

-- Tabla: question_options
CREATE TABLE question_options (
    id INT PRIMARY KEY,
    name VARCHAR(255),
    description TEXT,
    status VARCHAR(50),
    question_id INT,
    FOREIGN KEY (question_id) REFERENCES questions(id)
);

-- Tabla: onboarding_has_question (Tabla de unión)
CREATE TABLE onboarding_has_question (
    onboarding_id INT,
    question_id INT,
    PRIMARY KEY (onboarding_id, question_id),
    FOREIGN KEY (onboarding_id) REFERENCES onboardings(id),
    FOREIGN KEY (question_id) REFERENCES questions(id)
);