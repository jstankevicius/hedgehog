DROP TABLE IF EXISTS "prices";
DROP INDEX IF EXISTS "symbol_timestamp_idx";

CREATE TABLE prices (
	"symbol" text,
	"date" text,
	"time" text,
	"open" real,
	"high" real,
	"low" real,
	"close" real,
	"volume" integer
);

CREATE UNIQUE INDEX "symbol_timestamp_idx" ON "prices" ("symbol", "date", "time")