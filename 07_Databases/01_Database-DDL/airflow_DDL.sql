-- DROP SCHEMA public;

CREATE SCHEMA public AUTHORIZATION airflow;

COMMENT ON SCHEMA public IS 'standard public schema';

-- DROP SEQUENCE public.ab_permission_id_seq;

CREATE SEQUENCE public.ab_permission_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.ab_permission_view_id_seq;

CREATE SEQUENCE public.ab_permission_view_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.ab_permission_view_role_id_seq;

CREATE SEQUENCE public.ab_permission_view_role_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.ab_register_user_id_seq;

CREATE SEQUENCE public.ab_register_user_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.ab_role_id_seq;

CREATE SEQUENCE public.ab_role_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.ab_user_id_seq;

CREATE SEQUENCE public.ab_user_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.ab_user_role_id_seq;

CREATE SEQUENCE public.ab_user_role_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.ab_view_menu_id_seq;

CREATE SEQUENCE public.ab_view_menu_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.callback_request_id_seq;

CREATE SEQUENCE public.callback_request_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.connection_id_seq;

CREATE SEQUENCE public.connection_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.dag_pickle_id_seq;

CREATE SEQUENCE public.dag_pickle_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.dag_run_id_seq;

CREATE SEQUENCE public.dag_run_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.dataset_event_id_seq;

CREATE SEQUENCE public.dataset_event_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.dataset_id_seq;

CREATE SEQUENCE public.dataset_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.import_error_id_seq;

CREATE SEQUENCE public.import_error_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.job_id_seq;

CREATE SEQUENCE public.job_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.log_id_seq;

CREATE SEQUENCE public.log_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.log_template_id_seq;

CREATE SEQUENCE public.log_template_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.session_id_seq;

CREATE SEQUENCE public.session_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.slot_pool_id_seq;

CREATE SEQUENCE public.slot_pool_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.task_fail_id_seq;

CREATE SEQUENCE public.task_fail_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.task_id_sequence;

CREATE SEQUENCE public.task_id_sequence
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 9223372036854775807
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.task_reschedule_id_seq;

CREATE SEQUENCE public.task_reschedule_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.taskset_id_sequence;

CREATE SEQUENCE public.taskset_id_sequence
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 9223372036854775807
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.trigger_id_seq;

CREATE SEQUENCE public.trigger_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.variable_id_seq;

CREATE SEQUENCE public.variable_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;-- public.ab_permission definition

-- Drop table

-- DROP TABLE public.ab_permission;

CREATE TABLE public.ab_permission (
	id serial4 NOT NULL,
	"name" varchar(100) NOT NULL,
	CONSTRAINT ab_permission_name_uq UNIQUE (name),
	CONSTRAINT ab_permission_pkey PRIMARY KEY (id)
);


-- public.ab_register_user definition

-- Drop table

-- DROP TABLE public.ab_register_user;

CREATE TABLE public.ab_register_user (
	id serial4 NOT NULL,
	first_name varchar(64) NOT NULL,
	last_name varchar(64) NOT NULL,
	username varchar(256) NOT NULL,
	"password" varchar(256) NULL,
	email varchar(256) NOT NULL,
	registration_date timestamp NULL,
	registration_hash varchar(256) NULL,
	CONSTRAINT ab_register_user_pkey PRIMARY KEY (id),
	CONSTRAINT ab_register_user_username_uq UNIQUE (username)
);
CREATE UNIQUE INDEX idx_ab_register_user_username ON public.ab_register_user USING btree (lower((username)::text));


-- public.ab_role definition

-- Drop table

-- DROP TABLE public.ab_role;

CREATE TABLE public.ab_role (
	id serial4 NOT NULL,
	"name" varchar(64) NOT NULL,
	CONSTRAINT ab_role_name_uq UNIQUE (name),
	CONSTRAINT ab_role_pkey PRIMARY KEY (id)
);


-- public.ab_view_menu definition

-- Drop table

-- DROP TABLE public.ab_view_menu;

CREATE TABLE public.ab_view_menu (
	id serial4 NOT NULL,
	"name" varchar(250) NOT NULL,
	CONSTRAINT ab_view_menu_name_uq UNIQUE (name),
	CONSTRAINT ab_view_menu_pkey PRIMARY KEY (id)
);


-- public.alembic_version definition

-- Drop table

