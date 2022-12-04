DROP SCHEMA IF EXISTS parking_data CASCADE;
CREATE SCHEMA parking_data;
/*
 SPOT STATE
 */
CREATE TYPE parking_data.SPOT_STATE_ENUM AS ENUM ('OCCUPIED', 'FREE', 'UNIDENTIFIED');
CREATE TABLE IF NOT EXISTS parking_data.spot_state_enum_table (value text, PRIMARY KEY(value));
INSERT INTO parking_data.spot_state_enum_table (value) (
        SELECT unnest(enum_range(NULL::parking_data.SPOT_STATE_ENUM))::text
    );
-- Spot
-- SpotState
-- Camera
-- User
-- Snapshot
-- UserAccess
CREATE TABLE IF NOT EXISTS parking_data.spots (
    id SERIAL NOT NULL,
    latitude VARCHAR(45) NOT NULL,
    longitude VARCHAR(45) NOT NULL,
    available INT,
    last_updated TIMESTAMP,
    PRIMARY KEY (id)
);
CREATE TABLE IF NOT EXISTS parking_data.camera(
    id SERIAL NOT NULL,
    latitude VARCHAR(45) NOT NULL,
    longitude VARCHAR(45) NOT NULL,
    last_updated TIMESTAMP NOT NULL,
    PRIMARY KEY (id)
);
CREATE TABLE IF NOT EXISTS parking_data.spots_camera(
    id SERIAL NOT NULL,
    spot_id SERIAL NOT NULL,
    camera_id SERIAL NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (spot_id) REFERENCES parking_data.spots(id),
    FOREIGN KEY (camera_id) REFERENCES parking_data.camera(id)
);
CREATE TABLE IF NOT EXISTS parking_data.users(
    id SERIAL NOT NULL,
    username VARCHAR(45) NOT NULL,
    password VARCHAR(1000) NOT NULL,
    PRIMARY KEY (id)
);
CREATE TABLE IF NOT EXISTS parking_data.snapshots(
    id SERIAL NOT NULL,
    spot_id SERIAL NOT NULL,
    camera_id SERIAL NOT NULL,
    image VARCHAR(2048) NOT NULL,
    last_updated TIMESTAMP NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (spot_id) REFERENCES parking_data.spots(id),
    FOREIGN KEY (camera_id) REFERENCES parking_data.camera(id)
);
CREATE TABLE IF NOT EXISTS parking_data.spot_state(
    id SERIAL NOT NULL,
    spot_id SERIAL NOT NULL,
    state text NOT NULL,
    last_updated TIMESTAMP NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (spot_id) REFERENCES parking_data.spots(id)
);
CREATE TABLE IF NOT EXISTS parking_data.snapshots_spot_state(
    id SERIAL NOT NULL,
    snapshot_id SERIAL NOT NULL,
    spot_state_id SERIAL NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (snapshot_id) REFERENCES parking_data.snapshots(id),
    FOREIGN KEY (spot_state_id) REFERENCES parking_data.spot_state(id)
);
CREATE TABLE IF NOT EXISTS parking_data.user_access(
    id SERIAL NOT NULL,
    longtitude_min VARCHAR(45) NOT NULL,
    longtitude_max VARCHAR(45) NOT NULL,
    latitude_min VARCHAR(45) NOT NULL,
    latitude_max VARCHAR(45) NOT NULL,
    end_time TIMESTAMP NOT NULL,
    user_id SERIAL NOT NULL,
    PRIMARY KEY (id)
);