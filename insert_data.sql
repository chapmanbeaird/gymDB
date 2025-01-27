-- Insert data into member table
INSERT INTO member (member_id, name, join_date) VALUES
(1, 'Alice Johnson', '2025-01-01'),
(2, 'Bob Smith', '2025-01-05'),
(3, 'Charlie Brown', '2025-01-10'),
(4, 'Diana Prince', '2025-01-15'),
(5, 'Ethan Hunt', '2025-01-20');

-- Insert data into phone table
INSERT INTO phone (phone_id, member_id, area_code, number, can_receive_sms) VALUES
(1, 1, 123, 4567890, 1),
(2, 2, 234, 5678901, 0),
(3, 3, 345, 6789012, 1),
(4, 4, 456, 7890123, 1),
(5, 5, 567, 8901234, 0);

-- Insert data into membership_plan table
INSERT INTO membership_plan (plan_id, name, price, duration_in_months) VALUES
(1, 'Basic Plan', 30.00, 1),
(2, 'Standard Plan', 50.00, 3),
(3, 'Premium Plan', 120.00, 6);

-- Insert data into member_membership table
INSERT INTO member_membership (membership_id, member_id, plan_id, start_date, end_date) VALUES
(1, 1, 1, '2025-01-01', '2025-02-01'),
(2, 2, 2, '2025-01-05', '2025-04-05'),
(3, 3, 3, '2025-01-10', '2025-07-10'),
(4, 4, 2, '2025-01-15', '2025-04-15'),
(5, 5, 1, '2025-01-20', '2025-02-20');

-- Insert data into gym_class table
INSERT INTO gym_class (class_id, name, description) VALUES
(1, 'Yoga', 'A relaxing yoga class focusing on flexibility and breathing'),
(2, 'HIIT', 'High-intensity interval training for cardiovascular health'),
(3, 'Strength Training', 'Focus on building strength with weights and resistance'),
(4, 'Zumba', 'Dance-based workout for fun and fitness'),
(5, 'Pilates', 'Core-focused workout to improve stability and posture');

-- Insert data into class_attendance table
INSERT INTO class_attendance (attendance_id, member_id, class_id, attendance_date) VALUES
(1, 1, 1, '2025-01-05'),
(2, 1, 2, '2025-01-12'),
(3, 2, 3, '2025-01-15'),
(4, 3, 4, '2025-01-18'),
(5, 4, 5, '2025-01-20'),
(6, 5, 1, '2025-01-25');
