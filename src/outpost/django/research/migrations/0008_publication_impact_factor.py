# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-11-15 13:20
from __future__ import unicode_literals

from django.db import migrations


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
                ABSTRACT AS abstract_bytes
            FROM
                "research"."publikation"
            """,
        ),
        (
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
                IMPACT_FAKTOR_NORM_MAX::float AS impact
            FROM
                "research"."publikation"
            """,
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
            CREATE INDEX research_publication_document_id_idx ON "public"."research_publication" ("document_id");
            """,
            """
            DROP INDEX IF EXISTS research_publication_document_id_idx;
            """,
        ),
        (
            """
            CREATE INDEX research_publication_impact_idx ON "public"."research_publication" ("impact");
            """,
            """
            DROP INDEX IF EXISTS research_publication_impact_idx;
            """,
        ),
    ]

    dependencies = [
        ('research', '0007_bidding_biddingdeadline_biddingendowment'),
    ]

    operations = [
        migrations.RunSQL(
            [forward for forward, reverse in ops],
            [reverse for forward, reverse in reversed(ops)],
        )
    ]
