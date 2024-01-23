# Generated by Django 2.2.28 on 2024-01-22 09:23

from django.db import migrations
from django.utils.timezone import get_current_timezone


tz = get_current_timezone()


class Migration(migrations.Migration):

    ops = [
        (
            """
            DROP INDEX IF EXISTS research_publication_id_idx;
            """,
            """
            CREATE UNIQUE INDEX research_publication_id_idx ON "public"."research_publication" ("id");
            """,
        ),
        (
            """
            DROP INDEX IF EXISTS research_publication_year_idx;
            """,
            """
            CREATE INDEX research_publication_year_idx ON "public"."research_publication" ("year");
            """,
        ),
        (
            """
            DROP INDEX IF EXISTS research_publication_category_id_idx;
            """,
            """
            CREATE INDEX research_publication_category_id_idx ON "public"."research_publication" ("category_id");
            """,
        ),
        (
            """
            DROP INDEX IF EXISTS research_publication_document_id_idx;
            """,
            """
            CREATE INDEX research_publication_document_id_idx ON "public"."research_publication" ("document_id");
            """,
        ),
        (
            """
            DROP INDEX IF EXISTS research_publication_impact_idx;
            """,
            """
            CREATE INDEX research_publication_impact_idx ON "public"."research_publication" ("impact");
            """,
        ),
        (
            """
            ALTER FOREIGN TABLE "research"."publikation"
                ADD COLUMN "zeitschrift" text,
                ADD COLUMN "issn_nummer" varchar,
                ADD COLUMN "herausgeber_sammelwerk" text,
                ADD COLUMN "titel_sammelwerk" text,
                ADD COLUMN "auflage" varchar,
                ADD COLUMN "universitaet" varchar,
                ADD COLUMN "iso_alpha3" varchar,
                ADD COLUMN "fallbericht_ja_nein" varchar,
                ADD COLUMN "publikation_vortragstyp_id" integer,
                ADD COLUMN "impact_faktor" numeric,
                ADD COLUMN "impact_faktor_jahr" integer,
                ADD COLUMN "impact_faktor_norm_jahr" integer,
                ADD COLUMN "impact_faktor_norm_fach" varchar,
                ADD COLUMN "ifnorm_supermax" numeric,
                ADD COLUMN "ifnorm_supermax_jahr" integer,
                ADD COLUMN "ifnorm_supermax_fach" varchar,
                ADD COLUMN "anzahl_zitierungen" integer,
                ADD COLUMN "konferenz_name" varchar,
                ADD COLUMN "konferenz_datum" varchar,
                ADD COLUMN "konferenz_ort" varchar,
                ADD COLUMN "national_international" varchar,
                ADD COLUMN "wiss_veranstaltung_ja_nein" varchar,
                ADD COLUMN "eingeladener_vortrag_ja_nein" varchar,
                ADD COLUMN "keynotespeaker_ja_nein" varchar,
                ADD COLUMN "ausgew_praesentation_ja_nein" varchar,
                ADD COLUMN "biobank_nutzung_ja_nein" varchar,
                ADD COLUMN "tierbiologie_nutzung_ja_nein" varchar,
                ADD COLUMN "zmf_nutzung_ja_nein" varchar,
                ADD COLUMN "nennung_universitaet" varchar,
                ADD COLUMN "letztautor_ja_nein" varchar;
            """,
            """
            ALTER FOREIGN TABLE "research"."publikation"
                DROP COLUMN "zeitschrift",
                DROP COLUMN "issn_nummer",
                DROP COLUMN "herausgeber_sammelwerk",
                DROP COLUMN "titel_sammelwerk",
                DROP COLUMN "auflage",
                DROP COLUMN "universitaet",
                DROP COLUMN "iso_alpha3",
                DROP COLUMN "fallbericht_ja_nein",
                DROP COLUMN "publikation_vortragstyp_id",
                DROP COLUMN "impact_faktor",
                DROP COLUMN "impact_faktor_jahr",
                DROP COLUMN "impact_faktor_norm_jahr",
                DROP COLUMN "impact_faktor_norm_fach",
                DROP COLUMN "ifnorm_supermax",
                DROP COLUMN "ifnorm_supermax_jahr",
                DROP COLUMN "ifnorm_supermax_fach",
                DROP COLUMN "anzahl_zitierungen",
                DROP COLUMN "konferenz_name",
                DROP COLUMN "konferenz_datum",
                DROP COLUMN "konferenz_ort",
                DROP COLUMN "national_international",
                DROP COLUMN "wiss_veranstaltung_ja_nein",
                DROP COLUMN "eingeladener_vortrag_ja_nein",
                DROP COLUMN "keynotespeaker_ja_nein",
                DROP COLUMN "ausgew_praesentation_ja_nein",
                DROP COLUMN "biobank_nutzung_ja_nein",
                DROP COLUMN "tierbiologie_nutzung_ja_nein",
                DROP COLUMN "zmf_nutzung_ja_nein",
                DROP COLUMN "nennung_universitaet",
                DROP COLUMN "letztautor_ja_nein";
            """,
        ),
        (
            """
            DROP MATERIALIZED VIEW IF EXISTS "public"."research_publication";
            """,
            """
            CREATE MATERIALIZED VIEW "public"."research_publication" AS SELECT DISTINCT
                PUBLIKATION_ID::integer AS id,
                TITEL AS title,
                regexp_split_to_array(trim(both ' ' from AUTOR), ';\s*') AS authors,
                JAHR::integer AS year,
                QUELLE AS source,
                PUBLIKATION_TYP_ID::integer AS category_id,
                PUBLIKATION_DOKUMENTTYP_ID::integer AS document_id,
                SCI_ID AS sci,
                PUBMED_ID AS pubmed,
                DOI AS doi,
                PMC_ID AS pmc,
                ABSTRACT AS abstract_bytes,
                publikation.impact_faktor_norm_max::double precision AS impact,
                ERFASSUNGSDATUM AS imported
            FROM
                "research"."publikation";
            """.format(
                tz=tz.zone
            ),
        ),
        (
            """
            ALTER FOREIGN TABLE "research"."publikation"
                ALTER COLUMN "abstract" TYPE text;
            """,
            """
            ALTER FOREIGN TABLE "research"."publikation"
                ALTER COLUMN "abstract" TYPE text;
            """,
        ),
        (
            """
            CREATE MATERIALIZED VIEW "public"."research_publication" AS SELECT DISTINCT
                p.PUBLIKATION_ID::integer AS id,
                p.TITEL AS title,
                regexp_split_to_array(trim(both ' ' from p.AUTOR), ';\s*') AS authors,
                p.JAHR::integer AS year,
                p.QUELLE AS source,
                p.PUBLIKATION_TYP_ID::integer AS category_id,
                p.PUBLIKATION_DOKUMENTTYP_ID::integer AS document_type_id,
                p.SCI_ID AS sci,
                p.PUBMED_ID AS pubmed,
                p.DOI AS doi,
                p.PMC_ID AS pmc,
                p.ABSTRACT AS abstract,
                p.ERFASSUNGSDATUM AS imported,
                p.ZEITSCHRIFT AS journal,
                p.ISSN_NUMMER AS issn,
                p.HERAUSGEBER_SAMMELWERK AS collection_publisher,
                p.TITEL_SAMMELWERK AS collection_title,
                p.AUFLAGE AS edition,
                p.UNIVERSITAET AS university,
                li.iso_nummer AS country_id,
                COALESCE(LOWER(p.FALLBERICHT_JA_NEIN) = 'ja', FALSE) AS case_report,
                p.IMPACT_FAKTOR AS impactfactor,
                p.IMPACT_FAKTOR_JAHR AS impactfactor_year,
                p.IMPACT_FAKTOR_NORM_MAX AS impactfactor_norm,
                p.IMPACT_FAKTOR_NORM_JAHR AS impactfactor_norm_year,
                p.IMPACT_FAKTOR_NORM_FACH AS impactfactor_norm_category,
                p.IFNORM_SUPERMAX AS impactfactor_norm_super,
                p.IFNORM_SUPERMAX_JAHR AS impactfactor_norm_super_year,
                p.IFNORM_SUPERMAX_FACH AS impactfactor_norm_super_category,
                p.ANZAHL_ZITIERUNGEN AS citations, p.KONFERENZ_NAME AS conference_name,
                p.KONFERENZ_ORT AS conference_place,
                COALESCE(LOWER(p.NATIONAL_INTERNATIONAL) = 'international', FALSE) AS conference_international,
                COALESCE(LOWER(p.WISS_VERANSTALTUNG_JA_NEIN) = 'ja', FALSE) AS scientific_event,
                COALESCE(LOWER(p.EINGELADENER_VORTRAG_JA_NEIN) =  'ja', FALSE) AS invited_lecture,
                COALESCE(LOWER(p.KEYNOTESPEAKER_JA_NEIN) = 'ja', FALSE) AS keynote_speaker,
                COALESCE(LOWER(p.AUSGEW_PRAESENTATION_JA_NEIN) = 'ja', FALSE) AS selected_presentation,
                COALESCE(LOWER(p.BIOBANK_NUTZUNG_JA_NEIN) = 'ja', FALSE) AS biobank_use,
                COALESCE(LOWER(p.TIERBIOLOGIE_NUTZUNG_JA_NEIN) = 'ja', FALSE) AS bmf_use,
                COALESCE(LOWER(p.ZMF_NUTZUNG_JA_NEIN) = 'ja', FALSE) AS zmf_use,
                COALESCE(LOWER(p.NENNUNG_UNIVERSITAET) = 'ja', FALSE) AS local_affiliation
            FROM
                "research"."publikation" p
            LEFT JOIN
                "campusonline"."laender_iso" li
                ON LOWER(p.ISO_ALPHA3) = LOWER(li.iso_code_3)
            WITH DATA;
            """.format(
                tz=tz.zone
            ),
            """
            DROP MATERIALIZED VIEW IF EXISTS "public"."research_publication";
            """,
        ),
        (
            """
            CREATE UNIQUE INDEX research_publication_id_idx ON "public"."research_publication" ("id");
            """,
            """
            DROP INDEX IF EXISTS research_publication_id_idx;
            """,
        ),
        (
            """
            CREATE INDEX research_publication_year_idx ON "public"."research_publication" ("year");
            """,
            """
            DROP INDEX IF EXISTS research_publication_year_idx;
            """,
        ),
        (
            """
            CREATE INDEX research_publication_category_id_idx ON "public"."research_publication" ("category_id");
            """,
            """
            DROP INDEX IF EXISTS research_publication_category_id_idx;
            """,
        ),
        (
            """
            CREATE INDEX research_publication_document_type_id_idx ON "public"."research_publication" ("document_type_id");
            """,
            """
            DROP INDEX IF EXISTS research_publication_document_type_id_idx;
            """,
        ),
        (
            """
            CREATE INDEX research_publication_impactfactor_idx ON "public"."research_publication" ("impactfactor");
            """,
            """
            DROP INDEX IF EXISTS research_publication_impactfactor_idx;
            """,
        ),
        (
            """
            CREATE INDEX research_publication_impactfactor_norm_idx ON "public"."research_publication" ("impactfactor_norm");
            """,
            """
            DROP INDEX IF EXISTS research_publication_impactfactor_norm_idx;
            """,
        ),
        (
            """
            CREATE INDEX research_publication_impactfactor_norm_super_idx ON "public"."research_publication" ("impactfactor_norm_super");
            """,
            """
            DROP INDEX IF EXISTS research_publication_impactfactor_norm_super_idx;
            """,
        ),
    ]

    dependencies = [
        ("research", "0014_project_nbsp"),
    ]

    operations = [
        migrations.RunSQL(
            [forward for forward, reverse in ops],
            [reverse for forward, reverse in reversed(ops)],
        )
    ]