-- DROP TABLE public.alembic_version;

CREATE TABLE public.alembic_version (
	version_num varchar(32) NOT NULL,
	CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);


-- public.callback_request definition

-- Drop table

-- DROP TABLE public.callback_request;

CREATE TABLE public.callback_request (
	id serial4 NOT NULL,
	created_at timestamptz NOT NULL,
	priority_weight int4 NOT NULL,
	callback_data json NOT NULL,
	callback_type varchar(20) NOT NULL,
	processor_subdir varchar(2000) NULL,
	CONSTRAINT callback_request_pkey PRIMARY KEY (id)
);


-- public.celery_taskmeta definition

-- Drop table

-- DROP TABLE public.celery_taskmeta;

CREATE TABLE public.celery_taskmeta (
	id int4 NOT NULL,
	task_id varchar(155) NULL,
	status varchar(50) NULL,
	"result" bytea NULL,
	date_done timestamp NULL,
	traceback text NULL,
	"name" varchar(155) NULL,
	args bytea NULL,
	kwargs bytea NULL,
	worker varchar(155) NULL,
	retries int4 NULL,
	queue varchar(155) NULL,
	CONSTRAINT celery_taskmeta_pkey PRIMARY KEY (id),
	CONSTRAINT celery_taskmeta_task_id_key UNIQUE (task_id)
);


-- public.celery_tasksetmeta definition

-- Drop table

-- DROP TABLE public.celery_tasksetmeta;

CREATE TABLE public.celery_tasksetmeta (
	id int4 NOT NULL,
	taskset_id varchar(155) NULL,
	"result" bytea NULL,
	date_done timestamp NULL,
	CONSTRAINT celery_tasksetmeta_pkey PRIMARY KEY (id),
	CONSTRAINT celery_tasksetmeta_taskset_id_key UNIQUE (taskset_id)
);


-- public."connection" definition

-- Drop table

-- DROP TABLE public."connection";

CREATE TABLE public."connection" (
	id serial4 NOT NULL,
	conn_id varchar(250) NOT NULL,
	conn_type varchar(500) NOT NULL,
	description text NULL,
	host varchar(500) NULL,
	"schema" varchar(500) NULL,
	login varchar(500) NULL,
	"password" varchar(5000) NULL,
	port int4 NULL,
	is_encrypted bool NULL,
	is_extra_encrypted bool NULL,
	extra text NULL,
	CONSTRAINT connection_conn_id_uq UNIQUE (conn_id),
	CONSTRAINT connection_pkey PRIMARY KEY (id)
);


-- public.dag definition

-- Drop table

-- DROP TABLE public.dag;

CREATE TABLE public.dag (
	dag_id varchar(250) NOT NULL,
	root_dag_id varchar(250) NULL,
	is_paused bool NULL,
	is_subdag bool NULL,
	is_active bool NULL,
	last_parsed_time timestamptz NULL,
	last_pickled timestamptz NULL,
	last_expired timestamptz NULL,
	scheduler_lock bool NULL,
	pickle_id int4 NULL,
	fileloc varchar(2000) NULL,
	processor_subdir varchar(2000) NULL,
	owners varchar(2000) NULL,
	description text NULL,
	default_view varchar(25) NULL,
	schedule_interval text NULL,
	timetable_description varchar(1000) NULL,
	max_active_tasks int4 NOT NULL,
	max_active_runs int4 NULL,
	has_task_concurrency_limits bool NOT NULL,
	has_import_errors bool NULL DEFAULT false,
	next_dagrun timestamptz NULL,
	next_dagrun_data_interval_start timestamptz NULL,
	next_dagrun_data_interval_end timestamptz NULL,
	next_dagrun_create_after timestamptz NULL,
	CONSTRAINT dag_pkey PRIMARY KEY (dag_id)
);
CREATE INDEX idx_next_dagrun_create_after ON public.dag USING btree (next_dagrun_create_after);
CREATE INDEX idx_root_dag_id ON public.dag USING btree (root_dag_id);


-- public.dag_code definition

-- Drop table

-- DROP TABLE public.dag_code;

CREATE TABLE public.dag_code (
	fileloc_hash int8 NOT NULL,
	fileloc varchar(2000) NOT NULL,
	last_updated timestamptz NOT NULL,
	source_code text NOT NULL,
	CONSTRAINT dag_code_pkey PRIMARY KEY (fileloc_hash)
);


