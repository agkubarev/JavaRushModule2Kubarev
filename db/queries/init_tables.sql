CREATE TABLE IF NOT EXISTS images (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(255),
    original_name VARCHAR(255),
    size integer,
    file_type VARCHAR(255),
    upload_time timestamp DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO images (filename, original_name, size, file_type)
VALUES
    ('image1.jpg', 'Image 1', 12345, 'jpg'),
    ('image2.jpg', 'Image 2', 54321, 'jpg');