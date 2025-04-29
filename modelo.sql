BEGIN;


CREATE TABLE IF NOT EXISTS public."ANO"
(
    id bigint NOT NULL,
    CONSTRAINT "ANO_pkey" PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public."AREA"
(
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    nome character varying(50) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT "AREA_pkey" PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public."GERACAO_ENERGIA"
(
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    unidade_geracao character varying(10),
    valor_geracao double precision,
    unidade_emissao character varying(10),
    "valor_emissao_CO2" double precision,
    id_tipo bigint NOT NULL,
    id_area bigint NOT NULL,
    id_ano bigint NOT NULL,
    CONSTRAINT "GERACAO_ENERGIA_pkey" PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public."GRUPO"
(
    id bigint NOT NULL,
    codigo character varying(10) COLLATE pg_catalog."default" NOT NULL,
    nome character varying(50) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT "GRUPO_pkey" PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public."MES"
(
    id character varying(10) COLLATE pg_catalog."default" NOT NULL,
    numero bigint NOT NULL,
    id_ano bigint NOT NULL,
    CONSTRAINT "MES_pkey" PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public."MUD_TEMP"
(
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    mud_value double precision,
    desvio_padrao double precision,
    id_area bigint NOT NULL,
    id_mes character varying(10) COLLATE pg_catalog."default" NOT NULL,
    id_ano bigint NOT NULL,
    CONSTRAINT "MUD_TEMP_pkey" PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public."PAIS"
(
    id bigint NOT NULL,
    codigo character varying(10) COLLATE pg_catalog."default" NOT NULL,
    nome character varying(50) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT "PAIS_pkey" PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public."Pais_Grupo"
(
    "Pais_id" bigint NOT NULL,
    "Grupo_id" bigint NOT NULL
);

CREATE TABLE IF NOT EXISTS public."TIPO_ENERGIA"
(
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 9223372036854775807 CACHE 1 ),
    valor character varying(50) COLLATE pg_catalog."default",
    renovavel boolean,
    CONSTRAINT "TIPO_ENERGIA_pkey" PRIMARY KEY (id)
);

ALTER TABLE IF EXISTS public."GERACAO_ENERGIA"
    ADD CONSTRAINT "GERACAO_ENERGIA_id_ano_fkey" FOREIGN KEY (id_ano)
    REFERENCES public."ANO" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public."GERACAO_ENERGIA"
    ADD CONSTRAINT "GERACAO_ENERGIA_id_area_fkey" FOREIGN KEY (id_area)
    REFERENCES public."AREA" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public."GERACAO_ENERGIA"
    ADD CONSTRAINT "GERACAO_ENERGIA_id_tipo_fkey" FOREIGN KEY (id_tipo)
    REFERENCES public."TIPO_ENERGIA" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public."GRUPO"
    ADD CONSTRAINT "GRUPO_id_fkey" FOREIGN KEY (id)
    REFERENCES public."AREA" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;
CREATE INDEX IF NOT EXISTS "GRUPO_pkey"
    ON public."GRUPO"(id);


ALTER TABLE IF EXISTS public."MES"
    ADD CONSTRAINT "MES_id_ano_fkey" FOREIGN KEY (id_ano)
    REFERENCES public."ANO" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public."MUD_TEMP"
    ADD CONSTRAINT "MUD_TEMP_id_ano_fkey" FOREIGN KEY (id_ano)
    REFERENCES public."ANO" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public."MUD_TEMP"
    ADD CONSTRAINT "MUD_TEMP_id_area_fkey" FOREIGN KEY (id_area)
    REFERENCES public."AREA" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public."MUD_TEMP"
    ADD CONSTRAINT "MUD_TEMP_id_mes_fkey" FOREIGN KEY (id_mes)
    REFERENCES public."MES" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public."PAIS"
    ADD CONSTRAINT "PAIS_id_fkey" FOREIGN KEY (id)
    REFERENCES public."AREA" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;
CREATE INDEX IF NOT EXISTS "PAIS_pkey"
    ON public."PAIS"(id);


ALTER TABLE IF EXISTS public."Pais_Grupo"
    ADD CONSTRAINT "Pais_Grupo_Grupo_id_fkey" FOREIGN KEY ("Grupo_id")
    REFERENCES public."GRUPO" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public."Pais_Grupo"
    ADD CONSTRAINT "Pais_Grupo_Pais_id_fkey" FOREIGN KEY ("Pais_id")
    REFERENCES public."PAIS" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;

END;