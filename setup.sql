-- Table for gym members
CREATE TABLE member (
    member_id INTEGER PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    join_date DATE NOT NULL
);

-- Table for phone numbers (optional for SMS tracking)
CREATE TABLE phone (
    phone_id INTEGER PRIMARY KEY,
    member_id INTEGER NOT NULL,
    area_code INT NOT NULL,
    number INT NOT NULL,
    can_receive_sms TINYINT NOT NULL,
    FOREIGN KEY (member_id) REFERENCES member (member_id)
);

-- Table for membership plans
CREATE TABLE membership_plan (
    plan_id INTEGER PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    duration_in_months INT NOT NULL
);

-- Table for member memberships
CREATE TABLE member_membership (
    membership_id INTEGER PRIMARY KEY,
    member_id INTEGER NOT NULL,
    plan_id INTEGER NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    FOREIGN KEY (member_id) REFERENCES member (member_id),
    FOREIGN KEY (plan_id) REFERENCES membership_plan (plan_id)
);

-- Table for gym classes
CREATE TABLE gym_class (
    class_id INTEGER PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description VARCHAR(255)
);

-- Table for class attendance
CREATE TABLE class_attendance (
    attendance_id INTEGER PRIMARY KEY,
    member_id INTEGER NOT NULL,
    class_id INTEGER NOT NULL,
    attendance_date DATE NOT NULL,
    FOREIGN KEY (member_id) REFERENCES member (member_id),
    FOREIGN KEY (class_id) REFERENCES gym_class (class_id)
);