-- public.dag_pickle definition

-- Drop table

-- DROP TABLE public.dag_pickle;

CREATE TABLE public.dag_pickle (
	id serial4 NOT NULL,
	pickle bytea NULL,
	created_dttm timestamptz NULL,
	pickle_hash int8 NULL,
	CONSTRAINT dag_pickle_pkey PRIMARY KEY (id)
);


-- public.dataset definition

-- Drop table

-- DROP TABLE public.dataset;

CREATE TABLE public.dataset (
	id serial4 NOT NULL,
	uri varchar(3000) NOT NULL,
	extra json NOT NULL,
	created_at timestamptz NOT NULL,
	updated_at timestamptz NOT NULL,
	is_orphaned bool NOT NULL DEFAULT false,
	CONSTRAINT dataset_pkey PRIMARY KEY (id)
);
CREATE UNIQUE INDEX idx_uri_unique ON public.dataset USING btree (uri);


-- public.dataset_event definition

-- Drop table

-- DROP TABLE public.dataset_event;

CREATE TABLE public.dataset_event (
	id serial4 NOT NULL,
	dataset_id int4 NOT NULL,
	extra json NOT NULL,
	source_task_id varchar(250) NULL,
	source_dag_id varchar(250) NULL,
	source_run_id varchar(250) NULL,
	source_map_index int4 NULL DEFAULT '-1'::integer,
	"timestamp" timestamptz NOT NULL,
	CONSTRAINT dataset_event_pkey PRIMARY KEY (id)
);
CREATE INDEX idx_dataset_id_timestamp ON public.dataset_event USING btree (dataset_id, "timestamp");


-- public.import_error definition

-- Drop table

-- DROP TABLE public.import_error;

CREATE TABLE public.import_error (
	id serial4 NOT NULL,
	"timestamp" timestamptz NULL,
	filename varchar(1024) NULL,
	stacktrace text NULL,
	CONSTRAINT import_error_pkey PRIMARY KEY (id)
);


-- public.job definition

-- Drop table

-- DROP TABLE public.job;

CREATE TABLE public.job (
	id serial4 NOT NULL,
	dag_id varchar(250) NULL,
	state varchar(20) NULL,
	job_type varchar(30) NULL,
	start_date timestamptz NULL,
	end_date timestamptz NULL,
	latest_heartbeat timestamptz NULL,
	executor_class varchar(500) NULL,
	hostname varchar(500) NULL,
	unixname varchar(1000) NULL,
	CONSTRAINT job_pkey PRIMARY KEY (id)
);
CREATE INDEX idx_job_dag_id ON public.job USING btree (dag_id);
CREATE INDEX idx_job_state_heartbeat ON public.job USING btree (state, latest_heartbeat);
CREATE INDEX job_type_heart ON public.job USING btree (job_type, latest_heartbeat);


-- public.log definition

-- Drop table

-- DROP TABLE public.log;

CREATE TABLE public.log (
	id serial4 NOT NULL,
	dttm timestamptz NULL,
	dag_id varchar(250) NULL,
	task_id varchar(250) NULL,
	map_index int4 NULL,
	"event" varchar(30) NULL,
	execution_date timestamptz NULL,
	"owner" varchar(500) NULL,
	extra text NULL,
	CONSTRAINT log_pkey PRIMARY KEY (id)
);
CREATE INDEX idx_log_dag ON public.log USING btree (dag_id);
CREATE INDEX idx_log_event ON public.log USING btree (event);


-- public.log_template definition

-- Drop table

-- DROP TABLE public.log_template;

CREATE TABLE public.log_template (
	id serial4 NOT NULL,
	filename text NOT NULL,
	elasticsearch_id text NOT NULL,
	created_at timestamptz NOT NULL,
	CONSTRAINT log_template_pkey PRIMARY KEY (id)
);


-- public.serialized_dag definition

-- Drop table

-- DROP TABLE public.serialized_dag;

CREATE TABLE public.serialized_dag (
	dag_id varchar(250) NOT NULL,
	fileloc varchar(2000) NOT NULL,
	fileloc_hash int8 NOT NULL,
	"data" json NULL,
	data_compressed bytea NULL,
	last_updated timestamptz NOT NULL,
	dag_hash varchar(32) NOT NULL,
	processor_subdir varchar(2000) NULL,
	CONSTRAINT serialized_dag_pkey PRIMARY KEY (dag_id)
);
CREATE INDEX idx_fileloc_hash ON public.serialized_dag USING btree (fileloc_hash);


