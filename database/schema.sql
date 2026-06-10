
-- CREATION DE LA TABLE USERS 

-- Table: public.USERS

-- DROP TABLE IF EXISTS public."USERS";

CREATE TABLE IF NOT EXISTS public."USERS"
(
    id_users integer NOT NULL DEFAULT nextval('"USERS_id_users_seq"'::regclass),
    name text COLLATE pg_catalog."default" NOT NULL,
    surname text COLLATE pg_catalog."default" NOT NULL,
    phone_number numeric(9,0) NOT NULL,
    national_card text COLLATE pg_catalog."default" NOT NULL,
    account_type account_type NOT NULL,
    password text COLLATE pg_catalog."default" NOT NULL,
    created_at time with time zone NOT NULL DEFAULT now(),
    CONSTRAINT "USERS_pkey" PRIMARY KEY (id_users)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."USERS"
    OWNER to postgres;









-- CREATION DE LA TABLE WALLETS


-- Table: public.WALLETS

-- DROP TABLE IF EXISTS public."WALLETS";

CREATE TABLE IF NOT EXISTS public."WALLETS"
(
    id_wallets integer NOT NULL DEFAULT nextval('"WALLETS_id_wallets_seq"'::regclass),
    balance numeric(15,2) NOT NULL,
    currency text COLLATE pg_catalog."default" NOT NULL DEFAULT 'XAF'::text,
    daily_limit numeric(15,2) NOT NULL DEFAULT 100000,
    id_users integer NOT NULL,
    CONSTRAINT "WALLETS_pkey" PRIMARY KEY (id_wallets),
    CONSTRAINT fk_wallets_users FOREIGN KEY (id_users)
        REFERENCES public."USERS" (id_users) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."WALLETS"
    OWNER to postgres;








-- CREATION DE LA TABLE TRANSACTIONS

-- Table: public.TRANSACTIONS

-- DROP TABLE IF EXISTS public."TRANSACTIONS";

CREATE TABLE IF NOT EXISTS public."TRANSACTIONS"
(
    id_transactions integer NOT NULL DEFAULT nextval('"TRANSACTIONS_id_transactions_seq"'::regclass),
    balance numeric(15,2) NOT NULL DEFAULT 0,
    currency text COLLATE pg_catalog."default" NOT NULL DEFAULT 'XAF'::text,
    status status_transac NOT NULL,
    sended_at time with time zone NOT NULL DEFAULT now(),
    received_at time with time zone,
    id_wallet_sender integer NOT NULL,
    id_wallet_receiver integer NOT NULL,
    CONSTRAINT "TRANSACTIONS_pkey" PRIMARY KEY (id_transactions),
    CONSTRAINT fk_wallet_receiver FOREIGN KEY (id_wallet_receiver)
        REFERENCES public."WALLETS" (id_wallets) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT fk_wallet_sender FOREIGN KEY (id_wallet_sender)
        REFERENCES public."WALLETS" (id_wallets) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."TRANSACTIONS"
    OWNER to postgres;









-- CREATION DE LA TABLE AUDIT_LOGS

-- Table: public.AUDIT_LOGS

-- DROP TABLE IF EXISTS public."AUDIT_LOGS";

CREATE TABLE IF NOT EXISTS public."AUDIT_LOGS"
(
    id_log integer NOT NULL DEFAULT nextval('"AUDIT_LOGS_id_log_seq"'::regclass),
    action_type action_type_audit NOT NULL,
    status status_audit NOT NULL DEFAULT 'normal'::status_audit,
    ip_adress text COLLATE pg_catalog."default" NOT NULL,
    localisation text COLLATE pg_catalog."default",
    id_user integer NOT NULL,
    created_at time with time zone DEFAULT now(),
    CONSTRAINT "AUDIT_LOGS_pkey" PRIMARY KEY (id_log)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."AUDIT_LOGS"
    OWNER to postgres;









-- ENUMERATIONS


-- Enum Account_type

-- Type: account_type

-- DROP TYPE IF EXISTS public.account_type;

CREATE TYPE public.account_type AS ENUM
    ('standard', 'commercant', 'agent');

ALTER TYPE public.account_type
    OWNER TO postgres;





--Enum action_type_audit

-- Type: action_type_audit

-- DROP TYPE IF EXISTS public.action_type_audit;

CREATE TYPE public.action_type_audit AS ENUM
    ('connexion', 'deconnexion', 'mauvais mot de passe', 'compte bloque', 'modification profil');

ALTER TYPE public.action_type_audit
    OWNER TO postgres;










--Enum currency 


-- Type: currency

-- DROP TYPE IF EXISTS public.currency;

CREATE TYPE public.currency AS ENUM
    ('XAF', 'XOF', 'EUR', 'USD');

ALTER TYPE public.currency
    OWNER TO postgres;






--Enum status_audit

-- Type: status_audit

-- DROP TYPE IF EXISTS public.status_audit;

CREATE TYPE public.status_audit AS ENUM
    ('normal', 'suspect');

ALTER TYPE public.status_audit
    OWNER TO postgres;




-- Enum status_transac

-- Type: status_transac

-- DROP TYPE IF EXISTS public.status_transac;

CREATE TYPE public.status_transac AS ENUM
    ('Echouée', 'En cours', 'Validée', 'Suspecte');

ALTER TYPE public.status_transac
    OWNER TO postgres;
