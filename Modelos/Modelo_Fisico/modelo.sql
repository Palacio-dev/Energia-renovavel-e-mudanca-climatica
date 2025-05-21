BEGIN;


CREATE TABLE IF NOT EXISTS public."AREA"
(
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    nome character varying(50) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public."MES"
(
    id character varying(10) NOT NULL,
    numero bigint NOT NULL,
    id_ano bigint NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public."ANO"
(
    id bigint NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public."MUD_TEMP"
(
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    mud_value double precision,
    desvio_padrao double precision,
    id_area bigint NOT NULL,
    id_mes character varying(10) NOT NULL,
    id_ano bigint NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public."GERACAO_ENERGIA"
(
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    unidade_geracao character varying(10),
    valor_geracao double precision,
    unidade_emissao character varying(10),
    valor_emissao double precision,
    id_area bigint NOT NULL,
    id_ano bigint NOT NULL,
    id_tipo bigint NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public."TIPO_ENERGIA"
(
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    valor character varying(50),
    renovavel boolean,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public."PAIS"
(
    id bigint NOT NULL,
    codigo character varying(10) NOT NULL,
    nome character varying(50) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public."GRUPO"
(
    id bigint NOT NULL,
    codigo character varying(10) NOT NULL,
    nome character varying(50) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public."PAIS_GRUPO"
(
    "Pais_id" bigint NOT NULL,
    "Grupo_id" bigint NOT NULL
);

ALTER TABLE IF EXISTS public."MES"
    ADD FOREIGN KEY (id_ano)
    REFERENCES public."ANO" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public."MUD_TEMP"
    ADD FOREIGN KEY (id_area)
    REFERENCES public."AREA" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public."MUD_TEMP"
    ADD FOREIGN KEY (id_mes)
    REFERENCES public."MES" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public."MUD_TEMP"
    ADD FOREIGN KEY (id_ano)
    REFERENCES public."ANO" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public."GERACAO_ENERGIA"
    ADD FOREIGN KEY (id_area)
    REFERENCES public."AREA" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public."GERACAO_ENERGIA"
    ADD FOREIGN KEY (id_ano)
    REFERENCES public."ANO" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public."GERACAO_ENERGIA"
    ADD FOREIGN KEY (id_tipo)
    REFERENCES public."TIPO_ENERGIA" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public."PAIS"
    ADD FOREIGN KEY (id)
    REFERENCES public."AREA" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public."GRUPO"
    ADD FOREIGN KEY (id)
    REFERENCES public."AREA" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public."PAIS_GRUPO"
    ADD FOREIGN KEY ("Pais_id")
    REFERENCES public."PAIS" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public."PAIS_GRUPO"
    ADD FOREIGN KEY ("Grupo_id")
    REFERENCES public."GRUPO" (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;

END;