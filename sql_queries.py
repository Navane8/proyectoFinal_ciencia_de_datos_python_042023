DDL_QUERY =  '''
CREATE TABLE IF NOT EXISTS review(
    reviewsk INT PRIMARY KEY,
    review_id VARCHAR(32) UNIQUE,
    review_score INT NOT NULL,
    review_comment_message VARCHAR(210)    
);

CREATE TABLE IF NOT EXISTS product(
    productsk INT PRIMARY KEY,
    product_id VARCHAR(32) UNIQUE,
    product_width_cm FLOAT,
    product_length_cm FLOAT,
    product_height_cm FLOAT,
    product_weight_g FLOAT    
);

CREATE TABLE IF NOT EXISTS orderhead(
    ordersk INT PRIMARY KEY,
    order_id VARCHAR(32) UNIQUE,
    order_status VARCHAR(12)    
);


CREATE TABLE IF NOT EXISTS customer(
    customersk INT PRIMARY KEY,
    customer_id VARCHAR(32) UNIQUE,
    name VARCHAR(25),
    email VARCHAR(45),
    phone VARCHAR(25),
    customer_city VARCHAR(45),
    customer_state VARCHAR(4)
   
);

CREATE TABLE IF NOT EXISTS seller(
    sellersk INT PRIMARY KEY,
    seller_id VARCHAR(32) UNIQUE,
    name VARCHAR(25),
    email VARCHAR(45),
    phone VARCHAR(25),
    seller_city VARCHAR(45),
    seller_state VARCHAR(4)
);

CREATE TABLE IF NOT EXISTS detalle(
    id_detalle SERIAL PRIMARY KEY,
    price DOUBLE PRECISION,
    order_item_id INT,
    order_id VARCHAR(32),

    productsk INT,
    sellersk INT,
    productcatesk INT,


    CONSTRAINT fk_sellersk
        FOREIGN KEY (sellersk)
            REFERENCES seller(sellersk),


    CONSTRAINT fk_productsk
        FOREIGN KEY (productsk)
            REFERENCES product(productsk)

);

CREATE TABLE IF NOT EXISTS encabezado(
    id_encabezado SERIAL PRIMARY KEY,
    order_purchase_timestamp VARCHAR(25),
    payment_value DOUBLE PRECISION,
    order_id VARCHAR(32),

    ordersk INT,
    customersk INT,
    paymentsk INT,
    reviewsk INT,


    CONSTRAINT fk_enordersk
        FOREIGN KEY (ordersk)
            REFERENCES orderhead(ordersk),

    CONSTRAINT fk_encustomersk
        FOREIGN KEY (customersk)
            REFERENCES customer(customersk),

    CONSTRAINT fk_enreviewsk
        FOREIGN KEY (reviewsk)
            REFERENCES review(reviewsk)

);



 '''