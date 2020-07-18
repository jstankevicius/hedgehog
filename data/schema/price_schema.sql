DROP TABLE IF EXISTS "prices";
DROP TABLE IF EXISTS "last_updated";
DROP INDEX IF EXISTS "symbol_timestamp_idx";

CREATE TABLE prices (
	"symbol" text,
	"time" real,
	"open" real,
	"high" real,
	"low" real,
	"close" real,
	"adjusted_close" real,
	"volume" integer,
	"dividend_amount" real,
	"split_coefficient" real
);

CREATE UNIQUE INDEX "symbol_timestamp_idx" ON "prices" ("symbol", "time");

CREATE TABLE last_updated (
	"symbol" text,
	"time" real
);