CREATE TABLE onboardings (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    status INT DEFAULT 1,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    metadata JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE onboarding_questions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    type VARCHAR(50),
    onboarding_id INT NOT NULL,
    metadata JSON,
    status INT DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (onboarding_id) REFERENCES onboardings(id)
);

CREATE TABLE onboarding_options (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    status INT DEFAULT 1,
    question_id INT NOT NULL,
    metadata JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (question_id) REFERENCES onboarding_questions(id)
);

CREATE TABLE onboarding_users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    birth_date DATE NOT NULL,
    phone VARCHAR(20) NOT NULL,
    country VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    document_type VARCHAR(50) NOT NULL,
    document_number VARCHAR(50) NOT NULL,
    metadata JSON,
    status INT DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE onboarding_answers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    onboarding_id INT NOT NULL,
    question_id INT NOT NULL,
    option_id INT,
    answer_text TEXT NOT NULL,
    metadata JSON,
    status INT DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (onboarding_id) REFERENCES onboardings(id),
    FOREIGN KEY (question_id) REFERENCES onboarding_questions(id),
    FOREIGN KEY (user_id) REFERENCES onboarding_users(id)
);

CREATE TABLE onboarding_transactions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    onboarding_id INT,
    plan_name VARCHAR(50),
    total DECIMAL(10, 2) NOT NULL,
    payment_reference VARCHAR(50) NOT NULL,
    payment_status VARCHAR(50) NOT NULL,
    bank_name VARCHAR(50) NOT NULL,
    gateway_name VARCHAR(100) NOT NULL,
    gateway_response TEXT NOT NULL,
    tokenization_id INT NOT NULL,
    tokenization_source VARCHAR(100) NOT NULL,
    metadata JSON,
    status INT DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES onboarding_users(id),
    FOREIGN KEY (onboarding_id) REFERENCES onboardings(id)
);

CREATE INDEX idx_onboarding_answers_user_id ON onboarding_answers (user_id);
CREATE INDEX idx_onboarding_answers_onboarding_id ON onboarding_answers (onboarding_id);
CREATE INDEX idx_onboarding_answers_question_id ON onboarding_answers (question_id);
CREATE INDEX idx_onboarding_transactions_user_id ON onboarding_transactions (user_id);