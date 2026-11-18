--
-- PostgreSQL database dump
--

\restrict hqfYFe5qQa0rWVl0tr8ChYJZ1xomaG8iZbepLabthFv2BTRt5y9I0oUnA9TRxtr

-- Dumped from database version 16.16 (Debian 16.16-1.pgdg12+1)
-- Dumped by pg_dump version 16.16 (Debian 16.16-1.pgdg12+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: vector; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS vector WITH SCHEMA public;


--
-- Name: EXTENSION vector; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION vector IS 'vector data type and ivfflat and hnsw access methods';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: documents; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.documents (
    id integer NOT NULL,
    filename character varying(255) NOT NULL,
    file_path character varying(512) NOT NULL,
    file_type character varying(32) NOT NULL,
    file_size_bytes integer NOT NULL,
    status character varying(64) NOT NULL,
    error_message text,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


ALTER TABLE public.documents OWNER TO postgres;

--
-- Name: documents_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.documents_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.documents_id_seq OWNER TO postgres;

--
-- Name: documents_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.documents_id_seq OWNED BY public.documents.id;


--
-- Name: extracted_invoices; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.extracted_invoices (
    id integer NOT NULL,
    document_id integer NOT NULL,
    invoice_number character varying(128),
    invoice_date date,
    supplier_name character varying(255),
    customer_name character varying(255),
    subtotal numeric(12,2),
    tax numeric(12,2),
    total_amount numeric(12,2),
    currency character varying(16),
    line_items jsonb NOT NULL,
    is_manually_corrected boolean NOT NULL,
    raw_text text,
    embedding public.vector(384)
);


ALTER TABLE public.extracted_invoices OWNER TO postgres;

--
-- Name: extracted_invoices_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.extracted_invoices_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.extracted_invoices_id_seq OWNER TO postgres;

--
-- Name: extracted_invoices_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.extracted_invoices_id_seq OWNED BY public.extracted_invoices.id;


--
-- Name: validation_logs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.validation_logs (
    id integer NOT NULL,
    document_id integer NOT NULL,
    rule_name character varying(128) NOT NULL,
    error_description text NOT NULL,
    severity character varying(32) NOT NULL,
    created_at timestamp without time zone NOT NULL
);


ALTER TABLE public.validation_logs OWNER TO postgres;

--
-- Name: validation_logs_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.validation_logs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.validation_logs_id_seq OWNER TO postgres;

--
-- Name: validation_logs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.validation_logs_id_seq OWNED BY public.validation_logs.id;


--
-- Name: documents id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.documents ALTER COLUMN id SET DEFAULT nextval('public.documents_id_seq'::regclass);


--
-- Name: extracted_invoices id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.extracted_invoices ALTER COLUMN id SET DEFAULT nextval('public.extracted_invoices_id_seq'::regclass);


--
-- Name: validation_logs id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.validation_logs ALTER COLUMN id SET DEFAULT nextval('public.validation_logs_id_seq'::regclass);


--
-- Data for Name: documents; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.documents (id, filename, file_path, file_type, file_size_bytes, status, error_message, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: extracted_invoices; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.extracted_invoices (id, document_id, invoice_number, invoice_date, supplier_name, customer_name, subtotal, tax, total_amount, currency, line_items, is_manually_corrected, raw_text, embedding) FROM stdin;
\.


--
-- Data for Name: validation_logs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.validation_logs (id, document_id, rule_name, error_description, severity, created_at) FROM stdin;
\.


--
-- Name: documents_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.documents_id_seq', 8, true);


--
-- Name: extracted_invoices_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.extracted_invoices_id_seq', 8, true);


--
-- Name: validation_logs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.validation_logs_id_seq', 1, false);


--
-- Name: documents documents_file_path_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.documents
    ADD CONSTRAINT documents_file_path_key UNIQUE (file_path);


--
-- Name: documents documents_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.documents
    ADD CONSTRAINT documents_pkey PRIMARY KEY (id);


--
-- Name: extracted_invoices extracted_invoices_document_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.extracted_invoices
    ADD CONSTRAINT extracted_invoices_document_id_key UNIQUE (document_id);


--
-- Name: extracted_invoices extracted_invoices_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.extracted_invoices
    ADD CONSTRAINT extracted_invoices_pkey PRIMARY KEY (id);


--
-- Name: validation_logs validation_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.validation_logs
    ADD CONSTRAINT validation_logs_pkey PRIMARY KEY (id);


--
-- Name: idx_supplier_invoice_num; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_supplier_invoice_num ON public.extracted_invoices USING btree (supplier_name, invoice_number);


--
-- Name: ix_documents_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_documents_id ON public.documents USING btree (id);


--
-- Name: ix_documents_status; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_documents_status ON public.documents USING btree (status);


--
-- Name: ix_extracted_invoices_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_extracted_invoices_id ON public.extracted_invoices USING btree (id);


--
-- Name: ix_extracted_invoices_invoice_number; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_extracted_invoices_invoice_number ON public.extracted_invoices USING btree (invoice_number);


--
-- Name: ix_extracted_invoices_supplier_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_extracted_invoices_supplier_name ON public.extracted_invoices USING btree (supplier_name);


--
-- Name: ix_validation_logs_document_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_validation_logs_document_id ON public.validation_logs USING btree (document_id);


--
-- Name: ix_validation_logs_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX ix_validation_logs_id ON public.validation_logs USING btree (id);


--
-- Name: extracted_invoices extracted_invoices_document_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.extracted_invoices
    ADD CONSTRAINT extracted_invoices_document_id_fkey FOREIGN KEY (document_id) REFERENCES public.documents(id) ON DELETE CASCADE;


--
-- Name: validation_logs validation_logs_document_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.validation_logs
    ADD CONSTRAINT validation_logs_document_id_fkey FOREIGN KEY (document_id) REFERENCES public.documents(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict hqfYFe5qQa0rWVl0tr8ChYJZ1xomaG8iZbepLabthFv2BTRt5y9I0oUnA9TRxtr

