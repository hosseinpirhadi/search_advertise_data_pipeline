DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'advertise') THEN
        CREATE DATABASE advertise;
        RAISE NOTICE 'Database "advertise" created.';
    ELSE
        RAISE NOTICE 'Database "advertise" already exists.';
    END IF;
END $$;

\c advertise;

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'car_ad') THEN
        CREATE TABLE car_ad (
            id UUID PRIMARY KEY, -- DEFAULT uuid_generate_v1() PRIMARY KEY,
            code VARCHAR(50) NOT NULL,
            title VARCHAR(255),
            year VARCHAR(10),
            miles VARCHAR(50),
            date DATE,
            price VARCHAR(50)
        );
        RAISE NOTICE 'Table "car_ad" created.';
    ELSE
        RAISE NOTICE 'Table "car_ad" already exists.';
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'car_ad_archive') THEN
        CREATE TABLE car_ad_archive (
            id UUID PRIMARY KEY, -- DEFAULT uuid_generate_v1() PRIMARY KEY,
            code VARCHAR(50) NOT NULL,
            title VARCHAR(255),
            year VARCHAR(10),
            miles VARCHAR(50),
            date DATE,
            price VARCHAR(50)
        );
        RAISE NOTICE 'Table "car_ad_archive" created.';
    ELSE
        RAISE NOTICE 'Table "car_ad_archive" already exists.';
    END IF;
END $$;

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'public' AND table_name = 'ad_interaction') THEN
        CREATE TABLE ad_interaction (
            id UUID PRIMARY KEY, --DEFAULT uuid_generate_v1() PRIMARY KEY,
            type BOOLEAN,
            ad_id UUID REFERENCES car_ad(id),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            session_id UUID -- Assuming you meant UUID instead of UID
        );
        RAISE NOTICE 'Table "ad_interaction" created.';
    ELSE
        RAISE NOTICE 'Table "ad_interaction" already exists.';
    END IF;
END $$;
