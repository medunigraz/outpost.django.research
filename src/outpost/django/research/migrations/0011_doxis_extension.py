# Generated by Django 2.2.26 on 2022-04-19 07:01

from django.db import migrations
from django.conf import settings


class Migration(migrations.Migration):

    ops = [
        (
            """
            ALTER FOREIGN TABLE "research"."forschung_programm" ADD COLUMN GELDGEBER_ID numeric;
            """,
            """
            ALTER FOREIGN TABLE "research"."forschung_programm" DROP COLUMN GELDGEBER_ID;
            """,
        ),
        (
            """
            ALTER FOREIGN TABLE "research"."land"
                ADD COLUMN LAENDERGRUPPE_ID numeric,
                ADD COLUMN ISO_ALPHA2 varchar,
                ADD COLUMN ISO_ALPHA3 varchar;
                ;
            """,
            """
            ALTER FOREIGN TABLE "research"."land"
                DROP COLUMN LAENDERGRUPPE_ID,
                DROP COLUMN ISO_ALPHA2,
                DROP COLUMN ISO_ALPHA3;
            """,
        ),
        (
            """
            ALTER FOREIGN TABLE "research"."geldgeber"
                ADD COLUMN TELEFON varchar,
                ADD COLUMN EMAIL varchar,
                ADD COLUMN FO_FOE_JA_NEIN varchar,
                ADD COLUMN PEER_REVIEW_ASSOZPROF varchar,
                ADD COLUMN PEER_REVIEW_ALLG varchar,
                ADD COLUMN WIBI_TYP_ID numeric,
                ADD COLUMN STATISTIK_AUT_TYP_ID numeric,
                ADD COLUMN LANDALPHA2 varchar,
                ADD COLUMN LANDALPHA3 varchar;
            """,
            """
            ALTER FOREIGN TABLE "research"."geldgeber"
                DROP COLUMN TELEFON,
                DROP COLUMN EMAIL,
                DROP COLUMN FO_FOE_JA_NEIN,
                DROP COLUMN PEER_REVIEW_ASSOZPROF,
                DROP COLUMN PEER_REVIEW_ALLG,
                DROP COLUMN WIBI_TYP_ID,
                DROP COLUMN STATISTIK_AUT_TYP_ID,
                DROP COLUMN LANDALPHA2,
                DROP COLUMN LANDALPHA3;
            """,
        ),
        (
            """
            CREATE FOREIGN TABLE "research"."partner" (
                PARTNER_ID numeric,
                PARTNER_LANDESSPRACHE varchar,
                PARTNER_EN varchar,
                KURZBEZEICHNUNG varchar,
                STRASSE varchar,
                POSTLEITZAHL varchar,
                ORT varchar,
                LAND_ID numeric,
                LAND_DE varchar,
                LANDALPHA2 varchar,
                LANDALPHA3 varchar,
                URL varchar,
                TELEFON varchar,
                FAX varchar,
                WIBI_TYP_ID numeric,
                EMAIL varchar,
                ANMERKUNGEN varchar
            )
            SERVER sqlalchemy OPTIONS (
                tablename 'PARTNER',
                db_url '{}'
            );
            """.format(
                settings.MULTICORN.get("research")
            ),
            """
            DROP FOREIGN TABLE IF EXISTS "research"."partner";
            """,
        ),
        (
            """
            CREATE FOREIGN TABLE "research"."partner_typ_wb" (
                WIBI_TYP_ID numeric,
                BEZEICHNUNG_DE varchar,
                BEZEICHNUNG_EN varchar
            )
            SERVER sqlalchemy OPTIONS (
                tablename 'PARTNER_TYP_WB_L',
                db_url '{}'
            );
            """.format(
                settings.MULTICORN.get("research")
            ),
            """
            DROP FOREIGN TABLE IF EXISTS "research"."partner_typ_wb";
            """,
        ),
        (
            """
            CREATE FOREIGN TABLE "research"."geldgeber_typ_stataut" (
                STATISTIK_AUT_TYP_ID numeric,
                BEZEICHNUNG_DE varchar,
                BEZEICHNUNG_EN varchar
            )
            SERVER sqlalchemy OPTIONS (
                tablename 'GELDGEBER_TYP_STATAUT_L',
                db_url '{}'
            );
            """.format(
                settings.MULTICORN.get("research")
            ),
            """
            DROP FOREIGN TABLE IF EXISTS "research"."geldgeber_typ_stataut";
            """,
        ),
        (
            """
            CREATE FOREIGN TABLE "research"."geldgeber_typ_wissbil" (
                WIBI_TYP_ID numeric,
                BEZEICHNUNG_DE varchar,
                BEZEICHNUNG_EN varchar
            )
            SERVER sqlalchemy OPTIONS (
                tablename 'GELDGEBER_TYP_WISSBIL_L',
                db_url '{}'
            );
            """.format(
                settings.MULTICORN.get("research")
            ),
            """
            DROP FOREIGN TABLE IF EXISTS "research"."geldgeber_typ_wissbil";
            """,
        ),
        (
            """
            DROP MATERIALIZED VIEW IF EXISTS "public"."research_program";
            """,
            """
            CREATE MATERIALIZED VIEW "public"."research_program" AS SELECT
                FORSCHUNG_PROGRAMM_ID::integer AS id,
                FORSCHUNG_PROGRAMM_NAME AS name,
                COALESCE((LOWER(AKTIV_JN) = 'j'), FALSE)::boolean AS active
            FROM
                "research"."forschung_programm"
            """,
        ),
        (
            """
            CREATE MATERIALIZED VIEW "public"."research_program" AS SELECT
                FORSCHUNG_PROGRAMM_ID::integer AS id,
                FORSCHUNG_PROGRAMM_NAME AS name,
                COALESCE((LOWER(AKTIV_JN) = 'j'), FALSE)::boolean AS active,
                GELDGEBER_ID::integer AS funder_id
            FROM
                "research"."forschung_programm"
            """,
            """
            DROP MATERIALIZED VIEW IF EXISTS "public"."research_program";
            """,
        ),
        (
            """
            DROP MATERIALIZED VIEW IF EXISTS "public"."research_country";
            """,
            """
            CREATE MATERIALIZED VIEW "public"."research_country" AS SELECT
                LAND_ID::integer AS id,
                LAND_DE AS name
            FROM
                "research"."land"
            """,
        ),
        (
            """
            CREATE MATERIALIZED VIEW "public"."research_country" AS SELECT
                LAND_ID::integer AS id,
                hstore(
                    ARRAY['de', 'en'],
                    ARRAY[LAND_DE, LAND_EN]
                ) AS name,
                hstore(
                    ARRAY['alpha2', 'alpha3'],
                    ARRAY[ISO_ALPHA2, ISO_ALPHA3]
                ) AS iso
            FROM
                "research"."land"
            """,
            """
            DROP MATERIALIZED VIEW IF EXISTS "public"."research_country";
            """,
        ),
        (
            """
            DROP INDEX IF EXISTS research_funder_id_idx;
            """,
            """
            CREATE UNIQUE INDEX research_funder_id_idx ON "public"."research_funder" ("id");
            """,
        ),
        (
            """
            DROP MATERIALIZED VIEW IF EXISTS "public"."research_funder";
            """,
            """
            CREATE MATERIALIZED VIEW "public"."research_funder" AS SELECT
                GELDGEBER_ID::integer AS id,
                GELDGEBER_DE AS name,
                STRASSE AS street,
                ORT AS city,
                POSTLEITZAHL AS zipcode,
                LAND_ID::integer AS country_id,
                URL,
                GELDGEBER_TYP_ID::integer AS category_id
            FROM
                "research"."geldgeber"
            """,
        ),
        (
            """
            CREATE MATERIALIZED VIEW "public"."research_funder" AS SELECT
                GELDGEBER_ID::integer AS id,
                GELDGEBER_DE AS name,
                STRASSE AS street,
                ORT AS city,
                POSTLEITZAHL AS zipcode,
                LAND_ID::integer AS country_id,
                URL,
                GELDGEBER_TYP_ID::integer AS category_id,
                TELEFON AS telephone,
                EMAIL,
                COALESCE((LOWER(FO_FOE_JA_NEIN) = 'ja'), FALSE)::boolean AS patron,
                COALESCE((LOWER(PEER_REVIEW_ASSOZPROF) = 'ja'), FALSE)::boolean AS patron_associate_professor,
                COALESCE((LOWER(PEER_REVIEW_ALLG) = 'ja'), FALSE)::boolean AS patron_peer_review,
                WIBI_TYP_ID::integer AS typeintellectualcapitalaccounting_id,
                STATISTIK_AUT_TYP_ID::integer AS typestatisticsaustria_id
            FROM
                "research"."geldgeber"
            """,
            """
            DROP MATERIALIZED VIEW IF EXISTS "public"."research_funder";
            """,
        ),
        (
            """
            CREATE UNIQUE INDEX research_funder_id_idx ON "public"."research_funder" ("id");
            """,
            """
            DROP INDEX IF EXISTS research_funder_id_idx;
            """,
        ),
        (
            """
            CREATE MATERIALIZED VIEW "public"."research_partner" AS SELECT
                PARTNER_ID::integer AS id,
                PARTNER_LANDESSPRACHE AS name,
                KURZBEZEICHNUNG as short,
                STRASSE AS street,
                POSTLEITZAHL AS zipcode,
                ORT AS city,
                LAND_ID as country_id,
                URL,
                TELEFON as telephone,
                FAX,
                WIBI_TYP_ID::integer AS typeintellectualcapitalaccounting_id,
                EMAIL,
                ANMERKUNGEN AS information
            FROM
                "research"."partner"
            """,
            """
            DROP MATERIALIZED VIEW IF EXISTS "public"."research_partner";
            """,
        ),
        (
            """
            CREATE MATERIALIZED VIEW "public"."research_partnertypeintellectualcapitalaccounting" AS SELECT
                WIBI_TYP_ID::integer AS id,
                hstore(
                    ARRAY['de', 'en'],
                    ARRAY[BEZEICHNUNG_DE, BEZEICHNUNG_EN]
                ) AS name
            FROM
                "research"."partner_typ_wb"
            """,
            """
            DROP MATERIALIZED VIEW IF EXISTS "public"."research_partnertypeintellectualcapitalaccounting";
            """,
        ),
        (
            """
            CREATE MATERIALIZED VIEW "public"."research_fundertypeintellectualcapitalaccounting" AS SELECT
                WIBI_TYP_ID::integer AS id,
                hstore(
                    ARRAY['de', 'en'],
                    ARRAY[BEZEICHNUNG_DE, BEZEICHNUNG_EN]
                ) AS name
            FROM
                "research"."geldgeber_typ_wissbil"
            """,
            """
            DROP MATERIALIZED VIEW IF EXISTS "public"."research_fundertypeintellectualcapitalaccounting";
            """,
        ),
        (
            """
            CREATE MATERIALIZED VIEW "public"."research_fundertypestatisticsaustria" AS SELECT
                STATISTIK_AUT_TYP_ID::integer AS id,
                hstore(
                    ARRAY['de', 'en'],
                    ARRAY[BEZEICHNUNG_DE, BEZEICHNUNG_EN]
                ) AS name
            FROM
                "research"."geldgeber_typ_stataut"
            """,
            """
            DROP MATERIALIZED VIEW IF EXISTS "public"."research_fundertypestatisticsaustria";
            """,
        ),
    ]

    operations = [
        migrations.RunSQL(
            [forward for forward, reverse in ops],
            [reverse for forward, reverse in reversed(ops)],
        )
    ]
    dependencies = [
        ("research", "0010_project_left_outer_join"),
    ]
