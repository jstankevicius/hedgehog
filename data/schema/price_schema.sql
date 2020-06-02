DROP TABLE IF EXISTS "prices";
DROP TABLE IF EXISTS "last_updated";
DROP INDEX IF EXISTS "symbol_timestamp_idx";

CREATE TABLE prices (
	"symbol" text,
	"year" integer,
	"month" integer,
	"day" integer,
	"hour" integer,
	"minute" integer,
	"open" real,
	"high" real,
	"low" real,
	"close" real,
	"volume" integer
);

CREATE UNIQUE INDEX "symbol_timestamp_idx" ON "prices" ("symbol", "year", "month", "day", "hour", "minute");

CREATE TABLE last_updated (
	"symbol" text,
	"time" real
);