CREATE TABLE manufacturer (
    make_id SERIAL PRIMARY KEY,
    make VARCHAR(25) UNIQUE NOT NULL
);

CREATE TABLE body_type (
    body_type_id SERIAL PRIMARY KEY,
    body_type VARCHAR(25) UNIQUE NOT NULL
);

CREATE TABLE fuel_type (
    fuel_type_id SERIAL PRIMARY KEY,
    fuel_type VARCHAR(25) UNIQUE NOT NULL
);

CREATE TABLE transmission_type (
    transmission_type_id SERIAL PRIMARY KEY,
    transmission_type VARCHAR(25) UNIQUE NOT NULL
);

CREATE TABLE transmission (
    transmission_id SERIAL PRIMARY KEY,
    transmission VARCHAR(25) UNIQUE NOT NULL
);

CREATE TABLE emission (
    emission_id SERIAL PRIMARY KEY,
    emission VARCHAR(25) UNIQUE NOT NULL
);

CREATE TABLE color (
    color_id SERIAL PRIMARY KEY,
    color VARCHAR(25) UNIQUE NOT NULL
);

CREATE TABLE car (
    car_id SERIAL PRIMARY KEY,
    car_name VARCHAR(225),
    model VARCHAR(25),
    make_year SMALLINT,
    mileage_run INTEGER,
    no_of_owners VARCHAR(5),
    seating_capacity SMALLINT,
    fuel_tank_capacity_l SMALLINT,
    engine_type VARCHAR(225),
    cc_displacement SMALLINT,
    power_bhp FLOAT,
    torque_nm FLOAT,
    mileage_kmpl FLOAT,
    price FLOAT,
    make_id INTEGER,
    body_type_id INTEGER,
    fuel_type_id INTEGER,
    transmission_type_id INTEGER,
    transmission_id INTEGER,
    emission_id INTEGER,
    color_id INTEGER,
    foreign key (make_id) references manufacturer (make_id),
    foreign key (body_type_id) references body_type (body_type_id),
    foreign key (fuel_type_id) references fuel_type (fuel_type_id),
    foreign key (transmission_type_id) references transmission_type (transmission_type_id),
    foreign key (transmission_id) references transmission (transmission_id),
    foreign key (emission_id) references emission (emission_id),
    foreign key (color_id) references color (color_id)
);