-- public."session" definition

-- Drop table

-- DROP TABLE public."session";

CREATE TABLE public."session" (
	id serial4 NOT NULL,
	session_id varchar(255) NULL,
	"data" bytea NULL,
	expiry timestamp NULL,
	CONSTRAINT session_pkey PRIMARY KEY (id),
	CONSTRAINT session_session_id_key UNIQUE (session_id)
);


-- public.sla_miss definition

-- Drop table

-- DROP TABLE public.sla_miss;

CREATE TABLE public.sla_miss (
	task_id varchar(250) NOT NULL,
	dag_id varchar(250) NOT NULL,
	execution_date timestamptz NOT NULL,
	email_sent bool NULL,
	"timestamp" timestamptz NULL,
	description text NULL,
	notification_sent bool NULL,
	CONSTRAINT sla_miss_pkey PRIMARY KEY (task_id, dag_id, execution_date)
);
CREATE INDEX sm_dag ON public.sla_miss USING btree (dag_id);


-- public.slot_pool definition

-- Drop table

-- DROP TABLE public.slot_pool;

CREATE TABLE public.slot_pool (
	id serial4 NOT NULL,
	pool varchar(256) NULL,
	slots int4 NULL,
	description text NULL,
	CONSTRAINT slot_pool_pkey PRIMARY KEY (id),
	CONSTRAINT slot_pool_pool_uq UNIQUE (pool)
);


-- public."trigger" definition

-- Drop table

-- DROP TABLE public."trigger";

CREATE TABLE public."trigger" (
	id serial4 NOT NULL,
	classpath varchar(1000) NOT NULL,
	kwargs json NOT NULL,
	created_date timestamptz NOT NULL,
	triggerer_id int4 NULL,
	CONSTRAINT trigger_pkey PRIMARY KEY (id)
);


-- public.variable definition

-- Drop table

-- DROP TABLE public.variable;

CREATE TABLE public.variable (
	id serial4 NOT NULL,
	"key" varchar(250) NULL,
	val text NULL,
	description text NULL,
	is_encrypted bool NULL,
	CONSTRAINT variable_key_uq UNIQUE (key),
	CONSTRAINT variable_pkey PRIMARY KEY (id)
);


-- public.ab_permission_view definition

-- Drop table

-- DROP TABLE public.ab_permission_view;

CREATE TABLE public.ab_permission_view (
	id serial4 NOT NULL,
	permission_id int4 NULL,
	view_menu_id int4 NULL,
	CONSTRAINT ab_permission_view_permission_id_view_menu_id_uq UNIQUE (permission_id, view_menu_id),
	CONSTRAINT ab_permission_view_pkey PRIMARY KEY (id),
	CONSTRAINT ab_permission_view_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES public.ab_permission(id),
	CONSTRAINT ab_permission_view_view_menu_id_fkey FOREIGN KEY (view_menu_id) REFERENCES public.ab_view_menu(id)
);


-- public.ab_permission_view_role definition

-- Drop table

-- DROP TABLE public.ab_permission_view_role;

CREATE TABLE public.ab_permission_view_role (
	id serial4 NOT NULL,
	permission_view_id int4 NULL,
	role_id int4 NULL,
	CONSTRAINT ab_permission_view_role_permission_view_id_role_id_uq UNIQUE (permission_view_id, role_id),
	CONSTRAINT ab_permission_view_role_pkey PRIMARY KEY (id),
	CONSTRAINT ab_permission_view_role_permission_view_id_fkey FOREIGN KEY (permission_view_id) REFERENCES public.ab_permission_view(id),
	CONSTRAINT ab_permission_view_role_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.ab_role(id)
);


-- public.ab_user definition

-- Drop table

-- DROP TABLE public.ab_user;

