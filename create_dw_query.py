CREATE_DW = '''
create table if not exists dimcustomer(
	dimcustomerpk INT PRIMARY KEY,
    customer_id VARCHAR(32) UNIQUE,
    name VARCHAR(25),
    email VARCHAR(45),
    phone VARCHAR(25),
    customer_city VARCHAR(45),
    customer_state VARCHAR(4)
);

create table if not exists dimseller(
    dimsellerpk INT PRIMARY KEY,
    seller_id VARCHAR(32) UNIQUE,
    name VARCHAR(25),
    email VARCHAR(45),
    phone VARCHAR(25),
    seller_city VARCHAR(45),
    seller_state VARCHAR(4)
);

create table if not exists dimorder(
    dimorderpk INT PRIMARY KEY,
    order_id VARCHAR(32) UNIQUE,
    order_status VARCHAR(12)  
);

create table if not exists dimpaymentype(
    dimpaymentpk INT PRIMARY KEY,
    payment_type VARCHAR(20) UNIQUE
);

create table if not exists dimproductcate(
    dimproductcatepk INT PRIMARY KEY,
    product_category_name VARCHAR(20) UNIQUE 
);

create table if not exists dimproduct(
    dimproductpk INT PRIMARY KEY,
    product_id VARCHAR(32) UNIQUE,
    product_width_cm FLOAT,
    product_length_cm FLOAT,
    product_height_cm FLOAT,
    product_weight_g FLOAT 
);

create table if not exists dimreview(
    dimreviewpk INT PRIMARY KEY,
    review_id VARCHAR(32) UNIQUE,
    review_score INT NOT NULL,
    review_comment_message VARCHAR(210) 
);

create table if not exists dimcalendar(
	dimfechapk VARCHAR(25) primary key,
	year INT,
	month INT,
	quarter INT,
	week INT,
	dayofweek INT,
	hour INT, 
	minute INT, 
	is_weekend INT,
	order_purchase_timestamp DATETIME
);

CREATE TABLE IF NOT EXISTS factable(
    id_registro SERIAL PRIMARY KEY,
    dimfechafk VARCHAR(30),
    price DOUBLE PRECISION,
    payment_value DOUBLE PRECISION,
    order_item_id INT,

    dimorderfk INT,
    dimcustomerfk INT,
    dimpaymentfk INT,
    dimreviewfk INT,
    dimproductfk INT,
    dimsellerfk INT,
    dimproductcatefk INT,

    CONSTRAINT fk_dimorderfk
        FOREIGN KEY (dimorderfk)
            REFERENCES dimorder(dimorderpk),

    CONSTRAINT fk_dimcustomerfk
        FOREIGN KEY (dimcustomerfk)
            REFERENCES dimcustomer(dimcustomerpk),

    CONSTRAINT fk_dimsellerfk
        FOREIGN KEY (dimsellerfk)
            REFERENCES dimseller(dimsellerpk),

    CONSTRAINT fk_dimreviewfk
        FOREIGN KEY (dimreviewfk)
            REFERENCES dimreview(dimreviewpk),

    CONSTRAINT fk_dimproductfk
        FOREIGN KEY (dimproductfk)
            REFERENCES dimproduct(dimproductpk),
    
    CONSTRAINT fk_dimpaymentfk
        FOREIGN KEY (dimpaymentfk)
            REFERENCES dimpaymentype(dimpaymentpk),
            
    CONSTRAINT fk_dimproductcatefk
        FOREIGN KEY (dimproductcatefk)
            REFERENCES dimproductcate(dimproductcatepk),
            
    CONSTRAINT fk_dimfechafk
        FOREIGN KEY (dimfechafk)
            REFERENCES dimcalendar(dimfechapk)

);

'''
