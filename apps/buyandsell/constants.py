# Below are the categories
CATEGORY = (
    ('EL', 'Electronics'),
    ('BK', 'Books'),
    ('MS', 'Miscellaneous'),
    )

#Below are the sub categories corresponding to above categories

SUB_CATEGORY = {
'BK' : (('ED', 'Education'),  ('CS', 'Course Books'), ('FC', 'Fiction'), ('OT', 'Other'),),
'EL' : (('LP', 'Computer Accessories'), ('MO', 'Mobile Accessories'), ('OT', 'Other'),),
'MS' : (('TR', 'Trunks'), ('BC','Bicycles'), ('OT', 'Other'),)
}

EMPTY = (
    ('LP', 'Laptop'),
    ('MO', 'Mobiles'),
    ('ED', 'Education'),
    ('FC','Fiction'),
    ('BC', 'Bicycles'),
    ('TR', 'Trunks'),
    ('OT', 'Others'),
    ('CS', 'Course Books'),
)
MAX_NO_OF_DAYS = 2

STATUS = (
    ('Excellent', 'Excellent'),
    ('Good', 'Good'),
    ('Fine','Fine'),
    ('Old','Old'),
    )

EXPIRY = (
    (10, '10'),
    (15, '15'),
    (20, '20'),
    (25, '25'),
    (30, '30'),
    (45, '45'),
    (60, '60'),
    )