CREATE TABLE public.ab_user (
	id serial4 NOT NULL,
	first_name varchar(64) NOT NULL,
	last_name varchar(64) NOT NULL,
	username varchar(256) NOT NULL,
	"password" varchar(256) NULL,
	active bool NULL,
	email varchar(256) NOT NULL,
	last_login timestamp NULL,
	login_count int4 NULL,
	fail_login_count int4 NULL,
	created_on timestamp NULL,
	changed_on timestamp NULL,
	created_by_fk int4 NULL,
	changed_by_fk int4 NULL,
	CONSTRAINT ab_user_email_uq UNIQUE (email),
	CONSTRAINT ab_user_pkey PRIMARY KEY (id),
	CONSTRAINT ab_user_username_uq UNIQUE (username),
	CONSTRAINT ab_user_changed_by_fk_fkey FOREIGN KEY (changed_by_fk) REFERENCES public.ab_user(id),
	CONSTRAINT ab_user_created_by_fk_fkey FOREIGN KEY (created_by_fk) REFERENCES public.ab_user(id)
);
CREATE UNIQUE INDEX idx_ab_user_username ON public.ab_user USING btree (lower((username)::text));


-- public.ab_user_role definition

-- Drop table

-- DROP TABLE public.ab_user_role;

CREATE TABLE public.ab_user_role (
	id serial4 NOT NULL,
	user_id int4 NULL,
	role_id int4 NULL,
	CONSTRAINT ab_user_role_pkey PRIMARY KEY (id),
	CONSTRAINT ab_user_role_user_id_role_id_uq UNIQUE (user_id, role_id),
	CONSTRAINT ab_user_role_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.ab_role(id),
	CONSTRAINT ab_user_role_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.ab_user(id)
);


-- public.dag_owner_attributes definition

-- Drop table

-- DROP TABLE public.dag_owner_attributes;

CREATE TABLE public.dag_owner_attributes (
	dag_id varchar(250) NOT NULL,
	"owner" varchar(500) NOT NULL,
	link varchar(500) NOT NULL,
	CONSTRAINT dag_owner_attributes_pkey PRIMARY KEY (dag_id, owner),
	CONSTRAINT "dag.dag_id" FOREIGN KEY (dag_id) REFERENCES public.dag(dag_id) ON DELETE CASCADE
);


-- public.dag_run definition

-- Drop table

-- DROP TABLE public.dag_run;

CREATE TABLE public.dag_run (
	id serial4 NOT NULL,
	dag_id varchar(250) NOT NULL,
	queued_at timestamptz NULL,
	execution_date timestamptz NOT NULL,
	start_date timestamptz NULL,
	end_date timestamptz NULL,
	state varchar(50) NULL,
	run_id varchar(250) NOT NULL,
	creating_job_id int4 NULL,
	external_trigger bool NULL,
	run_type varchar(50) NOT NULL,
	conf bytea NULL,
	data_interval_start timestamptz NULL,
	data_interval_end timestamptz NULL,
	last_scheduling_decision timestamptz NULL,
	dag_hash varchar(32) NULL,
	log_template_id int4 NULL,
	updated_at timestamptz NULL,
	CONSTRAINT dag_run_dag_id_execution_date_key UNIQUE (dag_id, execution_date),
	CONSTRAINT dag_run_dag_id_run_id_key UNIQUE (dag_id, run_id),
	CONSTRAINT dag_run_pkey PRIMARY KEY (id),
	CONSTRAINT task_instance_log_template_id_fkey FOREIGN KEY (log_template_id) REFERENCES public.log_template(id)
);
CREATE INDEX dag_id_state ON public.dag_run USING btree (dag_id, state);
CREATE INDEX idx_dag_run_dag_id ON public.dag_run USING btree (dag_id);
CREATE INDEX idx_dag_run_queued_dags ON public.dag_run USING btree (state, dag_id) WHERE ((state)::text = 'queued'::text);
CREATE INDEX idx_dag_run_running_dags ON public.dag_run USING btree (state, dag_id) WHERE ((state)::text = 'running'::text);
CREATE INDEX idx_last_scheduling_decision ON public.dag_run USING btree (last_scheduling_decision);


-- public.dag_run_note definition

-- Drop table

-- DROP TABLE public.dag_run_note;

CREATE TABLE public.dag_run_note (
	user_id int4 NULL,
	dag_run_id int4 NOT NULL,
	"content" varchar(1000) NULL,
	created_at timestamptz NOT NULL,
	updated_at timestamptz NOT NULL,
	CONSTRAINT dag_run_note_pkey PRIMARY KEY (dag_run_id),
	CONSTRAINT dag_run_note_dr_fkey FOREIGN KEY (dag_run_id) REFERENCES public.dag_run(id) ON DELETE CASCADE,
	CONSTRAINT dag_run_note_user_fkey FOREIGN KEY (user_id) REFERENCES public.ab_user(id)
);


