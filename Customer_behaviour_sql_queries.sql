DROP TABLE customer;

CREATE TABLE customer (
    "Customer ID" INTEGER,
    "Age" INTEGER,
    "Gender" VARCHAR(20),
    "Item Purchased" VARCHAR(100),
    "Category" VARCHAR(100),
    "Purchase Amount (USD)" NUMERIC(10,2),
    "Location" VARCHAR(100),
    "Size" VARCHAR(20),
    "Color" VARCHAR(50),
    "Season" VARCHAR(20),
    "Review Rating" NUMERIC(3,1),
    "Subscription Status" VARCHAR(10),
    "Shipping Type" VARCHAR(50),
    "Discount Applied" VARCHAR(10),
    "Promo Code Used" VARCHAR(10),
    "Previous Purchases" INTEGER,
    "Payment Method" VARCHAR(50),
    "Frequency of Purchases" VARCHAR(50)
);

SELECT * FROM customer; 

select * from customer limit 20;