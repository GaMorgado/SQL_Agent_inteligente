-- init-db.sql (Ajustado)
--
-- PostgreSQL database dump
--

-- Dumped from database version 17.5
-- Dumped by pg_dump version 17.5

-- Started on 2025-06-05 11:26:10

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
-- SET transaction_timeout = 0; -- REMOVIDO/COMENTADO - Causava erro no PostgreSQL 15
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

-- O comando CREATE DATABASE e ALTER DATABASE para "Verity_project" foram removidos
-- pois o Docker entrypoint já cria o banco definido em POSTGRES_DB.

\connect "Verity_project"

-- Configurações de sessão para a conexão com "Verity_project"
SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
-- SET transaction_timeout = 0; -- REMOVIDO/COMENTADO - Causava erro no PostgreSQL 15
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 223 (class 1259 OID 24624)
-- Name: checkpoint_blobs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.checkpoint_blobs (
    thread_id text NOT NULL,
    checkpoint_ns text DEFAULT ''::text NOT NULL,
    channel text NOT NULL,
    version text NOT NULL,
    type text NOT NULL,
    blob bytea
);


ALTER TABLE public.checkpoint_blobs OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 24610)
-- Name: checkpoint_migrations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.checkpoint_migrations (
    v integer NOT NULL
);


ALTER TABLE public.checkpoint_migrations OWNER TO postgres;

--
-- TOC entry 224 (class 1259 OID 24632)
-- Name: checkpoint_writes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.checkpoint_writes (
    thread_id text NOT NULL,
    checkpoint_ns text DEFAULT ''::text NOT NULL,
    checkpoint_id text NOT NULL,
    task_id text NOT NULL,
    idx integer NOT NULL,
    channel text NOT NULL,
    type text,
    blob bytea NOT NULL,
    task_path text DEFAULT ''::text NOT NULL
);


ALTER TABLE public.checkpoint_writes OWNER TO postgres;

--
-- TOC entry 222 (class 1259 OID 24615)
-- Name: checkpoints; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.checkpoints (
    thread_id text NOT NULL,
    checkpoint_ns text DEFAULT ''::text NOT NULL,
    checkpoint_id text NOT NULL,
    parent_checkpoint_id text,
    type text,
    checkpoint jsonb NOT NULL,
    metadata jsonb DEFAULT '{}'::jsonb NOT NULL
);


ALTER TABLE public.checkpoints OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 16443)
-- Name: clientes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.clientes (
    id_cliente integer NOT NULL,
    nome_cliente text NOT NULL,
    saldo integer NOT NULL,
    saldo_gasto integer DEFAULT 0
);


ALTER TABLE public.clientes OWNER TO postgres;

--
-- TOC entry 218 (class 1259 OID 16451)
-- Name: produtos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.produtos (
    id_produto integer NOT NULL,
    product_name character varying(30) NOT NULL,
    descricao text,
    preco numeric NOT NULL,
    qtd_disponivel integer DEFAULT 0 NOT NULL,
    CONSTRAINT produtos_preco_check CHECK ((preco > (0)::numeric))
);


ALTER TABLE public.produtos OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 16461)
-- Name: transacoes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.transacoes (
    id_transacao integer NOT NULL,
    data_transacao timestamp without time zone DEFAULT now() NOT NULL,
    qtde integer,
    client_id integer NOT NULL,
    produto_id integer NOT NULL
);


ALTER TABLE public.transacoes OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 16460)
-- Name: transacoes_id_transacao_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.transacoes_id_transacao_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.transacoes_id_transacao_seq OWNER TO postgres;

--
-- TOC entry 4948 (class 0 OID 0)
-- Dependencies: 219
-- Name: transacoes_id_transacao_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.transacoes_id_transacao_seq OWNED BY public.transacoes.id_transacao;


--
-- TOC entry 4761 (class 2604 OID 16464)
-- Name: transacoes id_transacao; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transacoes ALTER COLUMN id_transacao SET DEFAULT nextval('public.transacoes_id_transacao_seq'::regclass);


--
-- TOC entry 4939 (class 0 OID 24624)
-- Dependencies: 223
-- Data for Name: checkpoint_blobs; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 4937 (class 0 OID 24610)
-- Dependencies: 221
-- Data for Name: checkpoint_migrations; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 4940 (class 0 OID 24632)
-- Dependencies: 224
-- Data for Name: checkpoint_writes; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 4938 (class 0 OID 24615)
-- Dependencies: 222
-- Data for Name: checkpoints; Type: TABLE DATA; Schema: public; Owner: postgres
--