-- public.dag_schedule_dataset_reference definition

-- Drop table

-- DROP TABLE public.dag_schedule_dataset_reference;

CREATE TABLE public.dag_schedule_dataset_reference (
	dataset_id int4 NOT NULL,
	dag_id varchar(250) NOT NULL,
	created_at timestamptz NOT NULL,
	updated_at timestamptz NOT NULL,
	CONSTRAINT dsdr_pkey PRIMARY KEY (dataset_id, dag_id),
	CONSTRAINT dsdr_dag_id_fkey FOREIGN KEY (dag_id) REFERENCES public.dag(dag_id) ON DELETE CASCADE,
	CONSTRAINT dsdr_dataset_fkey FOREIGN KEY (dataset_id) REFERENCES public.dataset(id) ON DELETE CASCADE
);


-- public.dag_tag definition

-- Drop table

-- DROP TABLE public.dag_tag;

CREATE TABLE public.dag_tag (
	"name" varchar(100) NOT NULL,
	dag_id varchar(250) NOT NULL,
	CONSTRAINT dag_tag_pkey PRIMARY KEY (name, dag_id),
	CONSTRAINT dag_tag_dag_id_fkey FOREIGN KEY (dag_id) REFERENCES public.dag(dag_id) ON DELETE CASCADE
);


-- public.dag_warning definition

-- Drop table

-- DROP TABLE public.dag_warning;

CREATE TABLE public.dag_warning (
	dag_id varchar(250) NOT NULL,
	warning_type varchar(50) NOT NULL,
	message text NOT NULL,
	"timestamp" timestamptz NOT NULL,
	CONSTRAINT dag_warning_pkey PRIMARY KEY (dag_id, warning_type),
	CONSTRAINT dcw_dag_id_fkey FOREIGN KEY (dag_id) REFERENCES public.dag(dag_id) ON DELETE CASCADE
);


-- public.dagrun_dataset_event definition

-- Drop table

-- DROP TABLE public.dagrun_dataset_event;

CREATE TABLE public.dagrun_dataset_event (
	dag_run_id int4 NOT NULL,
	event_id int4 NOT NULL,
	CONSTRAINT dagrun_dataset_event_pkey PRIMARY KEY (dag_run_id, event_id),
	CONSTRAINT dagrun_dataset_event_dag_run_id_fkey FOREIGN KEY (dag_run_id) REFERENCES public.dag_run(id) ON DELETE CASCADE,
	CONSTRAINT dagrun_dataset_event_event_id_fkey FOREIGN KEY (event_id) REFERENCES public.dataset_event(id) ON DELETE CASCADE
);
CREATE INDEX idx_dagrun_dataset_events_dag_run_id ON public.dagrun_dataset_event USING btree (dag_run_id);
CREATE INDEX idx_dagrun_dataset_events_event_id ON public.dagrun_dataset_event USING btree (event_id);


-- public.dataset_dag_run_queue definition

-- Drop table

-- DROP TABLE public.dataset_dag_run_queue;

CREATE TABLE public.dataset_dag_run_queue (
	dataset_id int4 NOT NULL,
	target_dag_id varchar(250) NOT NULL,
	created_at timestamptz NOT NULL,
	CONSTRAINT datasetdagrunqueue_pkey PRIMARY KEY (dataset_id, target_dag_id),
	CONSTRAINT ddrq_dag_fkey FOREIGN KEY (target_dag_id) REFERENCES public.dag(dag_id) ON DELETE CASCADE,
	CONSTRAINT ddrq_dataset_fkey FOREIGN KEY (dataset_id) REFERENCES public.dataset(id) ON DELETE CASCADE
);


-- public.task_instance definition

-- Drop table

-- DROP TABLE public.task_instance;