--
-- TOC entry 4933 (class 0 OID 16443)
-- Dependencies: 217
-- Data for Name: clientes; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.clientes VALUES (1, 'Carlos Silva', 1000, 3500) ON CONFLICT DO NOTHING;
INSERT INTO public.clientes VALUES (2, 'Ana Pereira', 1500, 300) ON CONFLICT DO NOTHING;
INSERT INTO public.clientes VALUES (3, 'João Souza', 2000, 400) ON CONFLICT DO NOTHING;


--
-- TOC entry 4934 (class 0 OID 16451)
-- Dependencies: 218
-- Data for Name: produtos; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.produtos VALUES (1, 'Notebook', 'Notebook Dell i5, 8GB RAM, 256GB SSD', 3500.00, 10) ON CONFLICT DO NOTHING;
INSERT INTO public.produtos VALUES (2, 'Mouse Gamer', 'Mouse óptico RGB', 150.00, 50) ON CONFLICT DO NOTHING;
INSERT INTO public.produtos VALUES (3, 'Teclado Mecânico', 'Teclado mecânico com iluminação', 400.00, 30) ON CONFLICT DO NOTHING;


--
-- TOC entry 4936 (class 0 OID 16461)
-- Dependencies: 220
-- Data for Name: transacoes; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.transacoes VALUES (1, '2025-06-03 17:30:00.375771', 1, 1, 1) ON CONFLICT DO NOTHING;
INSERT INTO public.transacoes VALUES (2, '2025-06-03 17:30:00.375771', 2, 2, 2) ON CONFLICT DO NOTHING;
INSERT INTO public.transacoes VALUES (3, '2025-06-03 17:30:00.375771', 1, 3, 3) ON CONFLICT DO NOTHING;


--
-- TOC entry 4949 (class 0 OID 0)
-- Dependencies: 219
-- Name: transacoes_id_transacao_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.transacoes_id_transacao_seq', 3, true);


--
-- TOC entry 4781 (class 2606 OID 24631)
-- Name: checkpoint_blobs checkpoint_blobs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.checkpoint_blobs
    ADD CONSTRAINT checkpoint_blobs_pkey PRIMARY KEY (thread_id, checkpoint_ns, channel, version);


--
-- TOC entry 4776 (class 2606 OID 24614)
-- Name: checkpoint_migrations checkpoint_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.checkpoint_migrations
    ADD CONSTRAINT checkpoint_migrations_pkey PRIMARY KEY (v);


--
-- TOC entry 4784 (class 2606 OID 24639)
-- Name: checkpoint_writes checkpoint_writes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.checkpoint_writes
    ADD CONSTRAINT checkpoint_writes_pkey PRIMARY KEY (thread_id, checkpoint_ns, checkpoint_id, task_id, idx);


--
-- TOC entry 4778 (class 2606 OID 24623)
-- Name: checkpoints checkpoints_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.checkpoints
    ADD CONSTRAINT checkpoints_pkey PRIMARY KEY (thread_id, checkpoint_ns, checkpoint_id);


--
-- TOC entry 4770 (class 2606 OID 16450)
-- Name: clientes clientes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clientes
    ADD CONSTRAINT clientes_pkey PRIMARY KEY (id_cliente);


--
-- TOC entry 4772 (class 2606 OID 16459)
-- Name: produtos produtos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.produtos
    ADD CONSTRAINT produtos_pkey PRIMARY KEY (id_produto);


--
-- TOC entry 4774 (class 2606 OID 16467)
-- Name: transacoes transacoes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transacoes
    ADD CONSTRAINT transacoes_pkey PRIMARY KEY (id_transacao);


--
-- TOC entry 4782 (class 1259 OID 24641)
-- Name: checkpoint_blobs_thread_id_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX checkpoint_blobs_thread_id_idx ON public.checkpoint_blobs USING btree (thread_id);


--
-- TOC entry 4785 (class 1259 OID 24642)
-- Name: checkpoint_writes_thread_id_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX checkpoint_writes_thread_id_idx ON public.checkpoint_writes USING btree (thread_id);


--
-- TOC entry 4779 (class 1259 OID 24640)
-- Name: checkpoints_thread_id_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX checkpoints_thread_id_idx ON public.checkpoints USING btree (thread_id);


--
-- TOC entry 4786 (class 2606 OID 16468)
-- Name: transacoes transacoes_client_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transacoes
    ADD CONSTRAINT transacoes_client_id_fkey FOREIGN KEY (client_id) REFERENCES public.clientes(id_cliente);


--
-- TOC entry 4787 (class 2606 OID 16473)
-- Name: transacoes transacoes_produto_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transacoes
    ADD CONSTRAINT transacoes_produto_id_fkey FOREIGN KEY (produto_id) REFERENCES public.produtos(id_produto);


-- Completed on 2025-06-05 11:26:10

--
-- PostgreSQL database dump complete
--