CREATE TABLE public.task_instance (
	task_id varchar(250) NOT NULL,
	dag_id varchar(250) NOT NULL,
	run_id varchar(250) NOT NULL,
	map_index int4 NOT NULL DEFAULT '-1'::integer,
	start_date timestamptz NULL,
	end_date timestamptz NULL,
	duration float8 NULL,
	state varchar(20) NULL,
	try_number int4 NULL,
	max_tries int4 NULL DEFAULT '-1'::integer,
	hostname varchar(1000) NULL,
	unixname varchar(1000) NULL,
	job_id int4 NULL,
	pool varchar(256) NOT NULL,
	pool_slots int4 NOT NULL,
	queue varchar(256) NULL,
	priority_weight int4 NULL,
	"operator" varchar(1000) NULL,
	queued_dttm timestamptz NULL,
	queued_by_job_id int4 NULL,
	pid int4 NULL,
	executor_config bytea NULL,
	updated_at timestamptz NULL,
	external_executor_id varchar(250) NULL,
	trigger_id int4 NULL,
	trigger_timeout timestamp NULL,
	next_method varchar(1000) NULL,
	next_kwargs json NULL,
	CONSTRAINT task_instance_pkey PRIMARY KEY (dag_id, task_id, run_id, map_index),
	CONSTRAINT task_instance_dag_run_fkey FOREIGN KEY (dag_id,run_id) REFERENCES public.dag_run(dag_id,run_id) ON DELETE CASCADE,
	CONSTRAINT task_instance_trigger_id_fkey FOREIGN KEY (trigger_id) REFERENCES public."trigger"(id) ON DELETE CASCADE
);
CREATE INDEX ti_dag_run ON public.task_instance USING btree (dag_id, run_id);
CREATE INDEX ti_dag_state ON public.task_instance USING btree (dag_id, state);
CREATE INDEX ti_job_id ON public.task_instance USING btree (job_id);
CREATE INDEX ti_pool ON public.task_instance USING btree (pool, state, priority_weight);
CREATE INDEX ti_state ON public.task_instance USING btree (state);
CREATE INDEX ti_state_lkp ON public.task_instance USING btree (dag_id, task_id, run_id, state);
CREATE INDEX ti_trigger_id ON public.task_instance USING btree (trigger_id);


-- public.task_instance_note definition

-- Drop table

-- DROP TABLE public.task_instance_note;

CREATE TABLE public.task_instance_note (
	user_id int4 NULL,
	task_id varchar(250) NOT NULL,
	dag_id varchar(250) NOT NULL,
	run_id varchar(250) NOT NULL,
	map_index int4 NOT NULL,
	"content" varchar(1000) NULL,
	created_at timestamptz NOT NULL,
	updated_at timestamptz NOT NULL,
	CONSTRAINT task_instance_note_pkey PRIMARY KEY (task_id, dag_id, run_id, map_index),
	CONSTRAINT task_instance_note_ti_fkey FOREIGN KEY (dag_id,task_id,run_id,map_index) REFERENCES public.task_instance(dag_id,task_id,run_id,map_index) ON DELETE CASCADE,
	CONSTRAINT task_instance_note_user_fkey FOREIGN KEY (user_id) REFERENCES public.ab_user(id)
);


-- public.task_map definition

-- Drop table

-- DROP TABLE public.task_map;

CREATE TABLE public.task_map (
	dag_id varchar(250) NOT NULL,
	task_id varchar(250) NOT NULL,
	run_id varchar(250) NOT NULL,
	map_index int4 NOT NULL,
	length int4 NOT NULL,
	keys json NULL,
	CONSTRAINT ck_task_map_task_map_length_not_negative CHECK ((length >= 0)),
	CONSTRAINT task_map_pkey PRIMARY KEY (dag_id, task_id, run_id, map_index),
	CONSTRAINT task_map_task_instance_fkey FOREIGN KEY (dag_id,task_id,run_id,map_index) REFERENCES public.task_instance(dag_id,task_id,run_id,map_index) ON DELETE CASCADE
);


-- public.task_outlet_dataset_reference definition

-- Drop table

-- DROP TABLE public.task_outlet_dataset_reference;

CREATE TABLE public.task_outlet_dataset_reference (
	dataset_id int4 NOT NULL,
	dag_id varchar(250) NOT NULL,
	task_id varchar(250) NOT NULL,
	created_at timestamptz NOT NULL,
	updated_at timestamptz NOT NULL,
	CONSTRAINT todr_pkey PRIMARY KEY (dataset_id, dag_id, task_id),
	CONSTRAINT todr_dag_id_fkey FOREIGN KEY (dag_id) REFERENCES public.dag(dag_id) ON DELETE CASCADE,
	CONSTRAINT todr_dataset_fkey FOREIGN KEY (dataset_id) REFERENCES public.dataset(id) ON DELETE CASCADE
);


-- public.task_reschedule definition

-- Drop table

-- DROP TABLE public.task_reschedule;

CREATE TABLE public.task_reschedule (
	id serial4 NOT NULL,
	task_id varchar(250) NOT NULL,
	dag_id varchar(250) NOT NULL,
	run_id varchar(250) NOT NULL,
	map_index int4 NOT NULL DEFAULT '-1'::integer,
	try_number int4 NOT NULL,
	start_date timestamptz NOT NULL,
	end_date timestamptz NOT NULL,
	duration int4 NOT NULL,
	reschedule_date timestamptz NOT NULL,
	CONSTRAINT task_reschedule_pkey PRIMARY KEY (id),
	CONSTRAINT task_reschedule_dr_fkey FOREIGN KEY (dag_id,run_id) REFERENCES public.dag_run(dag_id,run_id) ON DELETE CASCADE,
	CONSTRAINT task_reschedule_ti_fkey FOREIGN KEY (dag_id,task_id,run_id,map_index) REFERENCES public.task_instance(dag_id,task_id,run_id,map_index) ON DELETE CASCADE
);
CREATE INDEX idx_task_reschedule_dag_run ON public.task_reschedule USING btree (dag_id, run_id);
CREATE INDEX idx_task_reschedule_dag_task_run ON public.task_reschedule USING btree (dag_id, task_id, run_id, map_index);


-- public.xcom definition

-- Drop table

-- DROP TABLE public.xcom;

CREATE TABLE public.xcom (
	dag_run_id int4 NOT NULL,
	task_id varchar(250) NOT NULL,
	map_index int4 NOT NULL DEFAULT '-1'::integer,
	"key" varchar(512) NOT NULL,
	dag_id varchar(250) NOT NULL,
	run_id varchar(250) NOT NULL,
	value bytea NULL,
	"timestamp" timestamptz NOT NULL,
	CONSTRAINT xcom_pkey PRIMARY KEY (dag_run_id, task_id, map_index, key),
	CONSTRAINT xcom_task_instance_fkey FOREIGN KEY (dag_id,task_id,run_id,map_index) REFERENCES public.task_instance(dag_id,task_id,run_id,map_index) ON DELETE CASCADE
);
CREATE INDEX idx_xcom_key ON public.xcom USING btree (key);
CREATE INDEX idx_xcom_task_instance ON public.xcom USING btree (dag_id, task_id, run_id, map_index);


-- public.rendered_task_instance_fields definition

-- Drop table

-- DROP TABLE public.rendered_task_instance_fields;

CREATE TABLE public.rendered_task_instance_fields (
	dag_id varchar(250) NOT NULL,
	task_id varchar(250) NOT NULL,
	run_id varchar(250) NOT NULL,
	map_index int4 NOT NULL DEFAULT '-1'::integer,
	rendered_fields json NOT NULL,
	k8s_pod_yaml json NULL,
	CONSTRAINT rendered_task_instance_fields_pkey PRIMARY KEY (dag_id, task_id, run_id, map_index),
	CONSTRAINT rtif_ti_fkey FOREIGN KEY (dag_id,task_id,run_id,map_index) REFERENCES public.task_instance(dag_id,task_id,run_id,map_index) ON DELETE CASCADE
);


-- public.task_fail definition

-- Drop table

-- DROP TABLE public.task_fail;

CREATE TABLE public.task_fail (
	id serial4 NOT NULL,
	task_id varchar(250) NOT NULL,
	dag_id varchar(250) NOT NULL,
	run_id varchar(250) NOT NULL,
	map_index int4 NOT NULL DEFAULT '-1'::integer,
	start_date timestamptz NULL,
	end_date timestamptz NULL,
	duration int4 NULL,
	CONSTRAINT task_fail_pkey PRIMARY KEY (id),
	CONSTRAINT task_fail_ti_fkey FOREIGN KEY (dag_id,task_id,run_id,map_index) REFERENCES public.task_instance(dag_id,task_id,run_id,map_index) ON DELETE CASCADE
);
CREATE INDEX idx_task_fail_task_instance ON public.task_fail USING btree (dag_id, task_id, run_id, map_index);
